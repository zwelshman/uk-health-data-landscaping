# Pathfinding on OpenSAFELY tools in the NHS England National SDE — OpenSAFELY Cohort Scaffolding

## Project Overview
- **Project**: Pathfinding on OpenSAFELY tools in the NHS England National SDE
- **Institution**: NHS England National SDE / OpenSAFELY (Bennett Institute, Oxford)
- **Lead**: Not specified
- **Description**: Tests whether OpenSAFELY ehrQL can prepare HES data for national SDE users
- **Cardiovascular relevance**: Strong — HES APC contains all CVD hospitalisations; ehrQL preparation directly applicable to CVD cohorts

## Files
- `cohort_definition.py` — ehrQL dataset definition (cohort, index events, comorbidities, medications, time-varying covariates, outcomes)
- `codelists.json` — codelist inventory (candidate sets; see gap notes)

## Datasets Mapped
NHS England SDE (HES)

## BHF DSC Services Needed
- **Data curation and engineering**
- **Curated assets (HES APC preparation)**

## Usage
```bash
opensafely run ehrql:v1 --dataset-definition cohort_definition.py --output output.csv
```

## Caveats
- Codelists are candidate concept sets pending clinician review (Phenotype Library API unavailable during generation).
- ehrQL code targets v1.3+ API; verify against current OpenSAFELY docs before execution.
