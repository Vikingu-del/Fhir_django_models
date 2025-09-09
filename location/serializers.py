from fhir.resources import location
from components.serializers import (
    convert_identifier, convert_codeable_concept, convert_address
)
from . import models


def convert_location_position(django_position):
    """Convert Django LocationPosition to FHIR Location.position"""
    if not django_position:
        return None
    
    data = {
        'longitude': float(django_position.longitude),
        'latitude': float(django_position.latitude)
    }
    
    if django_position.altitude:
        data['altitude'] = float(django_position.altitude)
    
    return data


def convert_location(django_location):
    """Convert Django Location to FHIR Location"""
    if not django_location:
        return None
    
    data = {
        'resourceType': 'Location',
        'id': django_location.fhir_id
    }
    
    # Basic fields
    if django_location.status:
        data['status'] = django_location.status
    if django_location.name:
        data['name'] = django_location.name
    if django_location.alias:
        data['alias'] = django_location.alias
    if django_location.description:
        data['description'] = django_location.description
    if django_location.mode:
        data['mode'] = django_location.mode
    
    # Identifiers
    identifiers = []
    for identifier in django_location.identifiers.all():
        fhir_identifier = convert_identifier(identifier)
        if fhir_identifier:
            identifiers.append(fhir_identifier)
    if identifiers:
        data['identifier'] = identifiers
    
    # Operational status
    if django_location.operationalStatus:
        # Convert Coding to proper format
        coding_data = {}
        if django_location.operationalStatus.system:
            coding_data['system'] = django_location.operationalStatus.system
        if django_location.operationalStatus.code:
            coding_data['code'] = django_location.operationalStatus.code
        if django_location.operationalStatus.display:
            coding_data['display'] = django_location.operationalStatus.display
        if coding_data:
            data['operationalStatus'] = coding_data
    
    # Types
    types = []
    for location_type in django_location.types.all():
        fhir_type = convert_codeable_concept(location_type)
        if fhir_type:
            types.append(fhir_type)
    if types:
        data['type'] = types
    
    # Forms
    forms = []
    for form in django_location.forms.all():
        fhir_form = convert_codeable_concept(form)
        if fhir_form:
            forms.append(fhir_form)
    if forms:
        data['form'] = forms
    
    # Characteristics
    characteristics = []
    for characteristic in django_location.characteristics.all():
        fhir_characteristic = convert_codeable_concept(characteristic)
        if fhir_characteristic:
            characteristics.append(fhir_characteristic)
    if characteristics:
        data['characteristic'] = characteristics
    
    # Address
    if django_location.address:
        data['address'] = convert_address(django_location.address)
    
    # Position
    if hasattr(django_location, 'position') and django_location.position:
        data['position'] = convert_location_position(django_location.position)
    
    # Managing organization
    if django_location.managingOrganization:
        data['managingOrganization'] = {'reference': f'Organization/{django_location.managingOrganization.fhir_id}'}
    
    # Part of
    if django_location.partOf:
        data['partOf'] = {'reference': f'Location/{django_location.partOf.fhir_id}'}
    
    # Endpoints
    endpoints = []
    for endpoint in django_location.endpoint.all():
        endpoints.append({'reference': f'Endpoint/{endpoint.fhir_id}'})
    if endpoints:
        data['endpoint'] = endpoints
    
    return location.Location(**data)