# SCAMPI — OpenSAFELY Cohort Scaffolding

## Project Overview
- **Project**: SCAMPI
- **Institution**: Health Informatics Centre (HIC) with Scottish Safe Haven partners
- **Lead**: Not specified
- **Description**: Scalable architecture for medical image processing; open-source DICOM processing platform
- **Cardiovascular relevance**: Strong — cardiac imaging (CT coronary angiography, echocardiography) processing

## Files
- `cohort_definition.py` — ehrQL dataset definition (cohort, index events, comorbidities, medications, time-varying covariates, outcomes)
- `codelists.json` — codelist inventory (candidate sets; see gap notes)

## Datasets Mapped
Scottish Safe Haven imaging data

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
