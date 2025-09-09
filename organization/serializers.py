from fhir.resources import organization
from components.serializers import (
    convert_identifier, convert_codeable_concept, convert_contact_point,
    convert_address, convert_period, convert_human_name
)
from . import models


def convert_organization_qualification(django_qual):
    """Convert Django OrganizationQualification to FHIR Organization.qualification"""
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


def convert_organization(django_org):
    """Convert Django Organization to FHIR Organization"""
    if not django_org:
        return None
    
    data = {
        'resourceType': 'Organization',
        'id': django_org.fhir_id
    }
    
    # Basic fields
    if django_org.active is not None:
        data['active'] = django_org.active
    if django_org.name:
        data['name'] = django_org.name
    if django_org.alias:
        data['alias'] = django_org.alias
    if django_org.description:
        data['description'] = django_org.description
    
    # Identifiers
    identifiers = []
    for identifier in django_org.identifiers.all():
        fhir_identifier = convert_identifier(identifier)
        if fhir_identifier:
            identifiers.append(fhir_identifier)
    if identifiers:
        data['identifier'] = identifiers
    
    # Types
    types = []
    for org_type in django_org.org_types.all():
        fhir_type = convert_codeable_concept(org_type)
        if fhir_type:
            types.append(fhir_type)
    if types:
        data['type'] = types
    
    # Contacts
    contacts = []
    for contact in django_org.contacts.all():
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
    
    # Extended contact details
    extended_contacts = []
    for ext_contact in django_org.extended_contact_details.all():
        ext_data = {}
        if ext_contact.purpose:
            ext_data['purpose'] = convert_codeable_concept(ext_contact.purpose)
        if ext_contact.address:
            ext_data['address'] = convert_address(ext_contact.address)
        if ext_contact.organization:
            ext_data['organization'] = {'reference': f'Organization/{ext_contact.organization.fhir_id}'}
        if ext_contact.period:
            ext_data['period'] = convert_period(ext_contact.period)
        
        # Get names and telecom for extended contact
        names = []
        for name in ext_contact.names.all():
            fhir_name = convert_human_name(name)
            if fhir_name:
                names.append(fhir_name)
        if names:
            ext_data['name'] = names
        
        telecom_points = []
        for telecom in ext_contact.telecom_points.all():
            fhir_telecom = convert_contact_point(telecom)
            if fhir_telecom:
                telecom_points.append(fhir_telecom)
        if telecom_points:
            ext_data['telecom'] = telecom_points
        
        if ext_data:
            extended_contacts.append(ext_data)
    if extended_contacts:
        data['contact'] = extended_contacts
    
    # Qualifications
    qualifications = []
    for qual in django_org.qualifications.all():
        fhir_qual = convert_organization_qualification(qual)
        if fhir_qual:
            qualifications.append(fhir_qual)
    if qualifications:
        data['qualification'] = qualifications
    
    # Part of
    if django_org.partOf:
        data['partOf'] = {'reference': f'Organization/{django_org.partOf.fhir_id}'}
    
    # Endpoints
    endpoints = []
    for endpoint in django_org.endpoints.all():
        endpoints.append({'reference': f'Endpoint/{endpoint.fhir_id}'})
    if endpoints:
        data['endpoint'] = endpoints
    
    return organization.Organization(**data)