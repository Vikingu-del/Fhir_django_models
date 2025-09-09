"""
FHIR Django Models

A Django package providing models for FHIR (Fast Healthcare Interoperability Resources) standard.
This package allows easy integration of FHIR complex types into Django applications.
"""

__version__ = '0.1.0'
__author__ = 'Erik'

default_app_config = 'fhir_django_models.apps.FhirDjangoModelsConfig'

# Define what models are available without importing them immediately
__all__ = [
    # Core models
    'FHIRBaseModel',
    'Identifier',
    'CodeableConcept',
    'Coding',
    'HumanName',
    'ContactPoint',
    'Address',
    # Patient models
    'Patient',
    'PatientContact',
    'PatientCommunication',
    # Practitioner models
    'Practitioner',
    'PractitionerQualification',
    # Observation models
    'Observation',
    'ObservationComponent',
]

def get_model(model_name):
    """
    Lazy import function to get a model by name.
    This avoids importing models before Django apps are ready.
    """
    if model_name in [
        'FHIRBaseModel', 'Identifier', 'CodeableConcept', 
        'Coding', 'HumanName', 'ContactPoint', 'Address'
    ]:
        from .core.models import (
            FHIRBaseModel, Identifier, CodeableConcept,
            Coding, HumanName, ContactPoint, Address
        )
        return locals()[model_name]
    
    elif model_name in ['Patient', 'PatientContact', 'PatientCommunication']:
        from .patient.models import Patient, PatientContact, PatientCommunication
        return locals()[model_name]
    
    elif model_name in ['Practitioner', 'PractitionerQualification']:
        from .practitioner.models import Practitioner, PractitionerQualification
        return locals()[model_name]
    
    elif model_name in ['Observation', 'ObservationComponent']:
        from .observation.models import Observation, ObservationComponent
        return locals()[model_name]
    
    else:
        raise ValueError(f"Unknown model: {model_name}")


def __getattr__(name):
    """
    Dynamic attribute access for lazy loading of models.
    This allows 'from fhir_django_models import Patient' to work.
    """
    if name in __all__:
        return get_model(name)
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")