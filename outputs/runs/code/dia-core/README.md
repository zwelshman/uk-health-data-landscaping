# DIA-core (Diabetes Driver) — OpenSAFELY Cohort Scaffolding

## Project Overview
- **Project**: DIA-core (Diabetes Driver)
- **Institution**: South West SDE / University of Exeter
- **Lead**: Dr John Dennis
- **Description**: Implements the UK diabetes core dataset (30 core variables) in a further SDE with open code
- **Cardiovascular relevance**: Strong — diabetes is a major cardiovascular risk factor; CVRM spectrum

## Files
- `cohort_definition.py` — ehrQL dataset definition (cohort, index events, comorbidities, medications, time-varying covariates, outcomes)
- `codelists.json` — codelist inventory (candidate sets; see gap notes)

## Datasets Mapped
South West SDE; UK Biobank; CPRD

## BHF DSC Services Needed
- **Data curation and engineering**
- **Curated assets**
- **Computable phenotypes and codelists**

## Usage
```bash
opensafely run ehrql:v1 --dataset-definition cohort_definition.py --output output.csv
```

## Caveats
- Codelists are candidate concept sets pending clinician review (Phenotype Library API unavailable during generation).
- ehrQL code targets v1.3+ API; verify against current OpenSAFELY docs before execution.
