"""
OpenSAFELY/ehrQL Cohort Definition for CARDINAL-DATA Project
=============================================================
Project: CARDINAL-DATA - Extends the cardiovascular-renal-metabolic data specification 
already proven in the London SDE

Institution: London Secure Data Environment (OneLondon)
Lead: Not specified in HDRS metadata
Funding: HDRS Technology Transformation Projects funding

Target Datasets (from HDR UK Gateway):
- UK Biobank (500,000 participants) - Population ≥60k ✅
- CPRD Aurum (England, ~60M patients) - Population ≥60k ✅
- SAIL Databank (Wales, ~3.2M) - Population ≥60k ✅
- NHS England GPDPR (England, ~56M) - Population ≥60k ✅

Key Phenotypes: Cardiovascular, Renal, Metabolic conditions
"""

from ehrql import create_dataset, case, when, minimum_of, maximum_of
from ehrql.tables.tpp import (
    patients, 
    clinical_events, 
    medications, 
    apcs, 
    practice_registrations,
    ons_deaths
)
import codelists

# =============================================================================
# CODELIST DEFINITIONS (referenced from codelists.json)
# =============================================================================

# Cardiovascular phenotypes
MI_CODES = codelists.mi_codes
HEART_FAILURE_CODES = codelists.heart_failure_codes
ATRIAL_FIBRILLATION_CODES = codelists.atrial_fibrillation_codes
STROKE_CODES = codelists.stroke_codes
HYPERTENSION_CODES = codelists.hypertension_codes
PAD_CODES = codelists.peripheral_arterial_disease_codes
VALVULAR_DISEASE_CODES = codelists.valvular_disease_codes
CARDIOMYOPATHY_CODES = codelists.cardiomyopathy_codes
CONGENITAL_HEART_CODES = codelists.congenital_heart_disease_codes

# Renal phenotypes
CKD_CODES = codelists.chronic_kidney_disease_codes
AKI_CODES = codelists.acute_kidney_injury_codes

# Metabolic phenotypes
DIABETES_T1_CODES = codelists.diabetes_type1_codes
DIABETES_T2_CODES = codelists.diabetes_type2_codes
OBESITY_CODES = codelists.obesity_codes
DYSLIPIDEMIA_CODES = codelists.dyslipidemia_codes

# Medication codelists
ACEI_ARB_CODES = codelists.acei_arb_codes
BETA_BLOCKER_CODES = codelists.beta_blocker_codes
STATIN_CODES = codelists.statin_codes
ANTICOAGULANT_CODES = codelists.anticoagulant_codes
ANTIPLATELET_CODES = codelists.antiplatelet_codes
SGLT2_CODES = codelists.sglt2_inhibitor_codes
GLP1_CODES = codelists.glp1_agonist_codes
DIURETIC_CODES = codelists.diuretic_codes

# =============================================================================
# STUDY PARAMETERS
# =============================================================================

STUDY_START_DATE = "2015-01-01"
STUDY_END_DATE = "2024-12-31"
INDEX_DATE = "2020-01-01"  # COVID-19 pandemic start for CVD-COVID-UK alignment
FOLLOWUP_END_DATE = "2023-12-31"

# =============================================================================
# COHORT DEFINITION
# =============================================================================

dataset = create_dataset()

# --- Population ---
# Registered at a practice during study period
has_registration = practice_registrations.for_patient_on(INDEX_DATE).exists_for_patient()

# Age at index date (adults 18+)
age_at_index = patients.age_on(INDEX_DATE)
is_adult = (age_at_index >= 18) & (age_at_index <= 110)

# Sex
sex = patients.sex

# Ethnicity (from most recent clinical event)
ethnicity = clinical_events.where(
    clinical_events.snomedct_code.is_in(codelists.ethnicity_codes)
).sort_by(clinical_events.date).last_for_patient().snomedct_code.to_category(codelists.ethnicity_map)

# IMD quintile (deprivation)
imd = practice_registrations.for_patient_on(INDEX_DATE).practice_nuts1_region_name

# --- BASE COHORT ---
dataset.define_population(has_registration & is_adult)

# --- INDEX EVENTS ---
# First cardiovascular event during study period
cv_events = clinical_events.where(
    clinical_events.snomedct_code.is_in(
        MI_CODES + HEART_FAILURE_CODES + ATRIAL_FIBRILLATION_CODES + 
        STROKE_CODES + HYPERTENSION_CODES + PAD_CODES + 
        VALVULAR_DISEASE_CODES + CARDIOMYOPATHY_CODES + CONGENITAL_HEART_CODES
    )
).where(clinical_events.date.is_on_or_between(STUDY_START_DATE, STUDY_END_DATE))

first_cv_event = cv_events.sort_by(clinical_events.date).first_for_patient()
dataset.index_date = first_cv_event.date
dataset.index_event_type = first_cv_event.snomedct_code.to_category(codelists.cv_event_type_map)

# --- PRIOR COMORBIDITIES (Charlson/ELIXHAUSER + CVD-specific) ---
# Lookback period: 5 years before index date
lookback_start = dataset.index_date - 5 * 365

def has_prior_condition(codes, name):
    """Check for condition in 5-year lookback before index date"""
    events = clinical_events.where(
        clinical_events.snomedct_code.is_in(codes)
    ).where(clinical_events.date.is_on_or_between(lookback_start, dataset.index_date - 1))
    return events.exists_for_patient()

# Cardiovascular comorbidities
dataset.prior_mi = has_prior_condition(MI_CODES, "prior_mi")
dataset.prior_heart_failure = has_prior_condition(HEART_FAILURE_CODES, "prior_hf")
dataset.prior_af = has_prior_condition(ATRIAL_FIBRILLATION_CODES, "prior_af")
dataset.prior_stroke = has_prior_condition(STROKE_CODES, "prior_stroke")
dataset.prior_hypertension = has_prior_condition(HYPERTENSION_CODES, "prior_htn")
dataset.prior_pad = has_prior_condition(PAD_CODES, "prior_pad")
dataset.prior_valvular = has_prior_condition(VALVULAR_DISEASE_CODES, "prior_valvular")
dataset.prior_cardiomyopathy = has_prior_condition(CARDIOMYOPATHY_CODES, "prior_cmp")
dataset.prior_congenital = has_prior_condition(CONGENITAL_HEART_CODES, "prior_chd")

# Renal comorbidities
dataset.prior_ckd = has_prior_condition(CKD_CODES, "prior_ckd")
dataset.prior_aki = has_prior_condition(AKI_CODES, "prior_aki")

# Metabolic comorbidities
dataset.prior_diabetes_t1 = has_prior_condition(DIABETES_T1_CODES, "prior_dm1")
dataset.prior_diabetes_t2 = has_prior_condition(DIABETES_T2_CODES, "prior_dm2")
dataset.prior_obesity = has_prior_condition(OBESITY_CODES, "prior_obesity")
dataset.prior_dyslipidemia = has_prior_condition(DYSLIPIDEMIA_CODES, "prior_dyslip")

# Charlson Comorbidity Index components (simplified)
dataset.charlson_mi = dataset.prior_mi
dataset.charlson_chf = dataset.prior_heart_failure
dataset.charlson_pvd = dataset.prior_pad
dataset.charlson_cvd = dataset.prior_stroke
dataset.charlson_dementia = has_prior_condition(codelists.dementia_codes, "prior_dementia")
dataset.charlson_copd = has_prior_condition(codelists.copd_codes, "prior_copd")
dataset.charlson_rheumatic = has_prior_condition(codelists.rheumatic_disease_codes, "prior_rheum")
dataset.charlson_peptic_ulcer = has_prior_condition(codelists.peptic_ulcer_codes, "prior_pud")
dataset.charlson_liver_mild = has_prior_condition(codelists.mild_liver_disease_codes, "prior_liver_mild")
dataset.charlson_diabetes = dataset.prior_diabetes_t1 | dataset.prior_diabetes_t2
dataset.charlson_diabetes_complications = has_prior_condition(codelists.diabetes_complications_codes, "prior_dm_comp")
dataset.charlson_paraplegia = has_prior_condition(codelists.paraplegia_codes, "prior_para")
dataset.charlson_renal = dataset.prior_ckd
dataset.charlson_cancer = has_prior_condition(codelists.cancer_codes, "prior_cancer")
dataset.charlson_liver_severe = has_prior_condition(codelists.severe_liver_disease_codes, "prior_liver_sev")
dataset.charlson_metastatic = has_prior_condition(codelists.metastatic_cancer_codes, "prior_mets")
dataset.charlson_hiv = has_prior_condition(codelists.hiv_codes, "prior_hiv")

# Calculate Charlson score
dataset.charlson_score = (
    dataset.charlson_mi * 1 +
    dataset.charlson_chf * 1 +
    dataset.charlson_pvd * 1 +
    dataset.charlson_cvd * 1 +
    dataset.charlson_dementia * 1 +
    dataset.charlson_copd * 1 +
    dataset.charlson_rheumatic * 1 +
    dataset.charlson_peptic_ulcer * 1 +
    dataset.charlson_liver_mild * 1 +
    dataset.charlson_diabetes * 1 +
    dataset.charlson_diabetes_complications * 2 +
    dataset.charlson_paraplegia * 2 +
    dataset.charlson_renal * 2 +
    dataset.charlson_cancer * 2 +
    dataset.charlson_liver_severe * 3 +
    dataset.charlson_metastatic * 6 +
    dataset.charlson_hiv * 6
)

# --- MEDICATION HISTORY (12 months prior to index) ---
med_lookback_start = dataset.index_date - 365

def has_medication(codes, name):
    """Check for medication in 12-month lookback before index date"""
    meds = medications.where(
        medications.dmd_code.is_in(codes)
    ).where(medications.date.is_on_or_between(med_lookback_start, dataset.index_date - 1))
    return meds.exists_for_patient()

dataset.med_acei_arb = has_medication(ACEI_ARB_CODES, "med_acei_arb")
dataset.med_beta_blocker = has_medication(BETA_BLOCKER_CODES, "med_bb")
dataset.med_statin = has_medication(STATIN_CODES, "med_statin")
dataset.med_anticoagulant = has_medication(ANTICOAGULANT_CODES, "med_anticoag")
dataset.med_antiplatelet = has_medication(ANTIPLATELET_CODES, "med_antiplt")
dataset.med_sglt2 = has_medication(SGLT2_CODES, "med_sglt2")
dataset.med_glp1 = has_medication(GLP1_CODES, "med_glp1")
dataset.med_diuretic = has_medication(DIURETIC_CODES, "med_diuretic")

# Polypharmacy count
dataset.med_count = (
    dataset.med_acei_arb.cast(int) +
    dataset.med_beta_blocker.cast(int) +
    dataset.med_statin.cast(int) +
    dataset.med_anticoagulant.cast(int) +
    dataset.med_antiplatelet.cast(int) +
    dataset.med_sglt2.cast(int) +
    dataset.med_glp1.cast(int) +
    dataset.med_diuretic.cast(int)
)

# --- TIME-VARYING COVARIATES ---
# Annual measurements during follow-up
def latest_measurement_before(date, codes, value_column="numeric_value"):
    """Get latest measurement value before a given date"""
    meas = clinical_events.where(
        clinical_events.snomedct_code.is_in(codes)
    ).where(clinical_events.date < date).sort_by(clinical_events.date)
    return meas.last_for_patient()[value_column]

# Systolic BP (time-varying)
dataset.sbp_at_index = latest_measurement_before(dataset.index_date, codelists.sbp_codes)
dataset.sbp_1yr = latest_measurement_before(dataset.index_date + 365, codelists.sbp_codes)
dataset.sbp_2yr = latest_measurement_before(dataset.index_date + 730, codelists.sbp_codes)

# Diastolic BP
dataset.dbp_at_index = latest_measurement_before(dataset.index_date, codelists.dbp_codes)
dataset.dbp_1yr = latest_measurement_before(dataset.index_date + 365, codelists.dbp_codes)
dataset.dbp_2yr = latest_measurement_before(dataset.index_date + 730, codelists.dbp_codes)

# HbA1c
dataset.hba1c_at_index = latest_measurement_before(dataset.index_date, codelists.hba1c_codes)
dataset.hba1c_1yr = latest_measurement_before(dataset.index_date + 365, codelists.hba1c_codes)
dataset.hba1c_2yr = latest_measurement_before(dataset.index_date + 730, codelists.hba1c_codes)

# eGFR
dataset.egfr_at_index = latest_measurement_before(dataset.index_date, codelists.egfr_codes)
dataset.egfr_1yr = latest_measurement_before(dataset.index_date + 365, codelists.egfr_codes)
dataset.egfr_2yr = latest_measurement_before(dataset.index_date + 730, codelists.egfr_codes)

# Total cholesterol
dataset.chol_at_index = latest_measurement_before(dataset.index_date, codelists.cholesterol_codes)
dataset.chol_1yr = latest_measurement_before(dataset.index_date + 365, codelists.cholesterol_codes)
dataset.chol_2yr = latest_measurement_before(dataset.index_date + 730, codelists.cholesterol_codes)

# BMI
dataset.bmi_at_index = latest_measurement_before(dataset.index_date, codelists.bmi_codes)
dataset.bmi_1yr = latest_measurement_before(dataset.index_date + 365, codelists.bmi_codes)
dataset.bmi_2yr = latest_measurement_before(dataset.index_date + 730, codelists.bmi_codes)

# --- OUTCOMES ---
# Major Adverse Cardiovascular Events (MACE) during follow-up
followup_end = minimum_of(FOLLOWUP_END_DATE, ons_deaths.date)

mace_events = clinical_events.where(
    clinical_events.snomedct_code.is_in(
        MI_CODES + STROKE_CODES + codelists.cardiovascular_death_codes
    )
).where(clinical_events.date.is_on_or_between(dataset.index_date + 1, followup_end))

dataset.mace_event = mace_events.exists_for_patient()
dataset.mace_date = mace_events.sort_by(clinical_events.date).first_for_patient().date
dataset.mace_type = mace_events.sort_by(clinical_events.date).first_for_patient().snomedct_code.to_category(codelists.mace_type_map)

# Heart failure hospitalization
hf_hosp = apcs.where(
    apcs.primary_diagnosis.is_in(HEART_FAILURE_CODES)
).where(apcs.admission_date.is_on_or_between(dataset.index_date + 1, followup_end))

dataset.hf_hospitalization = hf_hosp.exists_for_patient()
dataset.hf_hosp_date = hf_hosp.sort_by(apcs.admission_date).first_for_patient().admission_date

# All-cause mortality
dataset.death_date = ons_deaths.date
dataset.all_cause_death = ons_deaths.date.is_on_or_between(dataset.index_date + 1, followup_end)
dataset.cv_death = (
    ons_deaths.underlying_cause_of_death.is_in(codelists.cardiovascular_death_codes) &
    dataset.all_cause_death
)

# --- COHORT ATTRIBUTES ---
dataset.age_at_index = age_at_index
dataset.sex = sex
dataset.ethnicity = ethnicity
dataset.imd_quintile = imd
dataset.followup_days = (followup_end - dataset.index_date).days

# =============================================================================
# EXPORT
# =============================================================================
# Dataset is ready for analysis in OpenSAFELY
# Run with: opensafely run ehrql:v1.3 --dataset-definition cohort_definition.py --output output.parquet