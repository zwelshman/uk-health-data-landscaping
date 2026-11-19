# CARDINAL-HEALTH × PH215 — MI Cohort Scaffolding

OpenSAFELY-ready ehrQL cohort definition for **myocardial infarction (MI) case
ascertainment** using the **PH215 "Myocardial infarction"** phenotype
(HDR UK Phenotype Library, version 430, CALIBER-derived,
DOI [10.48533/8smg-ga13](https://doi.org/10.48533/8smg-ga13)).

## Project context

| Field | Value |
|---|---|
| Requested project | CARDINAL-HEALTH |
| HDRS tracker match | **CARDINAL-DATA** (nearest match; CARDINAL-HEALTH not in tracker) |
| Host institution | London Secure Data Environment (OneLondon) |
| Funding | HDRS Technology Transformation Projects funding (one of 43 projects) |
| Description | Extends the cardiovascular-renal-metabolic data specification already proven in the London SDE |
| Source | https://www.hdrs.com/hdrs-funds-43-technical-transformation-projects |

## Files

| File | Purpose |
|---|---|
| `cohort_definition.py` | ehrQL dataset definition (v1.3+) implementing PH215 logic |
| `codelists.json` | 22 MI codelists (1,988 codes) across 9 terminologies, all traceable to the HDR UK Phenotype Library |

## PH215 case ascertainment logic

The MODIFIED CALIBER algorithm defines MI via three criteria; the earliest
matching date is the first event date:

1. **Primary care diagnosis of MI** — `myo_infarct_gprd` categories 1–7
   (Read v2 concept C1296; CTV3/SNOMED supplements for TPP)
2. **Secondary care diagnosis of MI** — `myo_infarct_hes` categories 1, 5, 6, 7
   (ICD-10 concept C1298)
3. **Secondary care coronary thrombolysis procedure** — `lysis_opcs` category 2
   (OPCS-4 concept C3172 via PH1024)

## Key function signatures

```python
index_mi_date() -> Series[date]
    # Earliest MI event across primary care, HES APC diagnoses and OPCS-4 thrombolysis

prior_mi(index_date, min_gap_days=28) -> Series[date]
    # Most recent prior MI event; non-null => recurrent MI

comorbidities_charlson(index_date) -> dict[str, Series[bool]]
    # Charlson-weighted prior CVD comorbidities (10-year lookback)

meds_12mo_atc(index_date) -> dict[str, Series[bool]]
    # Antiplatelet / DOAC / warfarin / statin history in the 12 months pre-index

time_varying_covariates(index_date) -> dict[str, Series[float]]
    # Latest creatinine (eGFR proxy), HbA1c, systolic BP in the 12 months pre-index
```

## Usage

```bash
# In an OpenSAFELY project, place this file as analysis/cohort_definition.py
# and codelists.json codes as analysis/codelists/*.csv, then:

opensafely run ehrql:v1 generate-cohort analysis/cohort_definition.py
```

The `codelists` module referenced by `cohort_definition.py` should be
materialised from `codelists.json` (one CSV per codelist, `code` column),
or replaced with `codelist_from_csv()` imports per the OpenSAFELY
[codelists how-to](https://docs.opensafely.org/codelists/).

## Codelist traceability

Every codelist in `codelists.json` carries:

- `codelist_id` — Phenotype Library phenotype/concept/version identifiers
  (e.g. `PH215/C1296/v3731`)
- `source` — the exact Phenotype Library record it was extracted from
- `validation` — CALIBER / BHF DSC / OpenSAFELY / NHSD refset provenance
- `ph215_alignment` — how it maps to the PH215 algorithm criteria

## Known limitations

1. **CARDINAL-HEALTH is not in the HDRS tracker** — CARDINAL-DATA was used
   as the nearest match (documented per requirement #1).
2. **Phenotype Library search endpoints failed** (server-side
   `PaginatedResponse` errors on `search_phenotypes`/`search_concepts`);
   supplements were identified via collection-detail and
   phenotype-detail endpoints instead.
3. **`creatinine_codes`, `hba1c_codes`, `systolic_bp_codes`** referenced by
   `time_varying_covariates()` are placeholders pending extraction of the
   corresponding lab-value codelists from the Phenotype Library (they are
   not MI-specific and out of PH215 scope).
4. **ATC codes are not directly available** from the Phenotype Library;
   BNF codelists (PH1612/PH1597/PH1598) are provided with a documented
   BNF→dm+d→ATC mapping path.
5. ehrQL TPP schema fields (`apcs.all_diagnoses`, `all_procedures`,
   `clinical_events_ranges.numeric_value`) should be verified against the
   current schema version before execution.
