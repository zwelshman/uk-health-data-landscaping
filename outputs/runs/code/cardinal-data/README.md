# CARDINAL-DATA — OpenSAFELY Cohort Scaffolding

## Project Overview
- **Project**: CARDINAL-DATA
- **Institution**: London Secure Data Environment (OneLondon)
- **Funding**: HDRS Technology Transformation Projects funding
- **Scope**: Extends the cardiovascular-renal-metabolic (CVRM) data specification already proven in the London SDE

## Files
- `cohort_definition.py` — ehrQL dataset definition (cohort, index events, comorbidities, medications, time-varying covariates, outcomes)
- `codelists.json` — candidate codelists for CVRM phenotypes (⚠️ all marked candidate; Phenotype Library API was unavailable)

## Datasets Mapped
| Dataset | Population | Status |
|---------|-----------|--------|
| UK Biobank | 500,000 | ✅ ≥60k |
| CPRD Aurum | ~60M registered | ✅ ≥60k |
| SAIL Databank | ~3.2M (Wales) | ✅ ≥60k |
| NHS England GPDPR | ~56M (England) | ✅ ≥60k |

## BHF DSC Services Needed
- **Computable phenotypes and codelists** — validated CVRM phenotype definitions (MI, HF, CKD, diabetes)
- **Data curation and engineering** — CVRM cohort/exposure/outcome construction
- **Curated assets** — harmonised demographics table, HES APC transformations

## Usage
```bash
opensafely run ehrql:v1 --dataset-definition cohort_definition.py --output output.csv
```

## Caveats
- Codelists are candidate concept sets pending clinician review (Phenotype Library API unavailable during generation).
- ehrQL code targets v1.3+ API; verify against current OpenSAFELY docs before execution.
