"""
Central FHIR serialization module
Converts Django models to FHIR resources using fhir.resources library
"""

from organization.serializers import convert_organization
from endpoint.serializers import convert_endpoint
from practitioner.serializers import convert_practitioner, convert_practitioner_role
from healthcareservice.serializers import convert_healthcare_service
from location.serializers import convert_location
from patient.serializers import convert_patient, convert_related_person
from citation.serializers import convert_citation

# Import models for type checking
from organization.models import Organization
from endpoint.models import Endpoint
from practitioner.models import Practitioner, PractitionerRole
from healthcareservice.models import HealthcareService
from location.models import Location
from patient.models import Patient, RelatedPerson
from citation.models import Citation


def serialize_to_fhir(django_instance):
    """
    Convert any Django FHIR model instance to its corresponding FHIR resource
    
    Args:
        django_instance: Django model instance
        
    Returns:
        FHIR resource object from fhir.resources library
        
    Raises:
        ValueError: If the model type is not supported
    """
    
    if isinstance(django_instance, Organization):
        return convert_organization(django_instance)
    elif isinstance(django_instance, Endpoint):
        return convert_endpoint(django_instance)
    elif isinstance(django_instance, Practitioner):
        return convert_practitioner(django_instance)
    elif isinstance(django_instance, PractitionerRole):
        return convert_practitioner_role(django_instance)
    elif isinstance(django_instance, HealthcareService):
        return convert_healthcare_service(django_instance)
    elif isinstance(django_instance, Location):
        return convert_location(django_instance)
    elif isinstance(django_instance, Patient):
        return convert_patient(django_instance)
    elif isinstance(django_instance, RelatedPerson):
        return convert_related_person(django_instance)
    elif isinstance(django_instance, Citation):
        return convert_citation(django_instance)
    else:
        raise ValueError(f"Unsupported model type: {type(django_instance)}")


def serialize_queryset_to_fhir(queryset):
    """
    Convert a Django queryset to a list of FHIR resources
    
    Args:
        queryset: Django queryset
        
    Returns:
        List of FHIR resource objects
    """
    return [serialize_to_fhir(instance) for instance in queryset]


def get_fhir_json(django_instance):
    """
    Get FHIR JSON representation of a Django model instance
    
    Args:
        django_instance: Django model instance
        
    Returns:
        JSON string of FHIR resource
    """
    fhir_resource = serialize_to_fhir(django_instance)
    return fhir_resource.json()


def get_fhir_dict(django_instance):
    """
    Get FHIR dictionary representation of a Django model instance
    
    Args:
        django_instance: Django model instance
        
    Returns:
        Dictionary representation of FHIR resource
    """
    fhir_resource = serialize_to_fhir(django_instance)
    return fhir_resource.dict()


# Example usage functions
def example_usage():
    """
    Example of how to use the FHIR serializers
    """
    
    # Get a Django model instance
    org = Organization.objects.first()
    
    if org:
        # Convert to FHIR resource object
        fhir_org = serialize_to_fhir(org)
        print(f"FHIR Resource Type: {fhir_org.resource_type}")
        
        # Get JSON representation
        json_output = get_fhir_json(org)
        print(f"FHIR JSON: {json_output}")
        
        # Get dictionary representation
        dict_output = get_fhir_dict(org)
        print(f"FHIR Dict: {dict_output}")
        
        # Convert multiple instances
        all_orgs = Organization.objects.all()
        fhir_orgs = serialize_queryset_to_fhir(all_orgs)
        print(f"Converted {len(fhir_orgs)} organizations to FHIR")


if __name__ == "__main__":
    example_usage()