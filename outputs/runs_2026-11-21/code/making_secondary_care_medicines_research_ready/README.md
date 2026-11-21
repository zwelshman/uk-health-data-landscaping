# Making Secondary Care Medicines Data Research-Ready

## Project Overview

**Project Name**: Making secondary care medicines data research-ready  
**Lead Organisation**: NHS England Secure Data Environment (SDE)  
**Partners**: 
- Professional Record Standards Body (PRSB)
- University of Liverpool
- Understanding Patient Data
- King's College Hospital NHS Foundation Trust

**Funding**: HDRS Technical Transformation Programme  
**Launch Date**: October 2026  
**Project URL**: https://theprsb.org/medsdataready

## Project Description

This project develops the **standards and tooling** to make **hospital prescribing and high-cost drugs data research-ready** across UK Secure Data Environments. The project addresses the critical need for standardised, accessible, and analysable secondary care medicines data for research purposes.

### Key Objectives

1. **Standards Development**: Create data standards for hospital prescribing data (ePMA), high-cost drugs (HCD), and systemic anti-cancer therapy (SACT)
2. **Tooling Creation**: Build reusable pipelines and tools for data extraction, transformation, and quality assurance
3. **Cross-Nation Harmonisation**: Enable consistent data access across England, Scotland, Wales, and Northern Ireland SDEs
4. **Research Readiness**: Transform complex secondary care medicines data into analysis-ready datasets

## Data Sources in Scope

- **Hospital Episode Statistics (HES)** - Admitted Patient Care, Outpatient, A&E
- **NHS England Secondary Uses Service (SUS)** data
- **Electronic Prescribing and Medicines Administration (ePMA)** systems
- **High Cost Drugs (HCD)** dataset
- **Systemic Anti-Cancer Therapy (SACT)** dataset
- **National Clinical Audit** datasets
- **Advanced Therapy Medicinal Products (ATMP)** registries

## Medicine Categories

- High-cost drugs (HCD)
- Systemic anti-cancer therapy (SACT)
- Biological therapies
- Advanced therapy medicinal products (ATMPs)
- Orphan drugs
- Hospital-only medicines
- Controlled drugs in secondary care

## BHF Data Science Centre Alignment

The BHF DSC services reference document outlines capabilities that directly support this project's success:

### 1. Data Curation and Engineering Services
- **Feasibility assessment** for secondary care medicines data across UK SDEs
- **Computable phenotype implementation** for medicine exposure/outcome definitions
- **Cohort, exposure, outcome, covariate creation** for medicines research
- **Documented, version-controlled, repeatable curation pipelines**
- **Cross-nation adaptation** for England, Scotland, Wales differences

### 2. Computable Phenotypes and Codelists
- **Phenotype library** with validated cardiovascular medicine phenotypes
- **Codelist Comparison Tool** for dm+d, SNOMED CT, BNF code mapping
- **Community-agreed, validated phenotypes** with implementation code
- **Lookup tables and terminology mapping** for medicines codes
- **FAIR sharing guidance** for phenotype definitions

### 3. Curated Assets
- **Harmonised HES APC diagnoses and procedures** - directly relevant for secondary care
- **Standardised mortality variables** - for medicine outcome studies
- **Reusable code components** for data preparation
- **Documentation and methodologies** for adaptation and reuse

### 4. Population Data Access
- **Population Data Dashboard** across NHS England SDE, Scotland Safe Haven, SAIL Wales
- **Dataset coverage, completeness, linkage opportunities** for medicines data
- **Cross-nation comparison** capabilities

### 5. Patient and Public Involvement (PPIE)
- **Co-design inclusive PPIE approaches** for medicines data research
- **Connect with lived-experience groups** for medication safety/effectiveness
- **Plain English summaries** for public-facing materials

### 6. UK CliC TRE Infrastructure
- **Consented cohort linkage** to routine NHS medicines data
- **Secure analysis environment** for linked cohort-medicines studies
- **SAIL Databank approval process** for data access

## Technical Approach

### Standards Development
- Leverage **PRSB standards** for clinical record structure
- Align with **dm+d (dictionary of medicines and devices)** for medicine coding
- Use **SNOMED CT** for clinical terminology
- Adopt **FHIR** standards for data exchange

### Tooling and Pipelines
- **Reproducible curation pipelines** (Python/R, version-controlled)
- **Quality assurance frameworks** for data completeness/accuracy
- **Automated codelist validation** against reference sets
- **Cross-SDE deployment** templates

### Governance and Ethics
- **Understanding Patient Data** partnership for public engagement
- **IG compliance** across all four UK nations
- **Safe researcher training** requirements
- **Output disclosure control** procedures

## Success Metrics

1. **Data Coverage**: % of secondary care medicines data available research-ready
2. **Standard Adoption**: Number of SDEs implementing project standards
3. **Research Usage**: Number of studies using research-ready medicines data
4. **Time Reduction**: Decrease in project setup time for medicines research
5. **Quality Improvement**: Consistency and completeness metrics
6. **Cross-Nation Studies**: Multi-nation medicines research enabled

## BHF DSC Service Integration Points

| Project Need | BHF DSC Service | Value Add |
|--------------|-----------------|-----------|
| Cardiovascular medicine phenotypes | Computable Phenotypes Library | Pre-validated CVD medicine codelists |
| Codelist development/validation | Codelist Comparison Tool | GDPPR reference, SDE counts, export |
| HES data preparation | Curated Assets (HES APC) | Harmonised diagnoses/procedures |
| Mortality outcomes | Curated Assets (Mortality) | Standardised death variables |
| Cross-nation data access | Population Data Dashboard | Coverage/completeness across UK |
| Pipeline development | Data Curation Engineering | Reusable, version-controlled pipelines |
| Public engagement | PPIE Service | Co-design, lived experience input |
| Cohort linkage | UK CliC TRE | Consented cohort + routine data linkage |

## Next Steps

1. **Engage BHF DSC** early for cardiovascular medicines focus
2. **Leverage existing phenotypes** from HDR UK Phenotype Library
3. **Use Codelist Comparison Tool** for dm+d/SNOMED validation
4. **Adopt curated HES assets** for secondary care diagnoses
5. **Plan PPIE strategy** with BHF DSC Public Advisory Group
6. **Design cross-nation pipelines** using Population Data Dashboard insights
7. **Explore UK CliC** for consented cohort linkage opportunities

## References

- Project Page: https://theprsb.org/medsdataready
- BHF DSC Services: https://bhfdatasciencecentre.org/research-services-new/
- HDR UK Phenotype Library: https://phenotype.hdruk.ac.uk/
- NHS England SDE: https://www.england.nhs.uk/secure-data-environment/
- PRSB Standards: https://theprsb.org/standards/