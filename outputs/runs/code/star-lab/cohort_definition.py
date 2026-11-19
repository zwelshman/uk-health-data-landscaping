"""
OpenSAFELY/ehrQL Cohort Definition for STAR-Lab
=============================================================
Project: STAR-Lab
Institution: DataLoch (partners: RDS, DaSH, HIC, West of Scotland Safe Haven)
Lead: Arlene Casey (PI), Kathy Harrison (Co-I)

Description: LLM-based de-identification of pathology and microbiology free text across four Scottish Safe Havens

Cardiovascular relevance: Indirect — pathology free-text includes cardiovascular specimens; de-identification enables CVD pathology research

Target Datasets: Scottish Safe Havens (DataLoch, DaSH, HIC, WoSSH)

Key Phenotypes: ['Infection (pathology)', 'Microbiology', 'Cardiovascular conditions incidental to pathology text']
"""

from ehrql import create_dataset, minimum_of
from ehrql.tables.tpp import (
    patients,
    clinical_events,
    medications,
    apcs,
    practice_registrations,
    ons_deaths,
)
import codelists

# =============================================================================
# STUDY PARAMETERS
# =============================================================================

STUDY_START_DATE = "2015-01-01"
STUDY_END_DATE = "2024-12-31"
INDEX_DATE = "2020-01-01"
FOLLOWUP_END_DATE = "2023-12-31"

# =============================================================================
# COHORT DEFINITION
# =============================================================================

dataset = create_dataset()

# --- Population ---
has_registration = practice_registrations.for_patient_on(INDEX_DATE).exists_for_patient()
age_at_index = patients.age_on(INDEX_DATE)
is_adult = (age_at_index >= 18) & (age_at_index <= 110)

dataset.define_population(has_registration & is_adult)

# --- INDEX EVENTS ---
# Phenotype-specific index events; codelists imported from codelists module
index_events = clinical_events.where(
    clinical_events.snomedct_code.is_in(codelists.index_event_codes)
).where(clinical_events.date.is_on_or_between(STUDY_START_DATE, STUDY_END_DATE))

first_index_event = index_events.sort_by(clinical_events.date).first_for_patient()
dataset.index_date = first_index_event.date

# --- PRIOR COMORBIDITIES (Charlson + CVD-specific) ---
lookback_start = dataset.index_date - 5 * 365


def has_prior_condition(codes):
    """Condition present in 5-year lookback before index date."""
    return (
        clinical_events.where(clinical_events.snomedct_code.is_in(codes))
        .where(clinical_events.date.is_on_or_between(lookback_start, dataset.index_date - 1))
        .exists_for_patient()
    )


# CVD-specific comorbidities
dataset.prior_mi = has_prior_condition(codelists.mi_codes)
dataset.prior_heart_failure = has_prior_condition(codelists.heart_failure_codes)
dataset.prior_af = has_prior_condition(codelists.atrial_fibrillation_codes)
dataset.prior_stroke = has_prior_condition(codelists.stroke_codes)
dataset.prior_hypertension = has_prior_condition(codelists.hypertension_codes)
dataset.prior_diabetes = has_prior_condition(codelists.diabetes_codes)
dataset.prior_ckd = has_prior_condition(codelists.chronic_kidney_disease_codes)

# Charlson components (abbreviated; extend per study protocol)
dataset.charlson_score = (
    dataset.prior_mi.cast(int)
    + dataset.prior_heart_failure.cast(int)
    + dataset.prior_stroke.cast(int)
    + dataset.prior_diabetes.cast(int)
    + dataset.prior_ckd.cast(int) * 2
)

# --- MEDICATION HISTORY (last 12 months) ---
med_lookback_start = dataset.index_date - 365


def has_medication(codes):
    """Medication issued in 12-month lookback before index date."""
    return (
        medications.where(medications.dmd_code.is_in(codes))
        .where(medications.date.is_on_or_between(med_lookback_start, dataset.index_date - 1))
        .exists_for_patient()
    )


dataset.med_acei_arb = has_medication(codelists.acei_arb_codes)
dataset.med_beta_blocker = has_medication(codelists.beta_blocker_codes)
dataset.med_statin = has_medication(codelists.statin_codes)
dataset.med_anticoagulant = has_medication(codelists.anticoagulant_codes)
dataset.med_antiplatelet = has_medication(codelists.antiplatelet_codes)

# --- TIME-VARYING COVARIATES ---
def latest_measurement_before(date, codes):
    meas = (
        clinical_events.where(clinical_events.snomedct_code.is_in(codes))
        .where(clinical_events.date < date)
        .sort_by(clinical_events.date)
    )
    return meas.last_for_patient().numeric_value


dataset.sbp_at_index = latest_measurement_before(dataset.index_date, codelists.sbp_codes)
dataset.hba1c_at_index = latest_measurement_before(dataset.index_date, codelists.hba1c_codes)
dataset.egfr_at_index = latest_measurement_before(dataset.index_date, codelists.egfr_codes)
dataset.bmi_at_index = latest_measurement_before(dataset.index_date, codelists.bmi_codes)

# --- OUTCOMES ---
followup_end = minimum_of(FOLLOWUP_END_DATE, ons_deaths.date)

mace_events = clinical_events.where(
    clinical_events.snomedct_code.is_in(codelists.mace_codes)
).where(clinical_events.date.is_on_or_between(dataset.index_date + 1, followup_end))

dataset.mace_event = mace_events.exists_for_patient()
dataset.mace_date = mace_events.sort_by(clinical_events.date).first_for_patient().date

dataset.death_date = ons_deaths.date
dataset.all_cause_death = ons_deaths.date.is_on_or_between(dataset.index_date + 1, followup_end)

# --- COHORT ATTRIBUTES ---
dataset.age_at_index = age_at_index
dataset.sex = patients.sex
dataset.followup_days = (followup_end - dataset.index_date).days

# =============================================================================
# EXPORT
# =============================================================================
# Run with: opensafely run ehrql:v1 --dataset-definition cohort_definition.py --output output.csv
