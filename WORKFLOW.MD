# CARDINAL-HEALTH × PH215 Deep-Dive Workflow

## Business Objective
Perform a focused, end-to-end deep-dive of a single HDRS project (CARDINAL-HEALTH) and its target phenotype PH215 (Myocardial Infarction) to:
- Map the project to BHF Data Science Centre services
- Identify UK-wide datasets suitable for MI research (population ≥60,000)
- Exhaustively compile MI-specific codelists across all UK clinical terminologies
- Generate OpenSAFELY-ready ehrQL cohort scaffolding for MI case ascertainment
- Produce a complete, auditable deliverable package

## Workflow Overview (Sequential Steps)

```mermaid
flowchart TD
    A[Start: HDRS MCP – Project Lookup] --> B{HDRS record found?}
    B -- Yes --> C[Extract CARDINAL-HEALTH metadata]
    B -- No --> D[Search HDRS by keyword "CARDINAL"]
    D --> E[Use matched project (e.g., CARDINAL-DATA)]
    C --> E
    E --> F[PhenotypeMCP – Get PH215 & PH1778 details]
    F --> G[PhenotypeMCP – Search MI-related phenotypes]
    G --> H[GatewayMCP – Dataset search (MI/CVD keywords + pop ≥60k)]
    H --> I[OpenSAFELY MCP – Generate ehrQL scaffolding]
    I --> J[Assemble artifacts: manifest, code, README, summary]
    J --> K[End: Validate & package outputs]
```

## Detailed Steps & Deliverables

### 1. HDRS Project Lookup
- **Input**: Project name `"CARDINAL-HEALTH"`
- **Action**: 
  - Try exact match via `get_project_details`
  - If not found, search by keyword `"CARDINAL"` via `search_projects`
- **Output**: Project metadata (lead, PI, objectives, funders, TREs, phenotypes used)  
  - *If not found*: Document gap and proceed with best match.
- **Deliverable**: Project profile (used in Summary §1)

### 2. Phenotype Library Extraction
- **Input**: Phenotype IDs `"PH215"` and `"PH1778"`
- **Action**: 
  - Retrieve full phenotype details via `get_phenotype_detail`
  - Capture name, description, version, authors, validation, existing codelist references
- **Additional Action**: 
  - Broaden search for MI-related phenotypes via `search_phenotypes` with query `"myocardial infarction" OR "MI" OR "acute coronary syndrome"`
- **Output**: 
  - PH215 specification (verbatim) – Summary §2
  - List of supplemental MI phenotypes and their codelists
- **Deliverable**: PH215 spec table + supplemental phenotype list

### 3. Codelist Consolidation
- **Input**: All MI-related phenotypes from Step 2
- **Action**: 
  - For each phenotype, retrieve its concept codelists via `get_concept_codelist` (where available)
  - Aggregate codes by terminology (ICD-10, ICD-9, SNOMED CT, Read v2, CTV3, Med codes, OPCS-4, OXMIS, GPRD product, ATC)
  - Deduplicate and retain source provenance (phenotype ID, concept ID, version)
- **Output**: 
  - Master codelist inventory (JSON) – `codelists.json`
  - Summary tables: 
    - Codelist inventory (Summary §4) 
    - Gap analysis (Summary §5)
- **Deliverable**: Exhaustive MI codelist bundle (≥10 codelists across ≥5 terminologies)

### 4. Dataset Discovery (GatewayMCP)
- **Input**: Keywords `[\"myocardial infarction\", \"acute coronary syndrome\", \"cardiovascular\", \"CVD\"]` + filter `population_size ≥ 60000`
- **Action**: 
  - Execute `search_datasets` for each keyword (single-word due to quoted‑phrase limitation)
  - Collect results: dataset ID, name, population, custodian, TRE, access route, MI‑relevant fields (diagnosis codes, troponin, ECG, imaging, procedures, medications)
- **Output**: 
  - Dataset table (Summary §3) with population flag (≥60k ✅, 30‑60k ⚠️, <30k ❌, unknown ❓)
- **Deliverable**: List of ≥5 qualifying datasets with MI‑relevant fields

### 5. OpenSAFELY EhrQL Scaffolding Generation
- **Input**: Curated codelist inventory (from Step 3) and dataset insights (Step 4)
- **Action**: 
  - Write ehrQL dataset definition (`cohort_definition.py`) implementing:
    - PH215’s three ascertainment streams (primary care, secondary care, procedure)
    - Index MI date (`index_mi_date()`)
    - Recurrent MI flag
    - Prior CVD comorbidity profile (`comorbidities_charlson()`)
    - 12‑month secondary‑prevention medication history (`meds_12mo_atc()`)
    - Time‑varying covariates (renal function, HbA1c) (`time_varying_covariates()`)
    - Mortality linkage (underlying cause of death)
  - Ensure required function/class names exist: `MI_Cohort`, `index_mi_date()`, `prior_mi()`, `comorbidities_charlson()`, `meds_12mo_atc()`, `time_varying_covariates()`
  - Add inline codelist samples (traceable to `codelists.json`) for syntax validation
  - Generate `README.md` with deployment guidance, placeholders, and BHF DSC service mapping
- **Output**: 
  - Syntactically valid Python module (passes `py_compile`)
  - Complete artifact bundle under `outputs/runs_<YYYY-MM-DD>/code/CARDINAL-HEALTH_PH215/`
- **Deliverable**: OpenSAFELY-ready cohort scaffolding

### 6. Packaging & Validation
- **Action**: 
  - Create `manifest.yaml` with schema:
    ```yaml
    date: "<today>"
    model_name: "<LLM used>"
    user_query: "<original prompt>"
    response_summary: "<concise narrative of outcomes>"
    artifacts:
      - "<relative path to cohort_definition.py>"
      - "<relative path to codelists.json>"
      - "<relative path to README.md>"
      - "<relative path to summary markdown>"
    ```
  - Verify all artifact paths are relative and exist
  - Confirm summary markdown includes all 8 required sections
- **Deliverable**: 
  - `manifest.yaml`
  - Final summary markdown (`response/<timestamp>_CARDINAL-HEALTH_PH215_summary.md`)

## Key Outputs (Artifact Bundle)

```
outputs/
└── runs_<YYYY-MM-DD>/
    ├── manifest.yaml
    ├── code/
    │   └── CARDINAL-HEALTH_PH215/
    │       ├── cohort_definition.py
    │       ├── codelists.json
    │       └── README.md
    └── response/
        └── <timestamp>_CARDINAL-HEALTH_PH215_summary.md
```

## Decision Points & Error Handling
- **Project not found**: Switch to keyword search; document gap.
- **PhenotypeMCP 401/500 errors**: Continue with available data; note in transparency log.
- **GatewayMCP quoted‑phrase limitation**: Use single‑word queries; document workaround.
- **Missing codelists/terminologies**: Flag in gap analysis; suggest clinician review or external sourcing.
- **Backend mismatch**: Clarify TPP vs CPRD GOLD mapping in README.

## Quality Gates
| Dimension | Target |
|-----------|--------|
| PH215 Fidelity | All codelists trace to PH215 spec; deviations documented |
| Terminology Coverage | ≥6 UK terminologies for MI; gaps listed |
| Dataset Relevance | Each dataset has MI‑specific fields (not just “CVD”) |
| Code Correctness | `ehrql` v1.3+ syntax; no import errors in scaffold |
| Traceability | Every codelist ID, dataset name, service name verifiable via MCP/reference |
| BHF DSC Grounding | Service names quoted exactly from reference file |

## Estimated Effort (Illustrative)
- HDRS lookup: 5 min
- Phenotype extraction: 10 min
- Codelist consolidation: 20 min
- Dataset discovery: 15 min
- Scaffold authoring: 25 min
- Packaging & validation: 10 min
- **Total**: ~85 min (sequential, no parallelism)

## Next Steps for Project Team
1. Confirm whether CARDINAL‑DELTA is the intended project; enrich HDRS record.
2. Engage BHF DSC “Computable phenotypes and codelists” for a refreshed MI definition (SNOMED‑CT primary‑care stream).
3. Resolve GPRD product → dm+d mapping for medication history.
4. Retrieve PH1778 (CKD) codelist once endpoint available.
5. Evaluate BHF DSC “Curated assets” before building new pipelines.
6. If registry‑grade MI ascertainment needed, pursue NICOR/HIQP for MINAP access.

---
*Workflow generated from the prompt execution on 2026-11-19.*