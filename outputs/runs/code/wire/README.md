# Waveform Integrated Research Environment (WIRE) — OpenSAFELY Cohort Scaffolding

## Project Overview
- **Project**: Waveform Integrated Research Environment (WIRE)
- **Institution**: NHS Research SDE Network
- **Lead**: Not specified
- **Description**: Captures high-frequency physiological waveform data from routine care linked to the health record
- **Cardiovascular relevance**: Strong — ECG/physiological waveforms are core cardiac signals

## Files
- `cohort_definition.py` — ehrQL dataset definition (cohort, index events, comorbidities, medications, time-varying covariates, outcomes)
- `codelists.json` — codelist inventory (candidate sets; see gap notes)

## Datasets Mapped
NHS England SDE waveform data

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
