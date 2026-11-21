# CARDINAL-HEALTH × PH215 Deep-Dive Project

This repository contains the output of a focused deep-dive analysis of the HDRS project **CARDINAL-HEALTH** (matched to **CARDINAL-DATA** in the HDRS tracking file) and its target phenotype **PH215 (Myocardial infarction)**. The analysis was performed using a sequence of MCP (Model Context Protocol) calls to gather project metadata, phenotype codelists, relevant datasets, and to generate OpenSAFELY-ready ehrQL cohort scaffolding.

## Table of Contents
- [Overview](#overview)
- [Artifacts](#artifacts)
- [Workflow Summary](#workflow-summary)
- [Using the OpenSAFELY Scaffolding](#using-the-opensafely-scaffolding)
- [References](#references)

## Overview

The goal of this deep-dive was to:
1. Map the project to BHF Data Science Centre services.
2. Identify UK-wide datasets suitable for MI research (population ≥60,000).
3. Exhaustively compile MI-specific codelists across all UK clinical terminologies.
4. Generate OpenSAFELY-ready ehrQL cohort scaffolding for MI case ascertainment.
5. Produce a complete, auditable deliverable package.

The analysis followed the sequential steps: HDRS → Phenotype Library → Gateway Dataset Search → OpenSAFELY Scaffolding.

## Artifacts

The full set of artifacts is located in the `outputs/runs_2026-11-19/` directory:

```
outputs/
└── runs_2026-11-19/
    ├── manifest.yaml
    ├── code/
    │   └── CARDINAL-HEALTH_PH215/
    │       ├── cohort_definition.py
    │       ├── codelists.json
    │       └── README.md
    └── response/
        └── 2026-11-19T14-43-18Z_CARDINAL-HEALTH_PH215_summary.md
```

- **manifest.yaml**: Metadata about the run (date, model used, user query, response summary, and list of artifacts).
- **code/CARDINAL-HEALTH_PH215/cohort_definition.py**: OpenSAFELY ehrQL cohort scaffolding for MI case ascertainment, implementing the PH215 phenotype's three ascertainment streams and additional covariates.
- **code/CARDINAL-HEALTH_PH215/codelists.json**: A JSON file containing 21 exhaustive MI codelists across 8 terminologies (ICD-10, ICD-9, SNOMED CT, Read v2, Med codes, OPCS-4, OXMIS, GPRD product) with full code lists and provenance.
- **code/CARDINAL-HEALTH_PH215/README.md**: Guidance on deploying the scaffolding in an OpenSAFELY study, including placeholders and BHF DSC service mapping.
- **response/2026-11-19T14-43-18Z_CARDINAL-HEALTH_PH215_summary.md**: A detailed, human-readable summary of the analysis, including:
  1. Project Profile (CARDINAL-HEALTH → CARDINAL-DATA)
  2. PH215 Specification (verbatim from Phenotype Library)
  3. Dataset Matches (table of datasets with population ≥60k and MI-relevant fields)
  4. MI Codelist Inventory (PH215 + supplements)
  5. Codelist Gap Analysis
  6. OpenSAFELY Scaffolding (file list and key function signatures)
  7. BHF DSC Service Mapping (project needs → exact service names → priority)
  8. Recommendations (next steps for the project team)

## Workflow Summary

A detailed workflow is available in [WORKFLOW.MD](./WORKFLOW.MD). The high-level steps are:

1. **HDRS Project Lookup**: Attempted to retrieve `CARDINAL-HEALTH`; when not found, searched by keyword "CARDINAL" and used the matched project (CARDINAL-DATA).
2. **Phenotype Library Extraction**: Retrieved PH215 and PH1778 details, then searched for all MI-related phenotypes.
3. **Codelist Consolidation**: Aggregated codelists from all MI-related phenotypes, creating an exhaustive inventory.
4. **Dataset Discovery**: Queried the HDR UK Gateway for datasets with MI-relevant fields and population ≥60,000.
5. **OpenSAFELY Scaffolding Generation**: Generated ehrQL code implementing the PH215 phenotype's ascertainment streams and required functions.
6. **Packaging & Validation**: Created the manifest, validated all artifacts, and produced the final summary.

## Using the OpenSAFELY Scaffolding

The ehrQL scaffolding in `code/CARDINAL-HEALTH_PH215/cohort_definition.py` is designed to be used as a starting point for an OpenSAFELY study. To use it:

1. **Replace placeholder codelists**: The scaffolding includes inline codelist samples for syntax validation. In a real study, replace these with codelists loaded from CSV files using `ehrql.codelist_from_csv`. The full codelist exports are in `codelists.json`.
2. **Adjust the index date logic**: The current `index_mi_date()` function uses the earliest primary-care MI on/after 1999-01-01 (PH215's evidence window start). Modify as needed for your study's index date definition.
3. **Wire in prior comorbidities and medications**: The functions `comorbidities_charlson()`, `meds_12mo_atc()`, and `time_varying_covariates()` contain placeholder codes. Replace these with the full codelists from `codelists.json` (or other sources) as appropriate for your study.
4. **Backend considerations**: The scaffolding uses the TPP backend (`ehrql.tables.tpp`). If targeting CPRD GOLD, adjust the table imports and codelist mappings (see the code's README for details).
5. **Run in OpenSAFELY**: Place the cohort definition in your study's `analysis/` directory, ensure the codelists are in `codelists/` and referenced in `codelists.txt`, then run with `opensafely run`.

For full deployment guidance, see `code/CARDINAL-HEALTH_PH215/README.md`.

## References

- BHF Data Science Centre Services Reference: [`bhf_reference/bhf_dsc_services_reference.md`](../bhf_reference/bhf_dsc_services_reference.md)
- Prompt used for this analysis: [`prompts/cardinal-health.md`](../prompts/cardinal-health.md)
- Detailed workflow: [WORKFLOW.MD](./WORKFLOW.MD)

## Contact

For questions about this analysis, please refer to the summary markdown or contact the analyst who generated this report.

---
*Generated on 2026-11-19 as part of the CARDINAL-HEALTH × PH215 deep-dive.*