from fhir.resources import endpoint
from components.serializers import (
    convert_identifier, convert_codeable_concept, convert_contact_point,
    convert_period
)
from . import models


def convert_endpoint_payload(django_payload):
    """Convert Django EndpointPayload to FHIR Endpoint.payload"""
    if not django_payload:
        return None
    
    data = {}
    
    # Get payload types
    types = []
    for payload_type in django_payload.payload_types.all():
        fhir_type = convert_codeable_concept(payload_type)
        if fhir_type:
            types.append(fhir_type)
    if types:
        data['type'] = types
    
    if django_payload.mimeType:
        data['mimeType'] = django_payload.mimeType
    
    return data


def convert_endpoint(django_endpoint):
    """Convert Django Endpoint to FHIR Endpoint"""
    if not django_endpoint:
        return None
    
    data = {
        'resourceType': 'Endpoint',
        'id': django_endpoint.fhir_id
    }
    
    # Basic fields
    if django_endpoint.status:
        data['status'] = django_endpoint.status
    if django_endpoint.name:
        data['name'] = django_endpoint.name
    if django_endpoint.description:
        data['description'] = django_endpoint.description
    if django_endpoint.address:
        data['address'] = django_endpoint.address
    if django_endpoint.header:
        data['header'] = django_endpoint.header
    
    # Identifiers
    identifiers = []
    for identifier in django_endpoint.identifiers.all():
        fhir_identifier = convert_identifier(identifier)
        if fhir_identifier:
            identifiers.append(fhir_identifier)
    if identifiers:
        data['identifier'] = identifiers
    
    # Connection type
    connection_types = []
    for conn_type in django_endpoint.connection_types.all():
        fhir_type = convert_codeable_concept(conn_type)
        if fhir_type:
            connection_types.append(fhir_type)
    if connection_types:
        data['connectionType'] = connection_types
    
    # Environment type
    env_types = []
    for env_type in django_endpoint.environment_types.all():
        fhir_type = convert_codeable_concept(env_type)
        if fhir_type:
            env_types.append(fhir_type)
    if env_types:
        data['environmentType'] = env_types
    
    # Managing organization
    if django_endpoint.managingOrganization:
        data['managingOrganization'] = {'reference': f'Organization/{django_endpoint.managingOrganization.fhir_id}'}
    
    # Contacts
    contacts = []
    for contact in django_endpoint.contacts.all():
        contact_data = {}
        if contact.name:
            contact_data['name'] = contact.name
        
        # Get telecom points for this contact
        telecom_points = []
        for telecom in contact.telecom_points.all():
            fhir_telecom = convert_contact_point(telecom)
            if fhir_telecom:
                telecom_points.append(fhir_telecom)
        if telecom_points:
            contact_data['telecom'] = telecom_points
        
        if contact_data:
            contacts.append(contact_data)
    if contacts:
        data['contact'] = contacts
    
    # Period
    if django_endpoint.period:
        data['period'] = convert_period(django_endpoint.period)
    
    # Payloads
    payloads = []
    for payload in django_endpoint.payloads.all():
        fhir_payload = convert_endpoint_payload(payload)
        if fhir_payload:
            payloads.append(fhir_payload)
    if payloads:
        data['payload'] = payloads
    
    return endpoint.Endpoint(**data)