From the hdrsmcp what is the Making secondary care medicines data research-ready projects and what could the @bhf_dsc_services_reference.md do to help make it a success?

Only add `code` if necessary.

### Output Format (Exact Structure: only fill if necessary)
```
outputs/
└── runs_{datetime_today}/
    ├── manifest.yaml
    ├── code/
    │   └── {project_name}/
    │       ├── cohort_definition.py
    │       ├── codelists.json
    │       └── README.md
    └── response/
        └── 2026-01-15T14-30-00Z_{project_name}_summary.md
```

**Exmaple `manifest.yaml` schema:**
```yaml
date: ""
model_name: ""
user_query: ""
response_summary: ""
artifacts:
  - artifact_1
  - artifact_2
```