from fhir.resources import practitioner, practitionerrole
from components.serializers import (
    convert_identifier, convert_codeable_concept, convert_contact_point,
    convert_human_name, convert_address, convert_period, convert_attachment
)
from . import models


def convert_practitioner_qualification(django_qual):
    """Convert Django PractitionerQualification to FHIR Practitioner.qualification"""
    if not django_qual:
        return None
    
    data = {}
    if django_qual.code:
        data['code'] = convert_codeable_concept(django_qual.code)
    if django_qual.period:
        data['period'] = convert_period(django_qual.period)
    if django_qual.issuer:
        data['issuer'] = {'reference': f'Organization/{django_qual.issuer.fhir_id}'}
    
    # Get identifiers for this qualification
    identifiers = []
    for identifier in django_qual.identifiers.all():
        fhir_identifier = convert_identifier(identifier)
        if fhir_identifier:
            identifiers.append(fhir_identifier)
    if identifiers:
        data['identifier'] = identifiers
    
    return data


def convert_practitioner_communication(django_comm):
    """Convert Django PractitionerCommunication to FHIR Practitioner.communication"""
    if not django_comm:
        return None
    
    data = {}
    if django_comm.language:
        data['language'] = convert_codeable_concept(django_comm.language)
    if django_comm.preferred is not None:
        data['preferred'] = django_comm.preferred
    
    return data


def convert_practitioner(django_practitioner):
    """Convert Django Practitioner to FHIR Practitioner"""
    if not django_practitioner:
        return None
    
    data = {
        'resourceType': 'Practitioner',
        'id': django_practitioner.fhir_id
    }
    
    # Basic fields
    if django_practitioner.active is not None:
        data['active'] = django_practitioner.active
    if django_practitioner.gender:
        data['gender'] = django_practitioner.gender
    if django_practitioner.birthDate:
        data['birthDate'] = django_practitioner.birthDate.isoformat()
    
    # Deceased choice type
    if django_practitioner.deceasedBoolean is not None:
        data['deceasedBoolean'] = django_practitioner.deceasedBoolean
    elif django_practitioner.deceasedDateTime:
        data['deceasedDateTime'] = django_practitioner.deceasedDateTime.isoformat()
    
    # Identifiers
    identifiers = []
    for identifier in django_practitioner.identifiers.all():
        fhir_identifier = convert_identifier(identifier)
        if fhir_identifier:
            identifiers.append(fhir_identifier)
    if identifiers:
        data['identifier'] = identifiers
    
    # Names
    names = []
    for name in django_practitioner.names.all():
        fhir_name = convert_human_name(name)
        if fhir_name:
            names.append(fhir_name)
    if names:
        data['name'] = names
    
    # Telecom
    telecom_points = []
    for telecom in django_practitioner.telecom_points.all():
        fhir_telecom = convert_contact_point(telecom)
        if fhir_telecom:
            telecom_points.append(fhir_telecom)
    if telecom_points:
        data['telecom'] = telecom_points
    
    # Addresses
    addresses = []
    for address in django_practitioner.addresses.all():
        fhir_address = convert_address(address)
        if fhir_address:
            addresses.append(fhir_address)
    if addresses:
        data['address'] = addresses
    
    # Photos
    if django_practitioner.photo:
        # Handle JSONField array of attachments
        photos = []
        for photo_data in django_practitioner.photo:
            # This would need custom handling since it's stored as JSON
            photos.append(photo_data)
        if photos:
            data['photo'] = photos
    
    # Qualifications
    qualifications = []
    for qual in django_practitioner.qualifications.all():
        fhir_qual = convert_practitioner_qualification(qual)
        if fhir_qual:
            qualifications.append(fhir_qual)
    if qualifications:
        data['qualification'] = qualifications
    
    # Communications
    communications = []
    for comm in django_practitioner.communications.all():
        fhir_comm = convert_practitioner_communication(comm)
        if fhir_comm:
            communications.append(fhir_comm)
    if communications:
        data['communication'] = communications
    
    return practitioner.Practitioner(**data)


def convert_practitioner_role(django_role):
    """Convert Django PractitionerRole to FHIR PractitionerRole"""
    if not django_role:
        return None
    
    data = {
        'resourceType': 'PractitionerRole',
        'id': django_role.fhir_id
    }
    
    # Basic fields
    if django_role.active is not None:
        data['active'] = django_role.active
    if django_role.period:
        data['period'] = convert_period(django_role.period)
    
    # References
    if django_role.practitioner:
        data['practitioner'] = {'reference': f'Practitioner/{django_role.practitioner.fhir_id}'}
    if django_role.organization:
        data['organization'] = {'reference': f'Organization/{django_role.organization.fhir_id}'}
    
    # Identifiers
    identifiers = []
    for identifier in django_role.identifiers.all():
        fhir_identifier = convert_identifier(identifier)
        if fhir_identifier:
            identifiers.append(fhir_identifier)
    if identifiers:
        data['identifier'] = identifiers
    
    # Codes
    codes = []
    for code in django_role.codes.all():
        fhir_code = convert_codeable_concept(code)
        if fhir_code:
            codes.append(fhir_code)
    if codes:
        data['code'] = codes
    
    # Specialties
    specialties = []
    for specialty in django_role.specialties.all():
        fhir_specialty = convert_codeable_concept(specialty)
        if fhir_specialty:
            specialties.append(fhir_specialty)
    if specialties:
        data['specialty'] = specialties
    
    # Locations
    locations = []
    for location in django_role.location.all():
        locations.append({'reference': f'Location/{location.fhir_id}'})
    if locations:
        data['location'] = locations
    
    # Healthcare services
    healthcare_services = []
    for service in django_role.healthcare_services.all():
        healthcare_services.append({'reference': f'HealthcareService/{service.fhir_id}'})
    if healthcare_services:
        data['healthcareService'] = healthcare_services
    
    # Endpoints
    endpoints = []
    for endpoint in django_role.endpoint.all():
        endpoints.append({'reference': f'Endpoint/{endpoint.fhir_id}'})
    if endpoints:
        data['endpoint'] = endpoints
    
    return practitionerrole.PractitionerRole(**data)