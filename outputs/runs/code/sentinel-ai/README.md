# SENTINEL-AI — OpenSAFELY Cohort Scaffolding

## Project Overview
- **Project**: SENTINEL-AI
- **Institution**: NHS Research SDE Network
- **Lead**: Not specified
- **Description**: Federated framework for continuous evaluation and post-market surveillance of clinical AI across three sentinel sites
- **Cardiovascular relevance**: Moderate — AI CVD tools (e.g., ECG interpretation) require phenotype validation

## Files
- `cohort_definition.py` — ehrQL dataset definition (cohort, index events, comorbidities, medications, time-varying covariates, outcomes)
- `codelists.json` — codelist inventory (candidate sets; see gap notes)

## Datasets Mapped
Three sentinel site SDEs

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
