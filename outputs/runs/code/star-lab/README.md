# STAR-Lab — OpenSAFELY Cohort Scaffolding

## Project Overview
- **Project**: STAR-Lab
- **Institution**: DataLoch (partners: RDS, DaSH, HIC, West of Scotland Safe Haven)
- **Lead**: Arlene Casey (PI), Kathy Harrison (Co-I)
- **Description**: LLM-based de-identification of pathology and microbiology free text across four Scottish Safe Havens
- **Cardiovascular relevance**: Indirect — pathology free-text includes cardiovascular specimens; de-identification enables CVD pathology research

## Files
- `cohort_definition.py` — ehrQL dataset definition (cohort, index events, comorbidities, medications, time-varying covariates, outcomes)
- `codelists.json` — codelist inventory (candidate sets; see gap notes)

## Datasets Mapped
Scottish Safe Havens (DataLoch, DaSH, HIC, WoSSH)

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
