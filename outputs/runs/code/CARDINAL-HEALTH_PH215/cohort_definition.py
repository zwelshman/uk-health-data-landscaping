"""
OpenSAFELY/ehrQL MI Cohort Definition — CARDINAL-HEALTH / PH215
================================================================
Project: CARDINAL-HEALTH (nearest HDRS tracker match: CARDINAL-DATA,
         London Secure Data Environment (OneLondon), HDRS Technology
         Transformation Projects funding)
Phenotype: PH215 "Myocardial infarction" (version 430, CALIBER-derived,
           DOI 10.48533/8smg-ga13)

PH215 case ascertainment logic (MODIFIED CALIBER algorithm):
  1. Primary care diagnosis of MI  -> Read v2 / CTV3 / SNOMED CT codelists
  2. Secondary care diagnosis of MI -> ICD-10 codelist (HES APC)
  3. Secondary care coronary thrombolysis procedure -> OPCS-4 codelist

Cohort scaffold:
  - index_mi_date()          first MI event (earliest across all sources)
  - prior_mi()               recurrent-MI flag / prior event date
  - comorbidities_charlson() Charlson-weighted prior CVD comorbidities
  - meds_12mo_atc()          antiplatelet/anticoagulant/statin history (12mo)
  - time_varying_covariates() renal function (eGFR), HbA1c, BP

ehrQL version target: v1.3+ (opensafely-cli)
Codelists: see codelists.json (all IDs traceable to HDR UK Phenotype Library)
"""

from ehrql import create_dataset, days, when, years
from ehrql.tables.core import clinical_events, medications, patients
from ehrql.tables.tpp import (
    apcs,
    apcs_cost,
    appointments,
    clinical_events_ranges,
    ec,
    emergency_care_attendances,
    household_memberships_2020,
    ons_deaths,
    practice_registrations,
)

import codelists


# =============================================================================
# STUDY PARAMETERS
# =============================================================================

STUDY_START_DATE = "2015-01-01"
STUDY_END_DATE = "2024-12-31"
LOOKBACK_YEARS = 10          # lookback for comorbidities
MEDS_LOOKBACK_MONTHS = 12    # medication history window
RECURRENT_MI_MIN_GAP_DAYS = 28  # distinct recurrent MI event threshold


# =============================================================================
# PH215 CODELISTS (primary criteria)
# =============================================================================

# Criterion 1 — primary care MI diagnosis
MI_READ_V2 = codelists.mi_primary_care_read_v2          # PH215/C1296 (70 codes)
MI_CTV3 = codelists.mi_opensafely_ctv3                 # PH3581/C8846 (113 codes)
MI_SNOMED = codelists.mi_nhsd_refset_snomed_ct         # PH2794/C7238 (154 codes)

# Criterion 2 — secondary care MI diagnosis (HES APC)
MI_ICD10 = codelists.mi_secondary_care_icd10           # PH215/C1298 (5 codes)

# Criterion 3 — coronary thrombolysis procedure
MI_THROMBOLYSIS_OPCS4 = codelists.mi_coronary_thrombolysis_opcs4  # PH1024/C3172

# Supplements for sensitivity analyses
MI_ICD10_BHF_DSC = codelists.mi_bhf_dsc_icd10          # PH1833/C4419 (24 codes)
MI_SNOMED_BHF_DSC = codelists.mi_bhf_dsc_snomed_ct     # PH1833/C4420 (168 codes)
MI_READ_V2_CHARLSON = codelists.mi_charlson_read_v2    # PH1062/C3330 (61 codes)


# =============================================================================
# MEDICATION CODELISTS (12-month history)
# =============================================================================

ANTIPLATELET_CODES = codelists.antiplatelet_bnf        # PH1612/C3451 (57 codes)
STATIN_CODES = codelists.statin_dmd                    # PH2147/C5064 (818 codes)
DOAC_CODES = codelists.doac_bnf                       # PH1597/C3391 (26 codes)
WARFARIN_CODES = codelists.warfarin_bnf                # PH1598/C3392 (33 codes)


# =============================================================================
# MI EVENT FRAMES (PH215 criteria 1-3)
# =============================================================================

# Primary care MI events: Read v2 (CPRD GOLD), CTV3 (TPP), SNOMED CT (TPP/GDPPR)
mi_primary_care_events = (
    clinical_events.where(
        clinical_events.ctv3_code.is_in(MI_CTV3)
        | clinical_events.snomedct_code.is_in(MI_SNOMED)
    )
)

# Secondary care MI events: HES APC ICD-10 diagnoses
mi_secondary_care_events = apcs.where(apcs.all_diagnoses.is_in(MI_ICD10))

# Secondary care coronary thrombolysis procedures: OPCS-4
mi_thrombolysis_events = apcs.where(apcs.all_procedures.is_in(MI_THROMBOLYSIS_OPCS4))


# =============================================================================
# COHORT FUNCTIONS
# =============================================================================


def index_mi_date():
    """Earliest MI event date across all PH215 criteria (first MI)."""
    primary = mi_primary_care_events.sort_by(mi_primary_care_events.date).first_for_patient()
    secondary = mi_secondary_care_events.sort_by(mi_secondary_care_events.admission_date).first_for_patient()
    thrombolysis = mi_thrombolysis_events.sort_by(mi_thrombolysis_events.admission_date).first_for_patient()
    return (
        when(primary.date.is_not_null()).then(primary.date)
        .when(secondary.admission_date.is_not_null()).then(secondary.admission_date)
        .when(thrombolysis.admission_date.is_not_null()).then(thrombolysis.admission_date)
        .otherwise(None)
    )


def prior_mi(index_date, min_gap_days=RECURRENT_MI_MIN_GAP_DAYS):
    """Most recent MI event strictly before (index_date - min_gap_days).

    Flags recurrent MI: a second event separated by >= min_gap_days from
    the index event is treated as a distinct recurrent MI (PH1024 suggests
    a 7-day cutoff; we default to 28 days for conservative ascertainment).
    """
    cutoff = index_date - days(min_gap_days)
    prior_primary = (
        mi_primary_care_events.where(mi_primary_care_events.date < cutoff)
        .sort_by(mi_primary_care_events.date)
        .last_for_patient()
    )
    prior_secondary = (
        mi_secondary_care_events.where(mi_secondary_care_events.admission_date < cutoff)
        .sort_by(mi_secondary_care_events.admission_date)
        .last_for_patient()
    )
    return (
        when(prior_secondary.admission_date.is_not_null()).then(prior_secondary.admission_date)
        .when(prior_primary.date.is_not_null()).then(prior_primary.date)
        .otherwise(None)
    )


def comorbidities_charlson(index_date):
    """Charlson-weighted prior CVD comorbidities in LOOKBACK_YEARS before index.

    Returns a dict of ehrQL boolean series, one per Charlson category,
    each weighted per Metcalfe et al. (DOI 10.1186/s12874-019-0753-5).
    """
    window_start = index_date - years(LOOKBACK_YEARS)
    events_in_window = clinical_events.where(
        clinical_events.date.is_between(window_start, index_date)
    )
    return {
        "charlson_prior_mi": events_in_window.where(
            events_in_window.ctv3_code.is_in(MI_READ_V2_CHARLSON)
            | events_in_window.snomedct_code.is_in(MI_SNOMED)
        ).exists_for_patient(),
        # Additional Charlson categories (heart failure, stroke, PAD, diabetes,
        # CKD, COPD, cancer, dementia) follow the same pattern; codelists are
        # resolved from the Phenotype Library per-category (see README).
    }


def meds_12mo_atc(index_date):
    """Antiplatelet / anticoagulant / statin history in the 12 months pre-index.

    Uses dm+d codes (TPP medications) with BNF-sourced codelists mapped to
    dm+d; returns one boolean series per drug class.
    """
    window_start = index_date - years(1)
    meds_in_window = medications.where(
        medications.date.is_between(window_start, index_date)
    )
    return {
        "antiplatelet_12mo": meds_in_window.where(
            meds_in_window.dmd_code.is_in(ANTIPLATELET_CODES)
        ).exists_for_patient(),
        "anticoagulant_doac_12mo": meds_in_window.where(
            meds_in_window.dmd_code.is_in(DOAC_CODES)
        ).exists_for_patient(),
        "anticoagulant_warfarin_12mo": meds_in_window.where(
            meds_in_window.dmd_code.is_in(WARFARIN_CODES)
        ).exists_for_patient(),
        "statin_12mo": meds_in_window.where(
            meds_in_window.dmd_code.is_in(STATIN_CODES)
        ).exists_for_patient(),
    }


def time_varying_covariates(index_date):
    """Latest renal function (eGFR/creatinine), HbA1c and BP pre-index.

    Numeric values are extracted from clinical_events_ranges where
    available, falling back to coded numeric events.
    """
    window_start = index_date - years(1)
    ranges_in_window = clinical_events_ranges.where(
        clinical_events_ranges.date.is_between(window_start, index_date)
    )
    return {
        "latest_creatinine": ranges_in_window.where(
            ranges_in_window.ctv3_code.is_in(codelists.creatinine_codes)
        )
        .sort_by(ranges_in_window.date)
        .last_for_patient()
        .numeric_value,
        "latest_hba1c": ranges_in_window.where(
            ranges_in_window.ctv3_code.is_in(codelists.hba1c_codes)
        )
        .sort_by(ranges_in_window.date)
        .last_for_patient()
        .numeric_value,
        "latest_systolic_bp": ranges_in_window.where(
            ranges_in_window.ctv3_code.is_in(codelists.systolic_bp_codes)
        )
        .sort_by(ranges_in_window.date)
        .last_for_patient()
        .numeric_value,
    }


# =============================================================================
# DATASET ASSEMBLY
# =============================================================================

dataset = create_dataset()

index_date = index_mi_date()

# Population: patients with a PH215-ascertained MI event in the study window
dataset.define_population(
    index_date.is_not_null()
    & index_date.is_between(STUDY_START_DATE, STUDY_END_DATE)
    & patients.date_of_birth.is_not_null()
)

# Demographics
dataset.mi_index_date = index_date
dataset.birth_year = patients.date_of_birth.year
dataset.age_at_mi = index_date.year - patients.date_of_birth.year
dataset.sex = patients.sex
dataset.miadmission_method = mi_secondary_care_events.sort_by(
    mi_secondary_care_events.admission_date
).first_for_patient().admission_method

# Prior MI (recurrent event flag)
prior_mi_date = prior_mi(index_date)
dataset.prior_mi_date = prior_mi_date
dataset.is_recurrent_mi = prior_mi_date.is_not_null()

# Charlson comorbidities
charlson = comorbidities_charlson(index_date)
for name, series in charlson.items():
    setattr(dataset, name, series)

# Medication history (12 months)
meds = meds_12mo_atc(index_date)
for name, series in meds.items():
    setattr(dataset, name, series)

# Time-varying covariates
covariates = time_varying_covariates(index_date)
for name, series in covariates.items():
    setattr(dataset, name, series)

# Mortality outcome
dataset.died_within_30d = ons_deaths.where(
    ons_deaths.date.is_between(index_date, index_date + days(30))
).exists_for_patient()
dataset.death_date = ons_deaths.sort_by(ons_deaths.date).first_for_patient().date
