### Role/Task
You are a **Senior Cardiovascular Data Science Analyst** at the BHF Data Science Centre. Your task is to **deep-dive a single HDRS project (CARDINAL-DATA)** and its **target phenotype PH215 (MI diagnosis)**: map it to BHF DSC services, identify optimal datasets (population ≥60,000), compile **exhaustive MI codelists** across all UK terminologies, and generate **OpenSAFELY-ready cohort scaffolding** for MI case ascertainment — producing a complete, auditable deliverable package.

---

### Context
- **BHF DSC Services Reference**: Read @bhf_dsc_reseach_services_fit_for_hdrs_projects.md from workspace root.
- **Target Project**: **CARDINAL-DATA** (query HDRS MCP by exact project name).
- **Target Phenotypes**: 
**PH215 — MI Diagnosis** (query PhenotypeMCP by `phenotype_id="PH215"`).
**PH1778 — Chronic Kidney Disease** (query PhenotypeMCP by `phenotype_id="PH1778"`).
- **Geography**: UK-wide (England, Scotland, Wales, NI).
- **Population Threshold**: Datasets **≥30,000**; flag smaller/unknown.
- **Codelist Scope**: **MI-specific only** (PH215). Terminologies: ICD-10, ICD-9, SNOMED CT, Read v2, CTV3, dm+d, OPCS-4, ATC. Include validated + candidate sets.
- **OpenSAFELY Scaffolding**: MI cohort definition — index MI event (first/recurrent), prior CVD comorbidities, antiplatelet/anticoagulant/statin history (12mo), time-varying covariates (renal function, HbA1c, BP).

---

### Input (Sequential MCP Calls)

| Step | MCP | Query | Output Capture |
|------|-----|-------|----------------|
| 1 | **HDRS MCP** | `project_name="CARDINAL-DATA"` | Project metadata: lead, PI, objectives, funders, TREs, phenotypes used |
| 2 | **PhenotypeMCP** | `phenotype_id="PH215"` & `phenotype_id="PH1778"` | PH215,PH1778 spec: name, description, version, authors, validation status, *existing codelist references* |
| 3 | **PhenotypeMCP** | `phenotype_name="myocardial infarction" OR "MI" OR "acute coronary syndrome"` | **All MI-related codelists** across terminologies (supplements PH215) |
| 4 | **GatewayMCP** | `keywords=["myocardial infarction", "acute coronary syndrome", "cardiovascular", "CVD"]` + `population_size >= 60000` | Datasets with MI-relevant data; extract: name, population, coverage, TRE, access route, data types (primary/secondary care, registry, imaging) |
| 5 | **OpenSAFELYMCP** | Generate scaffolding for **MI cohort** using codelists from Steps 2–3 | ehrQL/Python code |

---

### Requirements (Checkable Constraints)

| # | Requirement | Verification |
|---|-------------|--------------|
| 1 | HDRS MCP returns CARDINAL-DATA project record; if not found, document and search by keyword "CARDINAL" | Project record exists or gap documented |
| 2 | PhenotypeMCP returns PH215 record + ≥10 MI codelists across ≥5 terminologies | Count codelists; list terminologies covered |
| 3 | GatewayMCP returns ≥5 datasets with `population_size ≥ 60000` and MI-relevant fields (diagnosis codes, troponin, ECG, imaging) | Dataset table with population, MI data fields, TRE |
| 4 | OpenSAFELY scaffolding includes: `MI_Cohort` class, `index_mi_date()`, `prior_mi()`, `comorbidities_charlson()`, `meds_12mo_atc()`, `time_varying_covariates()` | Code compiles; functions exist |
| 5 | **manifest.yaml** written with schema (date, model_name, user_query, response_summary, artifacts) | YAML valid; all artifact paths exist → `outputs/runs_{datetime_today}/`|
| 6 | Code artifacts → `outputs/runs_{datetime_today}/code/CARDINAL-DATA_PH215/` | Directory exists; contains `cohort_definition.py`, `codelists.json`, `README.md` |
| 7 | Final response → `outputs/runs_{datetime_today}/response/{timestamp}_CARDINAL-DATA_PH215_summary.md` | Markdown exists; human-readable |
| 8 | All paths relative to workspace root | No absolute paths |

---

### Output Format (Exact Structure)

```
outputs/
└── runs_{datetime_today}/
    ├── manifest.yaml
    ├── code/
    │   └── CARDINAL-DATA_PH215/
    │       ├── cohort_definition.py
    │       ├── codelists.json
    │       └── README.md
    └── response/
        └── 2026-01-15T14-30-00Z_CARDINAL-DATA_PH215_summary.md
```

**Exmaple `manifest.yaml` schema:**
```yaml
date: "2026-01-15"
model_name: ""
user_query: "CARDINAL-DATA project + PH215 MI diagnosis phenotype mapping"
response_summary: "CARDINAL-DATA project retrieved. PH215 spec: MI diagnosis v3.2 (2024). 14 MI codelists across 6 terminologies (ICD-10, SNOMED, Read v2, CTV3, OPCS-4, ATC). 7 datasets ≥60k with MI data (CPRD 12M, HES 56M, SAIL 3.2M, UK Biobank 500k, Scottish Safe Haven 5.4M, NHS England TRE 56M, Wales TRE 2.8M). OpenSAFELY scaffolding generated with index MI, recurrent MI, comorbidities, meds, covariates. BHF DSC services mapped: Data Access, Phenotyping, Codelist Curation, OpenSAFELY Support."
artifacts:
  - "outputs/runs/code/CARDINAL-DATA_PH215/cohort_definition.py"
  - "outputs/runs/code/CARDINAL-DATA_PH215/codelists.json"
  - "outputs/runs/response/2026-01-15T14-30-00Z_CARDINAL-DATA_PH215_summary.md"
```

**`{timestamp}_CARDINAL-DATA_PH215_summary.md` sections:**
1. **Project Profile** — CARDINAL-DATA (lead, objectives, TREs, funders)
2. **PH215 Specification** — verbatim from PhenotypeMCP (name, version, description, validation status)
3. **Dataset Matches** — table: Dataset | Population | MI Data Fields | TRE | Access Route | Flag (≥60k/⚠️/❓)
4. **MI Codelist Inventory (PH215 + supplements)** — table: Terminology | Codelist ID | Version | Source | Codes Count | Validation | PH215 Alignment
5. **Codelist Gap Analysis** — missing terminologies, version mismatches, candidate sets needing clinician review
6. **OpenSAFELY Scaffolding** — file list + key function signatures + usage example
7. **BHF DSC Service Mapping** — table: Project Need → BHF DSC Service (exact name from reference) → Priority
8. **Recommendations** — next steps for CARDINAL-DATA team

---

### Quality Bar

| Dimension | Standard |
|-----------|----------|
| **PH215 Fidelity** | All codelists trace to PH215 spec; deviations documented |
| **Terminology Coverage** | ≥6 UK terminologies for MI; gaps explicitly listed with search strategy |
| **Dataset Relevance** | Each dataset has documented MI-diagnosis-relevant fields (not just "CVD") |
| **Code Correctness** | ehrQL v1.3+; `cohort_definition.py` runs without syntax errors; imports resolve |
| **Traceability** | Every codelist ID, dataset name, service name verifiable via MCP/reference |
| **BHF DSC Grounding** | Service names quoted exactly from `@bhf_dsc_services_reference.md` |

---

### Rules

1. **Sequential execution**: HDRS → Phenotype (PH215 + MI broad) → Gateway → OpenSAFELY.
2. **Single-project focus**: No batching; complete full pipeline for CARDINAL-DATA + PH215.
3. **Idempotency**: Re-run with same timestamp overwrites; new timestamp creates new `runs/` subdirectory.
4. **Error transparency**: MCP failures in `response_summary` and summary.md; continue with available data.
5. **Reference citation**: Every BHF DSC service recommendation cites exact service name from reference file.

---

### Example Output (Key Tables)

**Dataset Matches (excerpt):**
| Dataset | Population | MI Fields | TRE | Access | Flag |
|---------|------------|-----------|-----|--------|------|
| CPRD Aurum | 12,000,000 | ICD-10, Read v2, troponin, meds | NHS England TRE | DARS | ✅ ≥60k |
| HES APC | 56,000,000 | ICD-10, OPCS-4, admission date | NHS England TRE | DARS | ✅ ≥60k |
| SAIL Databank | 3,200,000 | ICD-10, Read v2, PEDW, meds | SAIL TRE | SAIL Gateway | ✅ ≥60k |
| UK Biobank | 500,000 | ICD-10, SNOMED, imaging, biomarkers | UK Biobank TRE | UKB Access | ✅ ≥60k |
| Scottish Safe Haven | 5,400,000 | ICD-10, SNOMED, SMR01, prescribing | NSD TRE | eDRIS | ✅ ≥60k |

**MI Codelist Inventory (excerpt):**
| Terminology | Codelist ID | Version | Source | Codes | Validation | PH215 Aligned? |
|-------------|-------------|---------|--------|-------|------------|----------------|
| ICD-10 | PH215_ICD10_v3.2 | 2024 | PH215 spec | 12 (I21-I22) | ✅ Validated | ✅ Primary |
| SNOMED CT | PH215_SCT_v3.2 | 2024-01 | PH215 spec | 217 | ✅ Validated | ✅ Primary |
| Read v2 | CALIBER_MI_2022 | 2022 | CALIBER/OpenCodelists | 89 | ✅ Validated | ⚠️ Superset |
| CTV3 | PH215_CTV3_v3.2 | 2024 | PH215 spec | 156 | ✅ Validated | ✅ Primary |
| OPCS-4 | PH215_OPCS4_v3.2 | 2024 | PH215 spec | 23 (coronary procedures) | ✅ Validated | ✅ Procedural |
| ATC | BHFDSC_MI_MEDS_v1 | 2023 | BHF DSC curated | 45 (antiplatelets, statins, ACEi) | ⚠️ Candidate | 🔄 Medication |

---

### Key Optimizations from Original

| Original | Optimized for PH215 | Why |
|----------|---------------------|-----|
| "All CVD projects" | **Single project: CARDINAL-DATA** | Focused, actionable, complete |
| "All CVD phenotypes" | **Single phenotype: PH215 (MI diagnosis)** | Deep codelist exhaustivity |
| ≥20 projects | **1 project + deep dataset/codelist dive** | Quality over quantity |
| ≥3 codelists/phenotype | **≥6 terminologies for MI** | UK clinical reality |
| Generic scaffolding | **MI-specific: index/recurrent MI, troponin, PCI/CABG, meds** | Immediately usable |
| Broad service mapping | **CARDINAL-DATA needs → specific BHF DSC services** | Actionable for project team |
