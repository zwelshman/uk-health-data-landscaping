# A Blueprint for Regional SDEs — OpenSAFELY Cohort Scaffolding

## Project Overview
- **Project**: A Blueprint for Regional SDEs
- **Institution**: Thames Valley and Surrey (TVS) SDE
- **Lead**: Not specified
- **Description**: Reference architecture and shared methodology from three regional SDEs
- **Cardiovascular relevance**: Indirect — infrastructure enabling regional CVD research

## Files
- `cohort_definition.py` — ehrQL dataset definition (cohort, index events, comorbidities, medications, time-varying covariates, outcomes)
- `codelists.json` — codelist inventory (candidate sets; see gap notes)

## Datasets Mapped
TVS SDE; regional SDEs

## BHF DSC Services Needed
- **Data curation and engineering**

## Usage
```bash
opensafely run ehrql:v1 --dataset-definition cohort_definition.py --output output.csv
```

## Caveats
- Codelists are candidate concept sets pending clinician review (Phenotype Library API unavailable during generation).
- ehrQL code targets v1.3+ API; verify against current OpenSAFELY docs before execution.
