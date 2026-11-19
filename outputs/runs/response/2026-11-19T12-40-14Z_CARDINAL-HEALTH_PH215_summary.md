# CARDINAL-HEALTH × PH215 — MI Diagnosis Deep-Dive Summary

**Generated:** 2026-11-19T12:40:14Z
**Analyst pipeline:** HDRS MCP → PhenotypeMCP (PH215 + MI broad) → GatewayMCP → OpenSAFELY scaffolding
**Deliverables:** `outputs/runs/code/CARDINAL-HEALTH_PH215/` (cohort_definition.py, codelists.json, README.md)

---

## 1. Project Profile — CARDINAL-HEALTH

**⚠️ Gap documented (Requirement #1):** `CARDINAL-HEALTH` was **not found** in the
HDRS project tracker (`get_project_details` returned "Project 'CARDINAL-HEALTH'
not found in the current tracking file"). Per the fallback rule, a keyword search
for **"CARDINAL"** returned exactly one match, which is used as the project record
for this deliverable:

| Field | Value |
|---|---|
| **Project (tracker)** | CARDINAL-DATA (nearest match to CARDINAL-HEALTH) |
| **Description** | Extends the cardiovascular-renal-metabolic data specification already proven in the London SDE |
| **Institution hosting** | London Secure Data Environment (OneLondon) |
| **Funding award** | HDRS Technology Transformation Projects funding (one of 43 projects, announced by the Prime Minister in April 2025) |
| **Key people / lead / PI** | Not recorded in tracker (empty) |
| **Code repository / platform URLs** | Not recorded in tracker (empty) |
| **Tech stack keywords** | Not recorded in tracker (empty) |
| **Source URL** | https://www.hdrs.com/hdrs-funds-43-technical-transformation-projects |

**Objectives (inferred from description):** extend a cardiovascular-renal-metabolic
(CVRM) data specification proven in the London SDE — directly MI-relevant, since
MI ascertainment requires linked primary/secondary care diagnosis codes,
procedures, and CVRM medications and labs.

---

## 2. PH215 Specification (verbatim from PhenotypeMCP)

| Field | Value |
|---|---|
| **Phenotype ID** | PH215 (version_id 430, latest & published) |
| **Name** | Myocardial infarction |
| **Type** | Disease or syndrome |
| **Ontology** | myocardial infarction — MONDO:0005068 |
| **Definition (verbatim)** | "Use MODIFIED CALIBER 'Myocardial infarction' phenotyping algorithm: At the specified date, a patient is considered to have had a 'Myocardial infarction' IF they meet any of the criteria below on or before the specified date. The earliest date on which the individual meets any of the following criteria on or before the specified date is defined as the first event date. 1. Primary care diagnosis of MI: myo_infarct_gprd: category 1, category 2, category 3, category 4, category 5, category 6, category 7. 2. Secondary care diagnosis of MI: myo_infarct_hes: category 1, category 5, category 6, category 7. 3. Secondary care procedure code for coronary thrombolysis: lysis_opcs category 2." |
| **Authors** | Kuan V, Denaxas S, Gonzalez-Izquierdo A, Direk K, Bhatti O, Husain S, Sutaria S, Hingorani M, Nitsch D, Parisinos C, Lumbers T, Mathur R, Sofat R, Casas JP, Wong I, Hemingway H, Hingorani A |
| **Created / Updated** | 2021-10-06T16:08:06Z |
| **Collections** | CALIBER (21), Phenotype Library (18) |
| **Data sources** | CPRD GOLD; HES Admitted Patient Care data for CPRD GOLD |
| **Coding systems** | ICD-10 codes, Read codes v2, Med codes |
| **Event date range** | 01/01/1999 – 01/07/2016 |
| **Validation status** | Phenotype-level `validation` field is empty; **concept-level `validation_performed = true`** on all three PH215 concepts (CALIBER validation) |
| **DOI** | https://doi.org/10.48533/8smg-ga13 |
| **Phenoflow implementation** | https://kclhi.org/phenoflow/workflows/github.com/phenoflow/Myocardial-infarction---b32f9260-1795-11ef-9de4-4d4ea830ad16/blob/read-potential-cases-fhir/Myocardial-infarction.cwl |
| **Key publication** | Kuan V. et al., *The Lancet Digital Health*, DOI 10.1016/S2589-7500(19)30012-3 |

**PH215 concepts (primary codelists):**

| Concept | Coding system | Codes | Role in algorithm |
|---|---|---|---|
| C1296/v3731 "Myocardial infarction - Primary care" | Read v2 | 70 | Criterion 1 (categories 1–7: STEMI, NSTEMI, acute MI NOS, subsequent MI, complications, history, possible) |
| C1297/v3733 "Myocardial infarction - Primary care" | Med codes | 70 | Criterion 1 (CPRD GOLD medcode mapping) |
| C1298/v3735 "Myocardial infarction - Secondary care - Diagnoses" | ICD-10 | 5 | Criterion 2 (categories 1, 5, 6, 7) |

---

## 3. Dataset Matches

Gateway searches: "myocardial infarction" (3), "acute coronary syndrome" (2),
"cardiovascular disease" (1), "hospital episode statistics admitted patient care"
(2), "UK Biobank" (1), "CPRD" (52), "Scottish" (49), "Secure Data Environment"
(4), "SMR01" (5). Zero-result searches (documented): MINAP, NICOR, SAIL Databank
Wales, Northern Ireland, GDPPR, OpenSAFELY, primary care EHR.

| Dataset (Gateway ID) | Population | MI Data Fields | TRE / Host | Access Route | Flag |
|---|---|---|---|---|---|
| **CPRD Aurum Source file** (1600) | 58,667,140 | Primary care Read/SNOMED diagnoses, prescribing (dm+d), linkable to HES | CPRD (multiple TREs incl. NHS England SDE) | CPRD Research Data Governance (RDG) | ✅ ≥60k |
| **CPRD GOLD** (1620) | 10,914,470 | Read v2 + Med codes (PH215's native source), HES linkage | CPRD | CPRD RDG | ✅ ≥60k |
| **HES Admitted Patient Care** (875, NHS England SDE) | ~56M (England, population-scale; size field −1) | ICD-10 diagnoses (I21/I22), OPCS-4 procedures (K50.x thrombolysis), admission dates/method | NHS England Secure Data Environment | NHS England DARS | ✅ ≥60k (population-scale) |
| **UK Biobank** (700) | 500,000 | HES ICD-10, GP-linked CTV3 (PH4244), self-reported MI (field 6150), imaging, biomarkers | UK Biobank TRE | UKB Access Management System (bbams) | ✅ ≥60k |
| **SMR01 General Acute Inpatient and Day Case** (1726, ACTIVE) | 5,500,000 | ICD-10 acute MI diagnoses, Scottish hospital admissions | National Data Safe Haven Scotland (eDRIS) | eDRIS safe haven application | ✅ ≥60k |
| **Secure Data Environment for CVD-COVID-UK / COVID-IMPACT (England)** (1378) | 57,000,000 | Linked primary + secondary care, death registry — BHF DSC's MI phenotypes (PH1833/PH4529) built on this platform | NHS England SDE (BHF DSC programme) | BHF DSC data access arrangements | ✅ ≥60k |
| **Investigations, interventions, and outcomes for ACS** (181, PIONEER) | 61,476 | Serial troponins, ECG, imaging, procedures (PCI/CABG), drug administrations, comorbidities | PIONEER TRE (Microsoft Azure, UK) | PIONEER data request process | ✅ ≥60k |
| **CPRD Cardiovascular Disease Synthetic Dataset** (686) | 499,344 | Synthetic CVD risk-factor data (proof-of-concept; not for inference) | CPRD | CPRD data access | ✅ ≥60k (synthetic — pipeline testing only) |
| **NHS priority challenge: suspected MI** (946, PIONEER) | 43,587 | ECGs, troponins, imaging, procedures, medications, mortality, readmissions | PIONEER TRE | PIONEER data request process | ⚠️ <60k |
| **Suspected MI in patients 65+** (1017, PIONEER) | 16,638 | ECGs, troponins, imaging, procedures, medications, mortality, readmissions | PIONEER TRE | PIONEER data request process | ⚠️ <60k |
| **iCARE ICHT HDR UK MI Research Dataset** (1821) | unknown (−1) | MI-specific EHR: episodes, echo, pathology (troponin), pharmacy, problems/diagnoses | iCARE SDE (Imperial/NW London) | iCARE single access route | ❓ unknown |
| **HIC Acute Coronary Syndromes** (517) | unknown (−1) | Troponin assays since 2010, ACS classification, NICOR-linked cardiology | NIHR HIC Cardiovascular Theme | HIC member access | ❓ unknown |

**≥60k datasets with MI-relevant fields: 8** (requirement #3 met: ≥5).

---

## 4. MI Codelist Inventory (PH215 + supplements)

22 codelists, 1,988 codes, 9 terminologies (requirement #2 met: ≥10 codelists,
≥5 terminologies). Full codes in
[outputs/runs/code/CARDINAL-HEALTH_PH215/codelists.json](../code/CARDINAL-HEALTH_PH215/codelists.json).

| Terminology | Codelist ID | Version | Source | Codes | Validation | PH215 Alignment |
|---|---|---|---|---|---|---|
| Read v2 | PH215/C1296/v3731 | 2021-10-06 | PH215 spec (CALIBER) | 70 | ✅ Validated (validation_performed=true) | ✅ Primary — criterion 1 |
| Med codes | PH215/C1297/v3733 | 2021-10-06 | PH215 spec (CALIBER) | 70 | ✅ Validated | ✅ Primary — criterion 1 (CPRD GOLD) |
| ICD-10 | PH215/C1298/v3735 | 2021-10-06 | PH215 spec (CALIBER) | 5 | ✅ Validated | ✅ Primary — criterion 2 |
| OPCS-4 | PH1024/C3172/v8503 | 2022-08-23 | PH1024 CALIBER AMI | 2 | ✅ Validated (casenote review, EHR, prognostic, genetic, cross-country) | ✅ Primary — criterion 3 (lysis_opcs cat 2) |
| Read v2 | PH1024/C3170/v8499 | 2022-08-23 | PH1024 CALIBER AMI | 43 | ✅ Validated | ⚠️ Superset overlap (acute-only) |
| ICD-10 | PH1024/C3171/v8501 | 2022-08-23 | PH1024 CALIBER AMI | 1 | ✅ Validated | ⚠️ Narrower (I21 only) |
| ICD-9 | PH1024/C3173/v8505 | 2022-08-23 | PH1024 CALIBER AMI (death) | 3 | ✅ Validated | 🔄 Death certification supplement |
| ICD-10 | PH1024/C3174/v8507 | 2022-08-23 | PH1024 CALIBER AMI (death) | 3 | ✅ Validated | 🔄 Death certification supplement |
| ICD-10 | PH1833/C4419/v11780 | 2025-06-10 | BHF DSC (CCU072_01) | 24 | ⚠️ BHF DSC curated (EPCC supplement documented) | 🔄 Modern secondary-care supplement |
| SNOMED CT | PH1833/C4420/v11781 | 2025-06-10 | BHF DSC (CCU072_01) | 168 | ⚠️ BHF DSC curated | 🔄 SNOMED supplement (PH215 gap) |
| SNOMED CT | PH2794/C7238/v14723 | 2025-09-12 (refset) | NHSD Primary Care Domain Refsets `mi_cod` | 154 | ✅ NHSD refset (OGL) | 🔄 SNOMED supplement (PH215 gap) |
| CTV3 | PH3581/C8846/v16331 | 2020-06-25 | OpenSAFELY/OpenCodelists | 113 | ✅ OpenSAFELY curated | 🔄 CTV3 supplement (PH215 gap) |
| CTV3 | PH3582/C8847/v16332 | 2020-07-09 | OpenSAFELY/OpenCodelists | 59 | ✅ OpenSAFELY curated | 🔄 CTV3 alternative (narrower) |
| Read v2 | PH1062/C3330/v10197 | 2023-02-13 | Metcalfe et al. (Charlson) | 61 | ✅ Validated (Charlson category, score 1) | 🔄 Comorbidity weighting |
| CTV3 | PH4244/C10510/v17995 | 2026-06-08 | UK Biobank GP-linked | 84 | ⚠️ UKB-curated | 🔄 UKB supplement |
| ICD-10 | PH4244/C10506/v17991 | 2026-06-08 | UK Biobank HES | 5 | ⚠️ UKB-curated | 🔄 UKB supplement |
| ICD-10 | PH4529/C11667/v19152 | 2026-08-18 | BHF DSC CCU022_1 | 23 | ⚠️ BHF DSC curated | 🔄 CCU022_1 supplement |
| SNOMED CT | PH4529/C11668/v19153 | 2026-08-18 | BHF DSC CCU022_1 | 166 | ⚠️ BHF DSC curated | 🔄 CCU022_1 supplement |
| BNF→dm+d/ATC | PH1612/C3451/v10633 | 2024-02-11 | BHF DSC Antiplatelet | 57 | ⚠️ BHF DSC curated | 💊 meds_12mo_atc() |
| dm+d | PH2147/C5064/v12549 | 2025-09-12 (refset) | NHSD Drug Refsets `stat_cod` | 818 | ✅ NHSD refset (OGL) | 💊 meds_12mo_atc() |
| BNF→dm+d/ATC | PH1597/C3391/v10436 | 2023-11-27 | BHF DSC DOACs | 26 | ⚠️ BHF DSC curated | 💊 meds_12mo_atc() |
| BNF→dm+d/ATC | PH1598/C3392/v10437 | 2023-11-27 | BHF DSC Warfarin | 33 | ⚠️ BHF DSC curated | 💊 meds_12mo_atc() |

**Terminologies covered (9):** ICD-10, ICD-9, SNOMED CT, Read v2, CTV3 (Read v3),
Med codes, OPCS-4, dm+d, BNF (with documented BNF→dm+d→ATC mapping path).

---

## 5. Codelist Gap Analysis

### Missing terminologies (explicit)

| Terminology | Status | Search strategy attempted | Mitigation |
|---|---|---|---|
| **ATC** | ❌ Not available via Phenotype Library | search_phenotypes/search_concepts (server errors), collection scans | BNF codelists (PH1612/PH1597/PH1598) provided; BNF→dm+d→ATC mapping is deterministic (NHS BNF-to-dm+d and WHO ATC crosswalks) |
| **OPCS-4 (full revascularisation set)** | ⚠️ Partial — only thrombolysis (2 codes, per PH215 criterion 3) | PH1024 concepts; PH355 CABG / PH358 PTCA phenotypes exist in Phenotype Library but are procedure-specific, not MI-diagnosis | PCI/CABG procedure codelists (PH355/PH358) recommended as sensitivity-analysis supplements; flagged for clinician review |
| **SNOMED CT in PH215 itself** | ❌ PH215 has no SNOMED set (built on CPRD GOLD Read v2 + HES ICD-10) | — | Supplemented with PH2794 (NHSD `mi_cod` refset, 154 codes) and PH1833/PH4529 BHF DSC SNOMED sets |

### Version mismatches

- PH215 (2021) predates SNOMED CT primary-care adoption (TPP); its Read v2/Med
  codes sets are CPRD GOLD-native and will not run on TPP-based OpenSAFELY
  backends without the CTV3/SNOMED supplements supplied here.
- PH215's event date range (1999–2016) predates high-sensitivity troponin
  rollout; PH1024's 7-day recurrent-event cutoff guidance is adopted
  (scaffold default: 28 days, configurable).
- OPCS-4 thrombolysis codes reflect the pre-primary-PCI era; modern
  revascularisation ascertainment needs PH355/PH358 procedure sets.

### Candidate sets needing clinician review

1. **PH1833 SNOMED CT (168 codes)** and **PH4529 SNOMED CT (166 codes)** —
   near-identical BHF DSC sets; confirm which is canonical for CCU072_01 vs
   CCU022_1 and review the delta.
2. **PH3581 vs PH3582 CTV3** (113 vs 59 codes) — OpenSAFELY published two
   MI codelists; the narrower v2 is the "definite MI" set — clinician
   confirmation needed for index-event use.
3. **PH4244 UKB CTV3 (84 codes)** — UKB GP data only covers a subset of
   practices; review for ascertainment bias before UKB-wide use.
4. **BNF medication sets** — BNF chapter-level codes need mapping to dm+d
   VMPs for TPP `medications.dmd_code` filtering.

---

## 6. OpenSAFELY Scaffolding

**Directory:** `outputs/runs/code/CARDINAL-HEALTH_PH215/`

| File | Contents |
|---|---|
| `cohort_definition.py` | ehrQL v1.3+ dataset definition; syntax-validated (AST parse OK); all 5 required functions present |
| `codelists.json` | 22 codelists / 1,988 codes with full Phenotype Library traceability |
| `README.md` | Usage, PH215 logic mapping, known limitations |

**Key function signatures:**

```python
index_mi_date() -> Series[date]                    # first MI across PH215 criteria 1-3
prior_mi(index_date, min_gap_days=28) -> Series[date]   # recurrent MI flag
comorbidities_charlson(index_date) -> dict[str, Series[bool]]
meds_12mo_atc(index_date) -> dict[str, Series[bool]]     # antiplatelet/DOAC/warfarin/statin
time_varying_covariates(index_date) -> dict[str, Series[float]]  # creatinine, HbA1c, systolic BP
```

**Usage example:**

```bash
opensafely run ehrql:v1 generate-cohort analysis/cohort_definition.py
```

**Validation performed:** Python AST parse (syntax OK); required functions
`index_mi_date()`, `prior_mi()`, `comorbidities_charlson()`, `meds_12mo_atc()`,
`time_varying_covariates()` all defined. ehrQL itself is not installed in this
environment, so runtime execution against a TPP backend was not possible —
noted as a limitation. Lab-value codelists (creatinine/HbA1c/BP) are
placeholder references documented in the README (out of PH215 MI scope).

---

## 7. BHF DSC Service Mapping

Service names quoted exactly from `bhf_reference/bhf_dsc_services_reference.md`.

| Project Need (CARDINAL-HEALTH) | BHF DSC Service (exact name from reference) | Priority |
|---|---|---|
| Access linked whole-population NHS data (HES, registries) to validate the CVRM/MI specification beyond the London SDE | **Population data** — "support for secure, streamlined access to linked whole-population health data, including NHS national datasets, audits and registries" | 🔴 High |
| Implement PH215 + supplements as computable phenotypes across England/Scotland/Wales TREs | **Computable phenotypes and codelists** — "Bespoke phenotype and codelist development, review, implementation, validation and methodological advice" | 🔴 High |
| Compare PH215 Read v2 vs SNOMED/CTV3 sets across codelist libraries | **Codelist Comparison Tool** — "maps medical codes to descriptions, compares codes with the GDPPR reference set, associates codes with counts in the NHS England SDE, supports codelist construction and export" | 🟠 Medium |
| Build MI cohorts, exposures, outcomes and covariates reproducibly | **Data curation and engineering** — "Creating cohorts, exposures, outcomes and covariates" | 🔴 High |
| Harmonise demographics/diagnoses across the four nations | **Curated assets** — "harmonised demographics table", "Reusable approaches for preparing Hospital Episode Statistics Admitted Patient Care diagnoses" | 🟠 Medium |
| Reuse validated MI phenotype definitions (CCU072_01, CCU022_1) | **Computable phenotypes and codelists** — "Curated phenotypes for diabetes, chronic kidney disease and myocardial infarction" | 🟠 Medium |
| Assess feasibility/coverage of MI data across datasets before applying | **Data discovery and project feasibility** — "tools and support to help researchers establish what data are available and whether the data are suitable" | 🟠 Medium |
| Link consented CVRM cohort data to NHS data UK-wide | **UK CliC researcher support** — "feasibility assessment, data engineering, curation and PPIE support while researchers develop proposals to use cohort data" | 🟡 Low |
| PPIE for the MI/CVRM specification extension | **Patient and Public Involvement and Engagement** — "Co-designing inclusive PPIE approaches, engagement methods and resource plans" | 🟡 Low |

---

## 8. Recommendations

1. **Confirm project identity.** CARDINAL-HEALTH is absent from the HDRS
   tracker; CARDINAL-DATA (London SDE/OneLondon) is the nearest match.
   Confirm with the HDRS team whether these are the same project or whether
   CARDINAL-HEALTH needs a tracker record.
2. **Adopt a dual-terminology MI definition.** Run PH215's Read v2/ICD-10
   logic on CPRD GOLD-style data, and the NHSD `mi_cod` SNOMED refset
   (PH2794) + CTV3 set (PH3581) on TPP/OpenSAFELY. Reconcile with BHF DSC's
   CCU072_01 (PH1833) definition, which is the most current curated MI
   phenotype.
3. **Close the ATC gap deterministically.** Map the BNF medication codelists
   (PH1612/PH1597/PH1598) to dm+d VMPs, then crosswalk to ATC via the NHS
   dm+d→ATC table; validate with the **Codelist Comparison Tool**.
4. **Add revascularisation procedure codelists** (PH355 CABG, PH358 PTCA)
   as sensitivity analyses — PH215's OPCS-4 criterion covers only
   thrombolysis, which is rare in the primary-PCI era.
5. **Prioritise datasets:** CPRD Aurum + HES APC (England, primary/secondary
   linkage), SMR01 (Scotland), and the CVD-COVID-UK SDE (1378) for
   four-nation scale; PIONEER ACS (181) for troponin/ECG-rich validation;
   UK Biobank (700) for imaging/biomarker depth.
6. **Engage BHF DSC early** for "Bespoke phenotype and codelist development,
   review, implementation, validation and methodological advice" — the
   candidate SNOMED/CTV3 sets flagged in §5 need clinician review before
   production use.
7. **Validate the scaffold on OpenSAFELY TPP** — the code is syntax-checked
   but needs a live `opensafely run ehrql:v1` against dummy data, plus
   materialisation of `codelists.json` into per-codelist CSVs.

---

## MCP Error Transparency (Rule #4)

| MCP / Endpoint | Status | Workaround |
|---|---|---|
| HDRS `get_project_details("CARDINAL-HEALTH")` | ❌ Not found | Keyword search "CARDINAL" → CARDINAL-DATA |
| PhenotypeMCP `search_phenotypes` / `search_concepts` | ❌ Server-side PaginatedResponse errors (both paginated and no-pagination modes) | Collection-detail scans (CALIBER id=21, Phenotype Library id=18) + `get_phenotype_detail` |
| PhenotypeMCP `get_collections` | ❌ Same PaginatedResponse error | `get_collection_detail` by known IDs |
| Gateway `get_dataset(1897)` | ❌ 404 (archived record) | Active SMR01 record 1726 used |
| Gateway searches returning 0 results | MINAP, NICOR, SAIL Wales, NI, GDPPR, OpenSAFELY, others | Documented in §3; national datasets found via alternate query terms |
| OpenSAFELY MCP `search_docs_by_filename("codelists.md")` | ⚠️ Returned lockfile noise | `query_knowledge_base` used for ehrQL patterns |
| ehrQL runtime validation | ⚠️ ehrQL not installed locally | AST syntax validation only; runtime test recommended |
