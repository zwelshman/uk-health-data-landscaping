# NHS DigiTrials Recruitment Connect — OpenSAFELY Cohort Scaffolding

## Project Overview
- **Project**: NHS DigiTrials Recruitment Connect
- **Institution**: NHS DigiTrials (NHS England)
- **Lead**: Multiple (Sasieni, Middleton, Manchanda)
- **Description**: Route for a regional SDE to pass an eligible cohort to DigiTrials for trial recruitment
- **Cardiovascular relevance**: Strong — CVD clinical trials (e.g., BEST4 cardiovascular outcomes) recruit via this route

## Files
- `cohort_definition.py` — ehrQL dataset definition (cohort, index events, comorbidities, medications, time-varying covariates, outcomes)
- `codelists.json` — codelist inventory (candidate sets; see gap notes)

## Datasets Mapped
NHS England SDE; regional SDEs

## BHF DSC Services Needed
- **Data access and linkage (Population data)**
- **Data discovery and project feasibility**

## Usage
```bash
opensafely run ehrql:v1 --dataset-definition cohort_definition.py --output output.csv
```

## Caveats
- Codelists are candidate concept sets pending clinician review (Phenotype Library API unavailable during generation).
- ehrQL code targets v1.3+ API; verify against current OpenSAFELY docs before execution.
