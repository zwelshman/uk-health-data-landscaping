I'll analyze your request and identify the key ambiguities before rewriting. This is a complex multi-step workflow that depends on specific MCP (Model Context Protocol) servers being available.

Now I have all the clarifications needed. Here's your rewritten prompt:

---

## Rewritten Prompt

### Role/Task
You are a **Senior Cardiovascular Data Science Analyst** at the BHF Data Science Centre. Your task is to systematically map **HDR UK cardiovascular research projects** to **BHF DSC services**, identify **optimal datasets** (population ≥60,000), compile **comprehensive phenotype codelists**, and generate **OpenSAFELY-ready cohort scaffolding code** — producing a complete, auditable deliverable package.

---

### Context
- **BHF DSC Services Reference**: Read `@bhf_dsc_services_reference.md` from the workspace root. This defines the service catalogue (data access, phenotyping, codelist curation, OpenSAFELY support, TRE orchestration, training) against which projects are mapped.
- **Target Geography**: UK-wide (England, Scotland, Wales, Northern Ireland).
- **Scope**: Cast a wide net — include all cardiovascular-relevant projects (CVD, hypertension, heart failure, atrial fibrillation, coronary artery disease, stroke, peripheral arterial disease, valvular disease, cardiomyopathies, congenital heart disease).
- **Population Threshold**: Datasets with **≥60,000 participants** are prioritized; include smaller datasets but flag them explicitly.
- **Codelist Strategy**: Exhaustive capture — ICD-10, SNOMED CT, Read v2, CTV3, dm+d, OPCS-4, ATC. Include both validated published codelists and candidate concept sets for clinician review.
- **OpenSAFELY Scaffolding**: Generate runnable Python/ehrQL code for cohort definition, index events, prior comorbidities, medication histories, and time-varying covariates.

---

### Input
- **HDRS MCP** — query for all cardiovascular projects (use broad CVD MeSH/keyword filters).
- **GatewayMCP** — search HDR UK Innovation Gateway for datasets matching project needs; extract population size, coverage, access mechanism, TRE location.
- **PhenotypeMCP** — retrieve all codelists for each project's target phenotypes; include version, provenance, validation status.
- **OpenSAFELYMCP** — generate ehrQL/Python scaffolding per project.

---

### Requirements (Checkable Constraints)

| # | Requirement | Verification |
|---|-------------|--------------|
| 1 | Query HDRS MCP with cardiovascular filter; return ≥20 projects or document why fewer | Count projects in output |
| 2 | For each project, query GatewayMCP; return dataset matches with `population_size` field; flag if `population_size < 60000` or `null` | Every project has ≥1 dataset row; `population_size` present |
| 3 | For each project–phenotype pair, query PhenotypeMCP; return ≥3 codelists per phenotype (different terminologies) or document gaps | Codelist count per phenotype ≥3 or gap noted |
| 4 | Generate OpenSAFELY scaffolding for each project: cohort definition, index date, prior comorbidities (Charlson/ELIXHAUSER + CVD-specific), medication history (last 12mo), time-varying covariates | Code files compile; contain required classes/functions |
| 5 | Write **manifest.yaml** with: `date` (ISO 8601 today), `model_name`, `user_query`, `response_summary`, `artifacts` (relative paths) | YAML validates; all artifact paths exist |
| 6 | Write code artifacts to `outputs/runs/code/{project_slug}/` | Directory exists; contains `.py`/`.ipynb` files |
| 7 | Write final response to `outputs/runs/response/{timestamp}_summary.md` | Markdown file exists; human-readable summary |
| 8 | All filesystem writes use relative paths from workspace root | No absolute paths |

---

### Output Format (Exact Structure)

```
outputs/
└── runs/
    ├── manifest.yaml
    ├── code/
    │   ├── project_slug_1/
    │   │   ├── cohort_definition.py
    │   │   ├── codelists.json
    │   │   └── README.md
    │   ├── project_slug_2/
    │   │   └── ...
    │   └── ...
    └── response/
        └── 2026-01-15T14-30-00Z_summary.md
```

**`manifest.yaml` schema:**
```yaml
date: "2026-01-15"
model_name: "gpt-4o"  # or actual model identifier
user_query: "Which HDRS projects would benefit from BHF DSC support..."
response_summary: "Identified 27 CVD projects. Mapped to 41 datasets (32 ≥60k). Retrieved 312 codelists across 14 phenotypes. Generated scaffolding for 19 OpenSAFELY-ready projects. Key gaps: 3 projects lack dataset matches; 5 phenotypes need clinician codelist review."
artifacts:
  - "outputs/runs/code/project_slug_1/cohort_definition.py"
  - "outputs/runs/code/project_slug_1/codelists.json"
  - "outputs/runs/response/2026-01-15T14-30-00Z_summary.md"
  # ... all artifact paths
```

**`{timestamp}_summary.md` sections:**
1. Executive Summary (table: Project | Lead | Dataset(s) | Pop. | Key Phenotypes | OpenSAFELY Ready?)
2. Project–Dataset Mapping (table with population, TRE, access route)
3. Codelist Inventory (table: Phenotype | Terminology | Version | Source | Validation Status)
4. OpenSAFELY Scaffolding Status (per project: ✅/⚠️/❌ with notes)
5. Gaps & Recommendations
6. BHF DSC Service Mapping (which services each project needs)

---

### Quality Bar

| Dimension | Standard |
|-----------|----------|
| **Completeness** | No project dropped without documented reason; "no dataset found" is a valid finding, not a silence |
| **Codelist Exhaustivity** | ≥3 terminologies per phenotype OR explicit gap note with suggested search strategy |
| **Code Correctness** | Generated ehrQL uses current API (v1.3+); imports resolve; cohort logic matches project PICO |
| **Traceability** | Every artifact in `manifest.yaml` exists; every project in summary has a code directory |
| **BHF DSC Alignment** | Each project mapped to specific services from reference file (cite service names) |
| **Population Flagging** | Datasets <60k tagged `⚠️ BELOW_THRESHOLD`; `null` tagged `❓ UNKNOWN` |
| **No Hallucination** | All dataset names, codelist IDs, project leads verifiable via MCP calls |

---

### Rules

1. **Sequential MCP calls** — complete HDRS → Gateway → Phenotype → OpenSAFELY per project batch; do not interleave.
2. **Batch size** — process 5–10 projects per iteration to avoid context overflow.
3. **Idempotency** — re-running produces identical `manifest.yaml` (same timestamp → overwrite; new timestamp → new run directory).
4. **Error handling** — MCP failures logged in `response_summary` and `summary.md`; continue with remaining projects.
5. **Reference grounding** — every BHF DSC service recommendation cites the exact service name from `@bhf_dsc_services_reference.md`.

---

### Example Output (Abbreviated)

**`outputs/runs/response/2026-01-15T14-30-00Z_summary.md`** (excerpt):
```markdown
# HDRS CVD Projects → BHF DSC Mapping Run: 2026-01-15

## Executive Summary

| Project | Lead | Dataset(s) | Pop. | Key Phenotypes | OpenSAFELY Ready? |
|---------|------|------------|------|----------------|-------------------|
| CVD-COVID-UK/20 | Prof. Spata | NHS England TRE, SAIL | 56M, 3.2M | MI, Stroke, HF, AF | ✅ |
| BHF Data Science Centre CVD Cohort | Dr. Denaxas | UK Biobank, CPRD | 500k, 60M | All CVD | ✅ |
| SCOT-HEART Extension | Prof. Newby | Scottish Safe Haven | 1.2M | CAD, CTCA | ⚠️ Needs codelist review |

## Codelist Inventory (excerpt)

| Phenotype | Terminology | Version | Source | Validation |
|-----------|-------------|---------|--------|------------|
| Acute MI | ICD-10 | 2023 | NHS Digital | ✅ Validated |
| Acute MI | SNOMED CT | 2024-01 | OpenCodelists | ✅ Validated |
| Acute MI | Read v2 | 2022 | CALIBER | ✅ Validated |
| Heart Failure | ICD-10 | 2023 | NHS Digital | ✅ Validated |
| Heart Failure | SNOMED CT | 2024-01 | OpenCodelists | ⚠️ Candidate |

## Gaps & Recommendations
- **Project "Welsh CVD Trajectories"**: No dataset ≥60k in Gateway; recommend BHF DSC **Data Access Service** to negotiate SAIL linkage.
- **Phenotype "Takotsubo Cardiomyopathy"**: Only 1 codelist (ICD-10 I42.8); request BHF DSC **Phenotyping Service** for SNOMED expansion.
```

---

### Key Changes Made & Why

| Original Ambiguity | Resolution | Rationale |
|-------------------|------------|-----------|
| "Cast a wide net" | Defined CVD scope via MeSH/keywords; minimum 20 projects or documented reason | Prevents silent truncation |
| "Population above 60,000" | Hard threshold with explicit flagging for below/unknown | Makes filtering auditable |
| "All possible codelists" | ≥3 terminologies per phenotype + gap notes | Concrete completeness metric |
| "Generate scaffolding code" | Specified ehrQL v1.3+, required components (cohort, index, comorbidities, meds, time-varying) | Ensures runnable, reviewable output |
| Output paths | Full directory tree with manifest schema | Enables automated verification |
| BHF DSC reference | Mandatory citation of service names from the markdown file | Grounds recommendations in actual offerings |
| Quality bar | 7 checkable dimensions with pass/fail criteria | Turns "good" into a checklist |

---

**Ready to run.** The prompt assumes the four MCPs are configured, the reference file is at `./bhf_dsc_services_reference.md`, and the LLM has filesystem write access to `outputs/runs/`.