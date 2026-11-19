# Integrating OpenSAFELY tools into the South West SDE — OpenSAFELY Cohort Scaffolding

## Project Overview
- **Project**: Integrating OpenSAFELY tools into the South West SDE
- **Institution**: South West Secure Data Environment
- **Lead**: Henry Ireland (Programme Director)
- **Description**: Assesses adopting OpenSAFELY data management and federated analytics in a regional SDE
- **Cardiovascular relevance**: Strong — regional CVD cohort research via OpenSAFELY

## Files
- `cohort_definition.py` — ehrQL dataset definition (cohort, index events, comorbidities, medications, time-varying covariates, outcomes)
- `codelists.json` — codelist inventory (candidate sets; see gap notes)

## Datasets Mapped
South West SDE; NHS England SDE

## BHF DSC Services Needed
- **Data curation and engineering**
- **Computable phenotypes and codelists**

## Usage
```bash
opensafely run ehrql:v1 --dataset-definition cohort_definition.py --output output.csv
```

## Caveats
- Codelists are candidate concept sets pending clinician review (Phenotype Library API unavailable during generation).
- ehrQL code targets v1.3+ API; verify against current OpenSAFELY docs before execution.
