# OpenSAFELY ehrQL scaffolding — CARDINAL-DATA × PH215 (Myocardial infarction)

Generated: 2026-11-19 · Project: **CARDINAL-DATA** (HDRS) · Phenotype: **PH215 v430** (HDR UK Phenotype Library)

## Files

| File | Purpose |
|------|---------|
| `cohort_definition.py` | ehrQL cohort scaffold implementing PH215 v430's three ascertainment streams, recurrence, prior CVD profile, 12-month secondary-prevention medications, time-varying renal/glycaemic covariates, and mortality linkage. Syntax-validated offline; **not runnable end-to-end** without a study repo + backend credentials. |
| `codelists.json` | Complete code-level exports of **21 codelists across 8 terminologies** pulled from the HDR UK Phenotype Library (PhenotypeMCP) on 2026-11-19. `metadata.source` records the upstream API base; every page in this bundle cites its PH/concept IDs. |
| `README.md` | This file: provenance, deployment mapping, and known placeholders. |

## PH215 v430 — what the scaffold implements

`PH215 "Myocardial infarction"` (version 430) is the MODIFIED CALIBER MI algorithm. Its definition text names three evidence streams:

1. **Primary-care MI diagnosis** (`myo_infarct_gprd`, categories 1–7) — Read v2 concept **C1296** (70 codes) + Med-code view **C1297** (70 codes, each carrying its Read v2 cross-map in `attributes`).
2. **Secondary-care MI diagnosis** (`myo_infarct_hes`, categories 1/5/6/7) — ICD-10 concept **C1298**: `I21, I22, I23, I241, I252`.
3. **Coronary thrombolysis procedure** (`lysis_opcs`, category 2) — OPCS-4 supplement from **PH1024 C3172**.

CALIBER categories: 1 = history of MI · 2 = possible MI/uncertain date · 3 = STEMI · 4 = NSTEMI · 5 = acute MI not further specified · 6 = subsequent MI · 7 = complications of MI.

Reference publication: Kuan V. et al., *Lancet Digital Health* 2019; DOI `10.1016/S2589-7500(19)30012-3`.

## Codelists bundled (codelists.json)

| Terminology | Codelists (PH_concept) | Codes |
|---|---|---|
| Read v2 | PH215_C1296, PH613_C2019, PH1024_C3170, PH481_C1842 | 70 + 58 + 43 + 65 |
| Med (CPRD) | PH215_C1297 | 70 |
| ICD-10 | PH215_C1298, PH611_C2017, PH942_C2720, PH1024_C3171, PH1024_C3174, PH1722_C4198 | 5 + 21 + 5 + 1 + 3 + 2 |
| ICD-9 | PH612_C2018, PH1024_C3173 | 30 + 3 |
| SNOMED CT | PH1722_C4199, PH2794_C7238, PH942_C2721 | 119 + 154 + 75 |
| OPCS-4 | PH1024_C3172 | 2 |
| OXMIS | PH481_C1843 | 21 |
| GPRD product (CPRD) | PH495_C1860 (anticoag), PH496_C1861 (antiplat), PH622_C2030 (statins) | 76 + 45 + 104 |

**21 codelists · 8 terminologies** — every ID above is retrievable from `https://phenotypes.healthdatagateway.org/phenotypes/<PH>/version/<vid>/detail/` or the equivalent concept page.

## Deploying into a real OpenSAFELY study repo

1. **Codelists as CSVs.** OpenSAFELY loads codelists from `codelists/` CSVs listed in `codelists.txt` (or `analysis/codelists.py` importing `ehrql.codelist_from_csv`). Convert the `codelists.json` entries you need into CSVs (`code,description` columns) and add them to `codelists.txt`, e.g.:

   ````text
   https://www.opencodelists.org/codelist/...   # preferred: Opencodelists hosted definitions matched to the PH215/PH2794 IDs above
   ````

   Then load per the docs:

   ````python
   from ehrql import codelist_from_csv

   mi_snomed = codelist_from_csv(
       "codelists/mi_snomed.csv",
       column="code",
   )
   ````

2. **Backend mapping.** `cohort_definition.py` uses the TPP backend (`ehrql.tables.tpp`) because it exposes HES APC (`apcs`), emergency care (`emergency_care_attendances`), medications (`medications`), and mortality (`ons_deaths`). For **CPRD GOLD** (the backend PH215 was validated on), swap `tables.tpp` for the equivalent tables and the SNOMED codelists (PH1722/PH2794) for Read v2 (PH215_C1296) + Med codes (PH215_C1297) — all present in `codelists.json`.

3. **ICD-10 + APCS quirk.** APCS stores 3-character ICD-10 codes with an "X" suffix. The scaffold's `expand_icd10_for_apcs()` implements the documented expansion ([docs.opensafely.org/ehrql/how-to/codelists](https://docs.opensafely.org/ehrql/how-to/codelists/)).

4. **Known placeholders (wire-up TODOs in the code).**
   - `SECONDARY_PREVENTION_DMD` — token placeholder; resolve real dm+d concept IDs from `codelists.json` keys `PH495_C1860`, `PH496_C1861`, `PH622_C2030` (their exports are GPRD product codes; convert via the dm+d browser or use NHSD refsets in the study repo).
   - `COMORBIDITY_CODESETS` — anchor Read v2 stubs for angina / heart failure / stroke-TIA / PAD; replace with full condition codelists (e.g., OpenCodelists `chronic cardiac`/`anginal` definitions) before analysis.
   - `SNOMED_CREATININE` / `SNOMED_HBA1C` — observable anchors; on TPP prefer `clinical_events_ranges` with units or validated regional refsets for eGFR.
   - `mi_hes_events` / `mi_lysis_events` — use `contains()` against `all_diagnoses` / `all_procedures` as an approximation; production studies should match exact codes on the APCS diagnosis/procedure columns (prepared in `MI_ICD10_APCS` and `PH1024_OPCS4_AMI_PROCEDURES`).
   - PH1778 (chronic kidney disease) fetch via PhenotypeMCP returned **HTTP 401**; re-source its codelist before adding renal-comorbidity covariates (see response summary §Codelist Gap Analysis).

5. **Index-date logic.** `index_mi_date()` takes the earliest primary-care MI event on/after 1999-01-01 (PH215's evidence window start). PH215's own window ends 2016-07-01 (`event_date_range`). A production implementation should take the **minimum across streams** using `minimum_of` per ehrQL docs and re-run across relative time windows as needed (see ehrQL "multiple time periods" how-to). The other requirement-named builders — `prior_mi()`, `comorbidities_charlson()`, `meds_12mo_atc()`, `time_varying_covariates()` — all take the index date as a parameter so they can be re-pointed at any index definition.

## Tooling notes

- `cohort_definition.py` passes `python -m py_compile` (offline syntax check) and follows current ehrQL idioms (`create_dataset`, `sort_by().first/last_for_patient()`, `days()`, `is_in`, `exists_for_patient`, `define_population`). The `ehrql` package is installed inside OpenSAFELY runner images, not PyPI, so validation here is syntax-level.
- Imports resolve only within an OpenSAFELY runner; run `opensafely run run_ehrqlv2 ...` in the study repo after wiring codelists.
- Dummy-data generation (`opensafely run generate-dummy-data ...`) will exercise the definition end-to-end without a backend.

## Provenance / audit trail

- Phenotype Library exports: PhenotypeMCP `get_phenotype_detail` for PH215, PH481, PH495, PH496, PH611, PH612, PH613, PH622, PH942, PH1024, PH1722, PH2794 (2026-11-19).
- Concept codelist deep-dive: `get_concept_codelist` for C4199 (SNOMED) and C1296 (Read v2).
- Project record: HDRS MCP `search_projects(keyword="CARDINAL")` → CARDINAL-DATA (OneLondon SDE). "CARDINAL-DATA" returned no record.
- ehrQL syntax references: [how-to/codelists](https://docs.opensafely.org/ehrql/how-to/codelists/) (codelist_from_csv, APCS ICD-10 expansion), TPP schema tables (apcs, emergency_care_attendances, medications, ons_deaths, patients) from OpenSAFELY docs.
