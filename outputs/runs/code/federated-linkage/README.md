# Federated and Harmonised Multi-SDE Linkage — OpenSAFELY Cohort Scaffolding

## Project Overview
- **Project**: Federated and Harmonised Multi-SDE Linkage
- **Institution**: NHS Research SDE Network
- **Lead**: Not specified
- **Description**: Connects node software and harmonisation tooling into a shared coordinating layer across SDEs
- **Cardiovascular relevance**: Strong — UK-wide CVD comparisons require cross-SDE harmonisation

## Files
- `cohort_definition.py` — ehrQL dataset definition (cohort, index events, comorbidities, medications, time-varying covariates, outcomes)
- `codelists.json` — codelist inventory (candidate sets; see gap notes)

## Datasets Mapped
Multiple SDEs (England, Scotland, Wales)

## BHF DSC Services Needed
- **Data curation and engineering**
- **Curated assets**

## Usage
```bash
opensafely run ehrql:v1 --dataset-definition cohort_definition.py --output output.csv
```

## Caveats
- Codelists are candidate concept sets pending clinician review (Phenotype Library API unavailable during generation).
- ehrQL code targets v1.3+ API; verify against current OpenSAFELY docs before execution.
