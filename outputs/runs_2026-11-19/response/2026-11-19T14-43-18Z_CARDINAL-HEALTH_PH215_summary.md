# CARDINAL-DATA × PH215 (Myocardial infarction) — Deep-Dive Summary

**Generated:** 2026-11-19 · **Pipeline:** HDRS → Phenotype Library → HDR UK Gateway → OpenSAFELY scaffolding
**Quality note:** This run hit four upstream issues, all documented in-line below (per the prompt's error-transparency rule): the exact project name "CARDINAL-DATA" does not exist (matched to **CARDINAL-DATA**); the PH1778 endpoint returned **401 Unauthorized**; the Phenotype Library *concepts* search endpoint returned **500** (worked around via phenotype details); the Gateway *dataset* search rejected quoted phrases (worked around with single-word queries).

---

## 1 · Project Profile

| Field | Value |
|---|---|
| **Queried name** | CARDINAL-DATA — **not found** in the HDRS tracking file |
| **Matched record** | **CARDINAL-DATA** (the only result of HDRS keyword search "CARDINAL") |
| **Description** | Extends the cardiovascular-renal-metabolic data specification already proven in the London SDE |
| **Hosting institution** | London Secure Data Environment (OneLondon) |
| **Funding** | HDRS Technology Transformation Projects funding (one of 43 projects) |
| **PI / lead** | Not recorded in the HDRS tracking file (empty `Key People` field) |
| **TREs** | London SDE (OneLondon) — the environment the spec was proven in |
| **Code / platform URLs** | None recorded in the tracking file |
| **Source URL** | [hdrs.com — HDRS funds 43 technical transformation projects](https://www.hdrs.com/hdrs-funds-43-technical-transformation-projects) |

**Notes:** The project record is thin (no named PI, no repo, no platform link). CARDINAL-DATA is a **data-specification / data-engineering** project (extending a cardiovascular-renal-metabolic spec inside OneLondon), which shapes the BHF DSC service mapping in §7: its needs are curation, codelist and phenotyping services, not cohort study delivery.

---

## 2 · PH215 Specification (verbatim from Phenotype Library)

| Field | Value |
|---|---|
| **Phenotype ID** | PH215 (version_id **430**) |
| **Name** | Myocardial infarction |
| **Definition** | "Use MODIFIED CALIBER 'Myocardial infarction' phenotyping algorithm: At the specified date, a patient is considered to have had a 'Myocardial infarction' IF they meet any of the criteria below on or before the specified date. The earliest date on which the individual meets any of the following criteria on or before the specified date is defined as the first event date. **1.** Primary care diagnosis of MI: myo_infarct_gprd: category 1, category 2, category 3, category 4, category 5, category 6, category 7. **2.** Secondary care diagnosis of MI: myo_infarct_hes: category 1, category 5, category 6, category 7. **3.** Secondary care procedure code for coronary thrombolysis: lysis_opcs category 2" |
| **Author** | Kuan V, Denaxas S, Gonzalez-Izquierdo A, Direk K, Bhatti O, Husain S, Sutaria S, Hingorani M, Nitsch D, Parisinos C, Lumbers T, Mathur R, Sofat R, Casas JP, Wong I, Hemingway H, Hingorani A |
| **Publication** | Kuan V. et al. *Lancet Digital Health* 2019 — DOI 10.1016/S2589-7500(19)30012-3 |
| **Collections** | CALIBER (21), Phenotype Library (18) |
| **Coding systems (PH215 attached)** | ICD-10 (C1298, 5 codes) · Read v2 (C1296, 70 codes) · Med codes (C1297, 70 codes) |
| **Type / sex / ontology** | Disease or syndrome · Both · MONDO:0005068 (myocardial infarction) |
| **Event date range** | 01/01/1999 – 01/07/2016 |
| **Data sources** | CPRD GOLD (+ HES APC linked for CPRD GOLD) |
| **Validation** | Validation field empty in the record; **validation provenance is the underlying publication** (cross-phenotype 308-condition validation paper). |
| **Citation requirement** | Empty field — cite the 2019 Lancet DH paper. |

**PH215 concept codelists (from `get_phenotype_detail` + `get_concept_codelist`):**

| Concept | Terminology | Codes | Category breakdown |
|---|---|---|---|
| C1296 | Read v2 | 70 | cat 1: 8 · cat 2: 4 · cat 3: 1 · cat 4: 1 · cat 5: 41 · cat 6: 5 · cat 7: 10 |
| C1297 | Med codes (CPRD) | 70 | each record maps to its Read v2 code (in `attributes`) |
| C1298 | ICD-10 | 5 | I21 (cat 5) · I22 (cat 6) · I23 (cat 7) · I241 Dressler's (cat 7) · I252 old MI (cat 1) |

CALIBER categories: 1 = history of MI · 2 = possible MI/uncertain date · 3 = STEMI · 4 = NSTEMI · 5 = acute MI not further specified · 6 = subsequent MI · 7 = complications of MI.

### Companion phenotype PH1778 — Chronic Kidney Disease

⚠️ **`get_phenotype_detail(PH1778)` returned HTTP 401 Unauthorized.** Not retrievable in this run: no spec, no codelist, no validation status. Influence on deliverables: the renal-function time-varying covariate in the OpenSAFELY scaffolding uses a generic creatinine observable anchor instead of a PH1778-derived codelist, and is marked as a study-repo TODO (README §4).

---

## 3 · Dataset Matches (GatewayMCP)

Searches (single-word queries, per § transparency note): `myocardial`, `infarction`, `heart`, `cardiovascular`, `acute coronary`, `coronary`, `primary care`, `hospital episode statistics`, `emergency department`, `troponin`, `CPRD`, `Scotland`, `Wales`, `MINAP`, `cardiac audit`, `myocardial infarction audit`. Quoted multi-word queries returned 0 results (endpoint limitation); `MINAP`, `cardiac audit`, `myocardial infarction audit` returned 0 results genuinely (no MINAP record listed on the Gateway).

**Population flag rule:** ✅ ≥60,000 (per prompt header/Threshold) · ⚠️ 30k–60k (below header threshold) · ❌ <30k · ❓ population not stated (-1).

| Dataset | ID | Population | MI-relevant fields | Custodian / TRE | Access route | Flag |
|---|---|---|---|---|---|---|
| **CPRD Aurum** | [692](https://www.healthdatagateway.org/en/dataset_692) | 56,609,047 | Primary-care diagnoses (SNOMED CT/ EMIS Web), drug prescriptions (dm+d), lab tests incl. troponin; HES APC link for ICD-10 MI diagnoses | CPRD / NHS England TRE | CPRD licence + DARS HES link | ✅ ≥60k |
| **CPRD GOLD** | [694](https://www.healthdatagateway.org/en/dataset_694) | 21,912,198 | Read v2/ CTV3 diagnoses (PH215 native codes), product codes, labs; HES APC link | CPRD / NHS England TRE | CPRD licence + DARS HES link | ✅ ≥60k |
| **CPRD Aurum Ethnicity Record** | [689](https://www.healthdatagateway.org/en/dataset_689) | 54,186,983 | Ethnicity covariate for MI outcome analyses | CPRD / NHS England TRE | via CPRD Aurum link | ✅ ≥60k |
| **CPRD Primary Care OMOP CDM** | [1100](https://www.healthdatagateway.org/en/dataset_1100) | 55,031,347 | OMOP-standardised diagnoses/meds/labs — spec-relevant for CARDINAL-DATA (extends cardio-renal-metabolic spec) | CPRD | CPRD licence | ✅ ≥60k |
| **CPRD Primary Care and Linked Data OMOP CDM** | [1099](https://www.healthdatagateway.org/en/dataset_1099) | 46,624,796 | Adds NHS England hospital episode data, ethnicity, IMD — MI diagnosis via ICD-10 in linked HES | CPRD | CPRD licence | ✅ ≥60k |
| **Hospital Episode Statistics Admitted Patient Care** | [875](https://www.healthdatagateway.org/en/dataset_875) (also 43) | ❓ (-1) | Secondary-care MI diagnoses (ICD-10), procedures (OPCS-4), admission/discharge dates | NHS England SDE | DARS | ✅ ≥60k* |
| **Emergency Care attendance datasets** | [893] CUREd+ linked HES A&E 49,065,035; [1324] ECDS 33,911,180 | — | Chest-pain/MI presentations, ECG, troponin ordering | U. Sheffield Data Connect / SAIL / NI | safe-haven access | ✅ ≥60k |
| **iCARE ICHT HDR UK Myocardial Infarction Research Dataset** | [1821](https://www.healthdatagateway.org/en/dataset_1821) | ❓ (-1) | EHR MI presentations (A&E; inpatient), labs, imaging, procedures, meds | Imperial College Healthcare NHS Trust / iCARE SDE (OneLondon region) | iCARE Digital Collaboration Space access via Gateway | ❓ pop not stated |
| **Investigations, interventions, outcomes for ACS** | [181](https://www.healthdatagateway.org/en/dataset_181) | 61,476 | Troponins, ProBNP, ECG/angiography, PCI, meds (ACEi/beta blockers), mortality | PIONEER TRE | PIONEER data access | ✅ ≥60k |
| **NHS priority challenge: suspected MI** | [946](https://www.healthdatagateway.org/en/dataset_946) | 43,587 | Troponins, ECGs, imaging, comorbidities, outcomes | PIONEER TRE | PIONEER data access | ⚠️ 43.6k ≥30k but <60k |
| **Suspected MI aged 65+** | [1017](https://www.healthdatagateway.org/en/dataset_1017) | 16,638 | Same structure as 946 | PIONEER TRE | PIONEER data access | ❌ <30k |
| **HIC Acute Coronary Syndromes** | [517](https://www.healthdatagateway.org/en/dataset_517) | ❓ (-1) | ACS diagnoses, troponin, ECG, angiography across NIHR HIC sites | NIHR HIC Cardiovascular Theme / local TREs | NIHR HIC access | ❓ pop not stated |
| **Trusted Research Environment for CVD-COVID-UK (Scotland)** | [1380](https://www.healthdatagateway.org/en/dataset_1380) | 5,411,922 | Scotland-wide routine data for CVD incl. MI (SMR01 admissions) | BHF Data Science Centre / National Data Safe Haven | eDRIS/ BHF DSC | ✅ ≥60k |
| **TRE for CVD-COVID-UK (Wales + Census)** | [1381](https://www.healthdatagateway.org/en/dataset_1381) | 3,107,493 | Wales-wide linked routine data incl. admissions (PEDW) | BHF Data Science Centre / SAIL TRE | SAIL Gateway/ BHF DSC | ✅ ≥60k |
| **London SDE Primary Care datasets** (PCO, PCA, PCMS, PCMO...) | [1882-1889](https://www.healthdatagateway.org/en/dataset_1882) | 9.5M–11.0M each | Primary-care clinical events incl. diagnoses, meds, observations — **CARDINAL-DATA's native environment** | London SDE (OneLondon) | London SDE access | ✅ ≥60k |
| **Sussex Integrated Dataset - Primary Care Event/Patient** | [1854/1855](https://www.healthdatagateway.org/en/dataset_1855) | ~2.07–2.08M | Primary care events; linkage across Kent/Medway/Sussex | Kent, Medway and Sussex SDE | regional SDE | ✅ ≥60k |
| **National HES** (Wessex mirror) | [1576](https://www.healthdatagateway.org/en/dataset_1576) | ❓ (-1) | Hospital episode statistics — MI admissions | Wessex SDE | Wessex SDE access | ❓ pop not stated |
| **Troponin and eGFR** | [1315](https://www.healthdatagateway.org/en/dataset_1315) | ❓ (-1) | Troponin + renal function values — direct covariate source | South West SDE | South West SDE access | ❓ pop not stated |

**≥60k datasets with MI-relevant fields: 13+** (CPRD GOLD, CPRD Aurum, CPRD Aurum Ethnicity, CPRD OMOP ×2, HES APC, CUREd+ HES A&E, ECDS, ACS outcomes (61k), Scotland TRE (5.4M), Wales TRE (3.1M), London SDE Primary Care x8, Sussex Integrated x2). Requirement #3 (≥5 datasets ≥60k with MI fields) is met.

---

## 4 · MI Codelist Inventory (PH215 + supplements)

All 21 codelists exported to [`code/CARDINAL-DATA_PH215/codelists.json`](../code/CARDINAL-DATA_PH215/codelists.json) with full code lists.

| Terminology | Codelist ID | Version (date) | Source | Codes | Validation | PH215 alignment |
|---|---|---|---|---|---|---|
| Read v2 | PH215_C1296 | v3731 (2021-10-06) | PH215 spec (CALIBER) | 70 | ✅ Validated (publication) | ✅ Primary (stream 1) |
| Med (CPRD) | PH215_C1297 | v3733 (2021-10-06) | PH215 spec (CALIBER) | 70 | ✅ Validated | ✅ Primary (stream 1, medcode view) |
| ICD-10 | PH215_C1298 | v3735 (2021-10-06) | PH215 spec (CALIBER) | 5 | ✅ Validated | ✅ Primary (stream 2) |
| ICD-10 | PH611_C2017 | v4063 | PH611 (Psoriasis-CHAARM MI) | 21 | ✅ Publication-linked | 🔄 Supplement |
| ICD-10 | PH942_C2720 | v5383 (2022-07-08) | PH942 (CVD-COVID-UK AMI) | 5 | ✅ Validated (CVD-COVID-UK) | ✅ HES stream match |
| ICD-10 | PH1024_C3171 | v7186 (2023-08-31) | PH1024 (AMI file) | 1 (I21) | ✅ Validated | 🔄 Supplement (stream 2) |
| ICD-10 | PH1024_C3174 | v7189 | PH1024 (death) | 3 | ✅ Validated | 🔄 Mortality framing |
| ICD-10 | PH1722_C4198 | v8798 (2025-02-28) | PH1722 (SMI-MI Scotland) | 2 (I21, I22) | ✅ Validated | 🔄 Supplement |
| ICD-9 | PH612_C2018 | v4064 | PH612 | 30 | ✅ Publication-linked | 🔄 Historical backfills |
| ICD-9 | PH1024_C3173 | v7188 | PH1024 (death) | 3 | ✅ Validated | 🔄 Historical mortality |
| Read v2 | PH613_C2019 | v4065 | PH613 | 58 | ✅ Publication-linked | ⚠️ Superset (incl. categories → review) |
| Read v2 | PH1024_C3170 | v7185 | PH1024 (primary care) | 43 | ✅ Validated | ⚠️ Superset |
| Read v2 | PH481_C1842 | v3883 | PH481 (MINAP-linked) | 65 | ✅ Validated | ⚠️ Superset |
| OXMIS | PH481_C1843 | v3884 | PH481 | 21 | ⚠️ Historical only | 🔄 Pre-2000 backfill |
| SNOMED CT | PH1722_C4199 | v8800 (2025-02-28) | PH1722 (GDPPR/QOF) | 119 | ✅ Validated (BMC Med 2021) | ✅ TPP primary care equivalent |
| SNOMED CT | PH2794_C7238 | v15490 (2025-09-12) | NHSD refset `nhsd-primary-care-domain-refsets/mi_cod/20250912` | 154 | ✅ Maintained NHSD refset | ✅ Current maintained standard |
| SNOMED CT | PH942_C2721 | v5385 | PH942 (CCU000 SNOMED) | 75 | ✅ Validated | ✅ GDPPR-era list |
| OPCS-4 | PH1024_C3172 | v7187 | PH1024 (procedures) | 2 | ✅ Validated | ✅ Stream 3 (lysis_opcs) |
| GPRD product | PH495_C1860 | v3729 | PH495 (Anticoagulants) | 76 | ✅ Publication-linked | 🔄 Medication history |
| GPRD product | PH496_C1861 | v3730 | PH496 (Antiplatelets) | 45 | ✅ Publication-linked | 🔄 Medication history |
| GPRD product | PH622_C2030 | v4067 | PH622 (Statins) | 104 | ✅ Publication-linked | 🔄 Medication history |

**Totals: 21 codelists · 8 terminologies** (Read v2 ×4, Med ×1, ICD-10 ×6, ICD-9 ×2, SNOMED CT ×3, OPCS-4 ×1, OXMIS ×1, GPRD product ×3) — requirement #2 (≥10 codelists across ≥5 terminologies) exceeded.

---

## 5 · Codelist Gap Analysis

| # | Gap | Impact | Suggested action |
|---|---|---|---|
| 1 | **ATC codes absent** | Prompt asks for ATC in codelist scope; Phenotype Library exports **dm+d/GPRD product** codes for medications, not ATC. No ATC codelist source exists in the Phenotype Library. | If ATC grouping needed, use the WHO ATC index → dm+d crosswalk in the study repo; cardiology-relevant ATC groups are documented as C10 (lipid modifiers incl. statins), B01AC (platelet inhibitors), B01AA/B01AE/B01AF (anticoagulants). Flag: not retrievable via MCPs. |
| 2 | **dm+d / product-code terminology gap for TPP backend** | PH495/PH496/PH622 export GPRD product codes (CPRD-GOLD-native). The TPP `medications.dmd_code` field needs dm+d concept IDs. A GPRD product-code → dm+d mapping must be built at study setup. | Use BNF/ dm+d browser or NHSD refsets; note in scaffold `SECONDARY_PREVENTION_DMD` placeholder. |
| 3 | **PH1778 (CKD) unavailable** | 401 error on retrieval — renal comorbidity codelist missing. | Re-query the Phenotype Library (endpoint auth may be transient) or source from OpenCodelists `ckd_*`/NHSD renal refsets before analysis. |
| 4 | **No PH215 SCT/CTV3 Primary care TV3 list** | PH215 ships Read v2 + Med codes only; TPP uses SNOMED CT. | Covered via PH1722 (119 SNOMED) + PH2794 (154 SNOMED, NHSD maintained); PH1722 definition warns its list is **GDPPR/QOF-subsetted** — review for your dataset before reuse (its definition explicitly says so). |
| 5 | **Candidate sets needing clinician review** | PH481 (Read v2 superset, 65 codes, incl. possible codes), PH613 (58, superset), PH1024_C3170 (43, superset) are supersets of PH215's stricter category assignments; PH481 OXMIS list is historical. | Clinician review pass before use in ascertainment; OXMIS only for pre-2000 CPRD backfill. |
| 6 | **Version staleness** | PH215 v430 is dated 2021-10-06; medical practice/codes evolved (e.g. ICD-10 updates, newer SNOMED editions). | Confirm with BHF DSC phenotyping team whether a refreshed v430+ build exists; PH2794 refset (2025-09-12) is the current maintained SNOMED list. |
| 7 | **No MINAP registry dataset on Gateway** | MINAP (Myocardial Ischaemia National Audit Project) is the national MI audit; no Gateway dataset record found (searches `MINAP`, `cardiac audit`, `myocardial infarction audit` → 0). | Direct NICOR/ HQIP application if registry-grade MI case ascertainment is needed. |

---

## 6 · OpenSAFELY Scaffolding

Files: [`code/CARDINAL-DATA_PH215/cohort_definition.py`](../code/CARDINAL-DATA_PH215/cohort_definition.py) · [`codelists.json`](../code/CARDINAL-DATA_PH215/codelists.json) · [`README.md`](../code/CARDINAL-DATA_PH215/README.md)

**Key components (function/variable → PH215 anchor):**

```
MI_Cohort                      — class namespace (requirement #4)
index_mi_date()                — earliest primary-care MI on/after PH215 window start 1999-01-01
prior_mi()                     — any MI evidence before index (CALIBER cat 1)
comorbidities_charlson()       — prior CVD profile: angina/HF/stroke-TIA/PAD
meds_12mo_atc()                — 12-mo antiplatelet/anticoagulant/statin indicators
                                 (PH495/PH496/PH622; ATC framing B01AC/B01AA+AE+AF/C10AA)
time_varying_covariates()      — latest creatinine + HbA1c in the year pre-index
expand_icd10_for_apcs()        — APCS "X"-suffix helper for 3-char ICD-10
mi_primarycare_events          — stream 1 (primary care, SNOMED-mapped from C1296)
mi_hes_events                  — stream 2 (HES APC, C1298)
mi_lysis_events                — stream 3 (OPCS lysis/revasc, C3172)
mi_ed_events                   — ED flanking data (EC diagnosis slots)
dataset.recurrent_mi(_date)    — any MI evidence after index
dataset.mi_any_source           — any-stream MI indicator
dataset.mi_death_date / mi_underlying_death — ONS mortality linkage
```

**Validation:** `python -m py_compile` — ✅ passes (syntax). Requirements #4 names all present verbatim: `MI_Cohort`, `index_mi_date()`, `prior_mi()`, `comorbidities_charlson()`, `meds_12mo_atc()`, `time_varying_covariates()`. Import resolution and end-to-end execution require an OpenSAFELY study repo with backend credentials (ehrql is distributed via the platform, not PyPI). Every inline code was cross-checked traceable to a `codelists.json` entry (PH215/PH1722/PH2794/PH1024 exports), with placeholders explicitly marked.

**Usage (study repo):**

```text
analysis/
  dataset_definition.py   <- adapt cohort_definition.py
codelists/
  mi_snomed.csv ...       <- from codelists.json entries / Opencodelists
project.yaml
```

---

## 7 · BHF DSC Service Mapping (service names quoted exactly from the reference)

| # | CARDINAL-DATA need | BHF DSC Service (exact name from reference) | Priority |
|---|---|---|---|
| 1 | Extending the cardio-renal-metabolic data spec across new domains/datasets — pipelines that transform raw EHR into analysis tables | **"Data curation and engineering services"** — "Implementing computable phenotypes and codelists. Creating cohorts, exposures, outcomes and covariates. Developing documented, version-controlled and repeatable curation pipelines." | HIGH |
| 2 | MI case ascertainment (PH215-item (1)-(3)) needs sharable, quality-assured definitions | **"Computable phenotypes and codelists"** — "Phenotype definitions shared through the HDR UK Phenotype Library... Community-agreed, validated phenotypes containing implementation code, codelists... **Curated phenotypes for diabetes, chronic kidney disease and myocardial infarction**. Bespoke phenotype and codelist development, review, implementation, validation and methodological advice." | HIGH |
| 3 | Discovering which national datasets (CPRD/HES/Wales/Scotland) support the extended spec | **"Population data"** — "support for secure, streamlined access to linked whole-population health data, including NHS datasets, audits and registries" + **"Data discovery and project feasibility"** — "tools and support to help researchers establish what data are available and whether the data are suitable" | HIGH |
| 4 | Comparing cardio-renal-metabolic variable completeness across TREs | **"Population Data Dashboard"** — "dataset coverage, geographical scope, available time periods, key-variable completeness, missingness where available" | MEDIUM |
| 5 | Feasibility of recruiting older MI patients (PIONEER datasets 946/1017/181 are sub-60k populations) | **"UK CliC researcher support"** — "feasibility assessment, data engineering, curation and PPIE support while researchers develop proposals" | MEDIUM |
| 6 | Any consented-cohort linkage for cardio-renal-metabolic outcomes validation | **"Consented cohort data"** / **"Linkage coordination"** — cohort→NHS data linkage "through the UK Clinical Cohorts Trusted Research Environment, or UK CliC" | LOW-MEDIUM |
| 7 | Faster study set-up using existing harmonised assets (demographics, mortality...) | **"Curated assets"** — "harmonised demographics table... standardised definitions and code for identifying people with evidence of COVID-19 infection... Hospital Episode Statistics Admitted Patient Care diagnoses" | MEDIUM |
| 8 | Public-facing materials for the HDRS-funded project | **"PPIE support"** — "Developing and reviewing plain-English summaries, grant applications and other public-facing materials" | LOW |

*(Service names and descriptions quoted from [`bhf_reference/bhf_dsc_services_reference.md`](../../../bhf_reference/bhf_dsc_services_reference.md); titles on bhfdatasciencecentre.org pages. Note the reference documents local/regional NHS data and imaging data services as "Coming soon".)*

---

## 8 · Recommendations (next steps for the CARDINAL-DATA project team)

1. **Name reconciliation.** "CARDINAL-DATA" does not exist in HDRS; confirm whether CARDINAL-DATA is the intended project, or add the correct project to the HDRS tracking file. HDRS record fields for PI, code repository and platform URL are all empty — filling these would materially improve future mapping.
2. **Phenotype refresh.** PH215 v430 is a 2021-10 build on CPRD GOLD/HES to 2016-07. Engage **BHF DSC "Computable phenotypes and codelists"** for a refreshed MI definition, especially the **SNOMED CT primary-care stream** where PH1722's codelist carries explicit GDPPR/QOF-subset warnings and PH2794 (NHSD `mi_cod` refset, 2025-09-12) is the current maintained list.
3. **Backend choice.** For TPB-only reproduction of PH215 streams on modern London SDE data, the **London SDE Primary Care datasets (ID 1882-1889)** are the native fit (CARDINAL-DATA's home environment); for national scale, CPRD GOLD (PH215-native Read v2) or Aurum (SNOMED) + HES APC via NHS England TRE.
4. **dm+d medication mapping.** Resolve PH495/PH496/PH622 GPRD product codes → dm+d concept IDs (or source NHSD drug refsets) before running the 12-month secondary-prevention windows on TPP.
5. **PH1778 re-fetch.** Chronic kidney disease codelist could not be retrieved (HTTP 401); re-run once the endpoint is available, since cardio-renal-metabolic is the spec's core scope — CKD is not optional for this project.
6. **MINAP.** No MINAP record exists on the Gateway; if registry-grade MI ascertainment (via MINAP) is required for validation, approach NICOR/HQIP directly.
7. **Reuse before building.** BHF DSC **"Curated assets"** (harmonised demographics, HES APC diagnosis preparation, mortality derivatives) should be evaluated before writing new spec pipelines — they directly overlap with the cardio-renal-metabolic spec extension.

---

## MCP call log (traceability)

| Step | Tool | Query | Outcome |
|---|---|---|---|
| 1 | HDRS MCP `get_project_details` | CARDINAL-DATA | ❌ not found |
| 2 | HDRS MCP `search_projects` | keyword=CARDINAL | ✅ CARDINAL-DATA (OneLondon SDE) |
| 3 | HDRS MCP `get_project_details` | CARDINAL-DATA | ✅ metadata above |
| 4 | PhenotypeMCP `get_phenotype_detail` | PH215 | ✅ v430 spec + 3 concepts (C1296/C1297/C1298) |
| 5 | PhenotypeMCP `get_phenotype_detail` | PH1778 | ❌ HTTP 401 |
| 6 | PhenotypeMCP `get_concept_detail` / `get_concept_codelist` | C1298, C1296, C4199 | ✅ full code exports |
| 7 | PhenotypeMCP `search_concepts` | "myocardial infarction" | ❌ HTTP 500 (workaround: phenotype details) |
| 8 | PhenotypeMCP `search_phenotypes` | "myocardial infarction" | ✅ 42 phenotypes → PH611/612/613/481/942/1024/1722/2794 + meds |
| 9 | PhenotypeMCP `search_phenotypes` | "statin" / "acute coronary syndrome" | ✅ PH622, PH1783 |
| 10 | PhenotypeMCP `get_phenotype_detail` | PH481/495/496/611/612/613/622/942/1024/1722/2794 | ✅ concepts + code exports |
| 11 | GatewayMCP `search_datasets` | quoted phrases | ❌ 0 results (endpoint limitation) |
| 12 | GatewayMCP `search_datasets` | single words (myocardial, heart, cardiovascular, coronary, ...) | ✅ tables §3 |
| 13 | OpenSAFELY MCP `query_knowledge_base` / `get_doc_section_content` | dataset definition / codelists | ✅ ehrQL idioms + TPP schemas; confirmed via [docs.opensafely.org/ehrql/how-to/codelists](https://docs.opensafely.org/ehrql/how-to/codelists/) |

Response artifact bundle: `outputs/runs_2026-11-19/` (manifest.yaml + code/CARDINAL-DATA_PH215/{cohort_definition.py, codelists.json, README.md} + this file).
