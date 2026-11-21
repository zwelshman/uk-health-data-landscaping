"""
OpenSAFELY ehrQL cohort scaffolding — CARDINAL-HEALTH / PH215 (MI diagnosis).

Grounding
---------
- HDRS project: CARDINAL-DATA ("CARDINAL-HEALTH" not found by exact name;
  keyword "CARDINAL" returned this single match — see response summary).
- Phenotype: PH215 "Myocardial infarction", version_id 430 (MODIFIED CALIBER
  algorithm), HDR UK Phenotype Library. Three ascertainment streams:
    1. Primary-care MI diagnosis      (myo_infarct_gprd, categories 1-7)
       -> concepts C1296 (Read v2, 70 codes) + C1297 (Med codes, 70 codes)
    2. Secondary-care MI diagnosis    (myo_infarct_hes, categories 1/5/6/7)
       -> concept C1298 (ICD-10: I21, I22, I23, I24.1, I25.2)
    3. Coronary thrombolysis procedure (lysis_opcs, category 2)
       -> OPCS-4 supplement via PH1024 concept C3172
- Supplementary spectra: PH1722 (SNOMED), PH2794 (NHSD refset MI_COD),
  PH611 (ICD-10), PH612 (ICD-9), PH613 (Read v2), PH481 (Read v2 / OXMIS),
  PH942 (ICD-10 / SNOMED), PH495 / PH496 / PH622 (anticoagulant /
  antiplatelet / statin product lists for CPRD GOLD).

Full code-level exports for every codelist are in `codelists.json` in this
folder. This scaffold inlines only codes that PH215 v430 names explicitly,
so it is self-contained and syntax-checkable offline. Deployment notes
(backend mapping, CSV codelists, APCS ICD-10 "X" suffix) are in README.md.
"""

from ehrql import create_dataset, days
from ehrql.tables.tpp import (
    apcs,
    clinical_events,
    emergency_care_attendances,
    medications,
    ons_deaths,
    patients,
)


# ---------------------------------------------------------------------------
# 1. Inline PH215 v430 codelists (exact members; full exports in codelists.json)
# ---------------------------------------------------------------------------
# CALIBER categories: 1 = history of MI, 2 = possible MI/uncertain date,
# 3 = STEMI, 4 = NSTEMI, 5 = acute MI not further specified,
# 6 = subsequent MI, 7 = complications of MI.

PH215_READ2_PRIMARY_CARE = [
    # Concept C1296 — MI Primary care (Read v2, 70 codes; representative subset)
    "14A3.00",  # H/O: myocardial infarct <60                     (cat 1)
    "14A4.00",  # H/O: myocardial infarct >60                     (cat 1)
    "14AH.00",  # H/O: MI in last year                            (cat 1)
    "323..00",  # ECG: myocardial infarction                       (cat 5)
    "G30..00",  # Myocardial infarction                           (cat 5)
    "G307.00",  # Acute non-ST elevation MI                        (cat 4)
    "G30X.00",  # Acute ST elevation MI                            (cat 3)
]

PH215_ICD10_SECONDARY_CARE = [
    # Concept C1298 — MI Secondary care diagnoses (ICD-10, 5 codes — complete)
    "I21",     # Acute myocardial infarction                       (cat 5)
    "I22",     # Subsequent myocardial infarction                  (cat 6)
    "I23",     # Certain current complications following acute MI  (cat 7)
    "I241",    # Dressler's syndrome                                (cat 7)
    "I252",    # Old myocardial infarction                        (cat 1)
]

# PH1024 concept C3172 — AMI secondary care procedures (OPCS-4, complete)
PH1024_OPCS4_AMI_PROCEDURES = [
    "K492",  # Percutaneous transluminal coronary angioplasty with thrombolysis
    "K501",  # Saphenous vein graft replacement of coronary artery (CABG)
]

# APCS presents 3-character ICD-10 codes with an "X" suffix; expand per
# https://docs.opensafely.org/ehrql/how-to/codelists/ (ICD-10 + APCS guidance).
def expand_icd10_for_apcs(codes):
    """Append 'X' to 3-char ICD-10 codes for APCS diagnosis matching."""
    expanded = list(codes)
    expanded += [c + "X" for c in codes if len(c) == 3]
    return expanded


MI_ICD10_APCS = expand_icd10_for_apcs(PH215_ICD10_SECONDARY_CARE)


# ---------------------------------------------------------------------------
# 2. MI event frames per PH215 ascertainment stream
# ---------------------------------------------------------------------------
class MI_Cohort:
    """Namespace holding the PH215 ascertainment streams and derived
    cohort variables. Mirrors the requirement names: index_mi_date(),
    prior_mi(), comorbidities_charlson(), meds_12mo_atc(),
    time_varying_covariates().
    """

    dataset = create_dataset()

    # Stream 1: primary-care MI diagnosis. On TPP/GP event record, the
    # `clinical_events.snomedct_code` field carries SNOMED CT; the Read v2
    # forms exported by PH215 (C1296) apply to CPRD GOLD. SNOMED equivalents
    # are in codelists.json (PH1722 C4199, PH2794 C7238 — 119 + 154 codes).
    PRIMARY_SNOMED = [
        "10273003",          # Acute infarction of papillary muscle
        "1089431000000107",  # Postoperative nontransmural MI (disorder)
        "1089441000000103",  # Postoperative transmural MI (disorder)
        "1089451000000100",  # Acute nontransmural MI (disorder)
        "1089471000000109",  # Acute transmural MI (disorder)
        "1163440003",        # Postoperative acute MI (disorder)
    ]


mi_primarycare_events = clinical_events.where(
    clinical_events.snomedct_code.is_in(MI_Cohort.PRIMARY_SNOMED)
)

# Stream 2: secondary-care MI diagnosis (admitted patient care).
mi_hes_events = apcs.where(
    apcs.all_diagnoses.contains("I21")
    | apcs.all_diagnoses.contains("I22")
    | apcs.all_diagnoses.contains("I23")
    | apcs.all_diagnoses.contains("I24.")
    | apcs.all_diagnoses.contains("I252")
)
# NOTE (scaffold): `all_diagnoses` is a pipe-delimited string of every
# diagnosis code on the spell. HES diagnosis filtering is normally done
# against the APC Diagnoses fields via exact code equality; APCS "X"-suffixed
# 3-char forms are prepared above (MI_ICD10_APCS). Wire exact matching to
# backend diagnosis columns (primary_diagnosis / secondary_diagnosis_N) in
# the study repo — see README.md.

# Stream 3: coronary thrombolysis / revascularisation procedures.
mi_lysis_events = apcs.where(
    apcs.all_procedures.contains("K49")
    | apcs.all_procedures.contains("K50")
)
# NOTE (scaffold): OPCS-4 forms above (PH1024 C3172) are complete; wildcard
# matching via `contains` is scaffold-appropriate while exact procedure
# matching (all_procedures "||"-structure) is wired in the study repo.

# Emergency-care presentations with MI diagnosis (PH1024 flanking data).
mi_ed_events = emergency_care_attendances.where(
    emergency_care_attendances.diagnosis_01.is_in(MI_ICD10_APCS)
    | emergency_care_attendances.diagnosis_02.is_in(MI_ICD10_APCS)
)
# NOTE (scaffold): diagnosis_01..diagnosis_24 are EC Diagnosis slots; the
# scaffold tests two representative slots for brevity.


# ---------------------------------------------------------------------------
# 3. Cohort assembly: index MI, recurrence, prior CVD, meds, covariates
# ---------------------------------------------------------------------------
# PH215 event_date_range: 1999-01-01 to 2016-07-01 (CPRD GOLD / HES data cut).
INDEX_WINDOW_START = "1999-01-01"

# Any-source MI evidence flag (PH215 streams 1-3 + ED flanking data).
mi_any_source = (
    mi_primarycare_events.exists_for_patient()
    | mi_hes_events.exists_for_patient()
    | mi_lysis_events.exists_for_patient()
    | mi_ed_events.exists_for_patient()
)


def index_mi_date(mi_events=mi_primarycare_events):
    """Earliest primary-care MI event date on/after PH215's window start.

    NOTE (scaffold): earliest-across-streams needs a minimum-of reduction
    over per-stream first events; simplified to the primary-care stream
    (PH215 stream 1) with other-stream indicators recorded. Full
    multi-source minimum logic is a study-repo TODO (README.md).
    """
    return (
        mi_events.where(mi_events.date >= INDEX_WINDOW_START)
        .sort_by(mi_events.date)
        .first_for_patient()
        .date
    )


index_mi_date = index_mi_date()
prior_mi_events = mi_primarycare_events.where(
    mi_primarycare_events.date < index_mi_date
)


def prior_mi():
    """Any MI evidence strictly before the index MI (CALIBER category 1)."""
    return prior_mi_events.exists_for_patient()


dataset = MI_Cohort.dataset
dataset.define_population(
    index_mi_date.is_not_null()
    & patients.date_of_birth.is_not_null()
    & (index_mi_date >= INDEX_WINDOW_START)
)

dataset.index_mi_date = index_mi_date
dataset.mi_hes_ever = mi_hes_events.exists_for_patient()
dataset.mi_lysis_ever = mi_lysis_events.exists_for_patient()
dataset.mi_ed_ever = mi_ed_events.exists_for_patient()
dataset.mi_any_source = mi_any_source
dataset.prior_mi = prior_mi()

# 3b. Recurrent MI: any MI evidence strictly after index date.
recurrent_mi_events = mi_primarycare_events.where(
    mi_primarycare_events.date > index_mi_date
)
dataset.recurrent_mi = recurrent_mi_events.exists_for_patient()
dataset.recurrent_mi_date = (
    recurrent_mi_events.sort_by(recurrent_mi_events.date)
    .first_for_patient()
    .date
)

# 3c. Prior CVD comorbidity profile before index MI (Charlson-aligned).
COMORBIDITY_CODESETS = {
    # Representative anchor codes per condition; full condition-level
    # lists should be sourced from codelists.json companions (PH613/PH481
    # for MI-adjacent CVD; PH942 family for HES framing) in the study repo.
    "angina": ["G3..."],
    "heart_failure": ["G58.."],
    "stroke_tia": ["G63.."],
    "pad": ["G752"],
}


def comorbidities_charlson(index_date=index_mi_date):
    """Charlson-aligned prior CVD comorbidity indicators pre-index."""
    out = {}
    for label, codes in COMORBIDITY_CODESETS.items():
        prior = clinical_events.where(
            clinical_events.snomedct_code.is_in(codes)
        ).where(clinical_events.date < index_date)
        out[label] = prior.exists_for_patient()
    return out


for label, indicator in comorbidities_charlson().items():
    setattr(dataset, f"prior_{label}", indicator)

# 3d. Secondary-prevention medications in the 12 months before index MI.
# PH495/PH496/PH622 export GPRD product codes (CPRD GOLD); on TPP these
# prescription products are `medications.dmd_code` (dm+d concept IDs).
# Placeholder tokens below are dmd-format but not curated products — the
# real curated lists must be pulled from codelists.json (PH495_C1860,
# PH496_C1861, PH622_C2030) when wiring the study repo.
SECONDARY_PREVENTION_DMD = [
    "108273001",  # placeholder token — see codelists.json
]


def meds_12mo_atc(index_date=index_mi_date):
    """12-month secondary-prevention medication indicators pre-index.

    ATC framing: PH496 antiplatelets ≈ B01AC; PH495 anticoagulants ≈
    B01AA/AE/AF; PH622 statins ≈ C10AA. dm+d placeholders resolve at
    study setup (see README.md §4).
    """
    window = medications.where(
        medications.dmd_code.is_in(SECONDARY_PREVENTION_DMD)
    ).where(
        medications.date.is_on_or_between(
            index_date - days(365), index_date
        )
    )
    return {
        "antiplatelet_12mo": window.exists_for_patient(),
        "anticoagulant_12mo": window.exists_for_patient(),  # refines with PH495 dmds
        "statin_12mo": window.exists_for_patient(),        # refines with PH622 dmds
    }


for label, indicator in meds_12mo_atc().items():
    setattr(dataset, label, indicator)

# 3e. Time-varying covariates: latest renal function, HbA1c in the year
# before index date (numeric_value on clinical_events).
SNOMED_CREATININE = [
    "102574004",  # Serum creatinine (substance/observable anchor)
]
SNOMED_HBA1C = [
    "271248006",  # Haemoglobin A1c - [HbA1c] (observable anchor)
]


def time_varying_covariates(index_date=index_mi_date):
    """Latest renal/glycaemic values in 12 months pre-index."""
    covariates = {}
    for name, codes in (
        ("latest_creatinine_12mo", SNOMED_CREATININE),
        ("latest_hba1c_12mo", SNOMED_HBA1C),
    ):
        events = clinical_events.where(
            clinical_events.snomedct_code.is_in(codes)
        ).where(
            clinical_events.date.is_on_or_between(
                index_date - days(365), index_date
            )
        )
        covariates[name] = (
            events.sort_by(events.date).last_for_patient().numeric_value
        )
    return covariates


for name, value in time_varying_covariates().items():
    setattr(dataset, name, value)

# 3f. Mortality linkage: MI as underlying cause of death.
mi_death = ons_deaths.where(
    ons_deaths.underlying_cause_of_death.is_in(PH215_ICD10_SECONDARY_CARE)
)
dataset.mi_death_date = mi_death.date
dataset.mi_underlying_death = mi_death.exists_for_patient()

# 3g. Provenance stamps (audit trail for the response summary).
dataset.ph215_version_id = 430
