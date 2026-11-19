# Project Iceberg — OpenSAFELY Cohort Scaffolding

## Project Overview
- **Project**: Project Iceberg
- **Institution**: NHS Research SDE Network
- **Lead**: Not specified
- **Description**: Reusable service turning unstructured clinical text into research-ready data with clinical review and provenance
- **Cardiovascular relevance**: Moderate — free-text phenotyping captures CVD presentations missed by coded data

## Files
- `cohort_definition.py` — ehrQL dataset definition (cohort, index events, comorbidities, medications, time-varying covariates, outcomes)
- `codelists.json` — codelist inventory (candidate sets; see gap notes)

## Datasets Mapped
NHS England SDE free-text records

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
