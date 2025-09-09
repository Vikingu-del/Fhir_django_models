from fhir.resources import healthcareservice
from components.serializers import (
    convert_identifier, convert_codeable_concept, convert_attachment
)
from . import models


def convert_healthcare_service_eligibility(django_eligibility):
    """Convert Django HealthcareServiceEligibility to FHIR HealthcareService.eligibility"""
    if not django_eligibility:
        return None
    
    data = {}
    if django_eligibility.code:
        data['code'] = convert_codeable_concept(django_eligibility.code)
    if django_eligibility.comment:
        data['comment'] = django_eligibility.comment
    
    return data


def convert_healthcare_service(django_service):
    """Convert Django HealthcareService to FHIR HealthcareService"""
    if not django_service:
        return None
    
    data = {
        'resourceType': 'HealthcareService',
        'id': django_service.fhir_id
    }
    
    # Basic fields
    if django_service.active is not None:
        data['active'] = django_service.active
    if django_service.name:
        data['name'] = django_service.name
    if django_service.comment:
        data['comment'] = django_service.comment
    if django_service.extraDetails:
        data['extraDetails'] = django_service.extraDetails
    if django_service.appointmentRequired is not None:
        data['appointmentRequired'] = django_service.appointmentRequired
    
    # References
    if django_service.providedBy:
        data['providedBy'] = {'reference': f'Organization/{django_service.providedBy.fhir_id}'}
    
    # Identifiers
    identifiers = []
    for identifier in django_service.identifiers.all():
        fhir_identifier = convert_identifier(identifier)
        if fhir_identifier:
            identifiers.append(fhir_identifier)
    if identifiers:
        data['identifier'] = identifiers
    
    # Categories
    categories = []
    for category in django_service.categories.all():
        fhir_category = convert_codeable_concept(category)
        if fhir_category:
            categories.append(fhir_category)
    if categories:
        data['category'] = categories
    
    # Types
    types = []
    for service_type in django_service.types.all():
        fhir_type = convert_codeable_concept(service_type)
        if fhir_type:
            types.append(fhir_type)
    if types:
        data['type'] = types
    
    # Specialties
    specialties = []
    for specialty in django_service.specialties.all():
        fhir_specialty = convert_codeable_concept(specialty)
        if fhir_specialty:
            specialties.append(fhir_specialty)
    if specialties:
        data['specialty'] = specialties
    
    # Locations
    locations = []
    for location in django_service.location.all():
        locations.append({'reference': f'Location/{location.fhir_id}'})
    if locations:
        data['location'] = locations
    
    # Coverage areas
    coverage_areas = []
    for area in django_service.coverageArea.all():
        coverage_areas.append({'reference': f'Location/{area.fhir_id}'})
    if coverage_areas:
        data['coverageArea'] = coverage_areas
    
    # Service provision codes
    provision_codes = []
    for code in django_service.service_provision_codes.all():
        fhir_code = convert_codeable_concept(code)
        if fhir_code:
            provision_codes.append(fhir_code)
    if provision_codes:
        data['serviceProvisionCode'] = provision_codes
    
    # Programs
    programs = []
    for program in django_service.programs.all():
        fhir_program = convert_codeable_concept(program)
        if fhir_program:
            programs.append(fhir_program)
    if programs:
        data['program'] = programs
    
    # Characteristics
    characteristics = []
    for characteristic in django_service.characteristics.all():
        fhir_characteristic = convert_codeable_concept(characteristic)
        if fhir_characteristic:
            characteristics.append(fhir_characteristic)
    if characteristics:
        data['characteristic'] = characteristics
    
    # Communications
    communications = []
    for communication in django_service.communications.all():
        fhir_communication = convert_codeable_concept(communication)
        if fhir_communication:
            communications.append(fhir_communication)
    if communications:
        data['communication'] = communications
    
    # Referral methods
    referral_methods = []
    for method in django_service.referral_methods.all():
        fhir_method = convert_codeable_concept(method)
        if fhir_method:
            referral_methods.append(fhir_method)
    if referral_methods:
        data['referralMethod'] = referral_methods
    
    # Photo
    if django_service.photo:
        data['photo'] = convert_attachment(django_service.photo)
    
    # Eligibilities
    eligibilities = []
    for eligibility in django_service.eligibilities.all():
        fhir_eligibility = convert_healthcare_service_eligibility(eligibility)
        if fhir_eligibility:
            eligibilities.append(fhir_eligibility)
    if eligibilities:
        data['eligibility'] = eligibilities
    
    # Endpoints
    endpoints = []
    for endpoint in django_service.endpoint.all():
        endpoints.append({'reference': f'Endpoint/{endpoint.fhir_id}'})
    if endpoints:
        data['endpoint'] = endpoints
    
    # Offered in (self-references)
    offered_in = []
    for service in django_service.offeredIn.all():
        offered_in.append({'reference': f'HealthcareService/{service.fhir_id}'})
    if offered_in:
        data['offeredIn'] = offered_in
    
    return healthcareservice.HealthcareService(**data)