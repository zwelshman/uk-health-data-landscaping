"""
Cohort definition for Making secondary care medicines data research-ready project.

This module defines the cohort for hospital prescribing and high-cost drugs data
to make it research-ready across UK Secure Data Environments.

Project: Making secondary care medicines data research-ready
Lead: NHS England SDE with PRSB, University of Liverpool, Understanding Patient Data, King's College Hospital NHS Foundation Trust
Funding: HDRS technical transformation programme
Launch: October 2026
"""

from dataclasses import dataclass
from typing import List, Optional
from datetime import date


@dataclass
class MedicinesCohortDefinition:
    """Defines the cohort for secondary care medicines research-ready data."""
    
    # Inclusion criteria
    start_date: date = date(2020, 1, 1)  # Project launch context
    end_date: Optional[date] = None  # Ongoing
    
    # Data sources
    data_sources: List[str] = None
    
    # Medicine categories
    medicine_categories: List[str] = None
    
    # Care settings
    care_settings: List[str] = None
    
    def __post_init__(self):
        if self.data_sources is None:
            self.data_sources = [
                "Hospital Episode Statistics (HES) - Admitted Patient Care",
                "HES - Outpatient",
                "HES - Accident & Emergency",
                "NHS England Secondary Uses Service (SUS)",
                "Electronic Prescribing and Medicines Administration (ePMA)",
                "High Cost Drugs (HCD) dataset",
                "Systemic Anti-Cancer Therapy (SACT)",
                "National Clinical Audit datasets"
            ]
        
        if self.medicine_categories is None:
            self.medicine_categories = [
                "High-cost drugs (HCD)",
                "Systemic anti-cancer therapy (SACT)",
                "Biological therapies",
                "Advanced therapy medicinal products (ATMPs)",
                "Orphan drugs",
                "Hospital-only medicines",
                "Controlled drugs in secondary care"
            ]
        
        if self.care_settings is None:
            self.care_settings = [
                "Inpatient",
                "Outpatient",
                "Day case",
                "Emergency department",
                "Critical care",
                "Specialist centres"
            ]


def get_cohort_definition() -> MedicinesCohortDefinition:
    """Returns the standard cohort definition for secondary care medicines."""
    return MedicinesCohortDefinition()


def get_bhf_dsc_aligned_cohort() -> MedicinesCohortDefinition:
    """
    Returns cohort definition aligned with BHF DSC capabilities:
    - Population data access across England, Scotland, Wales
    - CVD-COVID-UK/COVID-IMPACT linked datasets
    - UK CliC TRE for consented cohort linkage
    - Curated HES APC diagnoses and procedures
    - Harmonised mortality variables
    """
    cohort = MedicinesCohortDefinition()
    # BHF DSC adds cardiovascular-relevant medicines focus
    cohort.medicine_categories.extend([
        "Cardiovascular medicines (anticoagulants, antihypertensives, statins)",
        "Heart failure medications (ARNI, SGLT2 inhibitors, MRAs)",
        "Antiplatelet and anticoagulation therapy",
        "Lipid-lowering therapies"
    ])
    return cohort