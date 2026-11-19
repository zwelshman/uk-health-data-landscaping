# PRANA — OpenSAFELY Cohort Scaffolding

## Project Overview
- **Project**: PRANA
- **Institution**: Wessex SDE / University Hospital Southampton (CIRU)
- **Lead**: Not specified
- **Description**: Pre-hospital Research and Audit Network; ambulance, air ambulance and trauma data pipelines
- **Cardiovascular relevance**: Strong — pre-hospital cardiac arrest and stroke pathways

## Files
- `cohort_definition.py` — ehrQL dataset definition (cohort, index events, comorbidities, medications, time-varying covariates, outcomes)
- `codelists.json` — codelist inventory (candidate sets; see gap notes)

## Datasets Mapped
Wessex SDE; ambulance service data; NHS England HES

## BHF DSC Services Needed
- **Data curation and engineering**
- **Data access and linkage (Population data)**

## Usage
```bash
opensafely run ehrql:v1 --dataset-definition cohort_definition.py --output output.csv
```

## Caveats
- Codelists are candidate concept sets pending clinician review (Phenotype Library API unavailable during generation).
- ehrQL code targets v1.3+ API; verify against current OpenSAFELY docs before execution.
