# Extending OMOP auto-mapping for Brain and Mental Health — OpenSAFELY Cohort Scaffolding

## Project Overview
- **Project**: Extending OMOP auto-mapping for Brain and Mental Health
- **Institution**: NHS Research SDE Network
- **Lead**: Not specified
- **Description**: Extends automated OMOP mapping from mental health into neurosciences
- **Cardiovascular relevance**: Indirect — OMOP mapping infrastructure applicable to CVD; stroke overlaps neurology

## Files
- `cohort_definition.py` — ehrQL dataset definition (cohort, index events, comorbidities, medications, time-varying covariates, outcomes)
- `codelists.json` — codelist inventory (candidate sets; see gap notes)

## Datasets Mapped
NHS England SDE

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
