from fhir.resources import patient, relatedperson
from components.serializers import (
    convert_identifier, convert_codeable_concept, convert_contact_point,
    convert_human_name, convert_address, convert_attachment, convert_period
)
from . import models


def convert_patient_contact(django_contact):
    """Convert Django PatientContact to FHIR Patient.contact"""
    if not django_contact:
        return None
    
    data = {}
    
    # Relationships
    relationships = []
    for relationship in django_contact.relationships.all():
        fhir_relationship = convert_codeable_concept(relationship)
        if fhir_relationship:
            relationships.append(fhir_relationship)
    if relationships:
        data['relationship'] = relationships
    
    # Name
    if django_contact.name:
        data['name'] = convert_human_name(django_contact.name)
    
    # Telecom
    telecom_points = []
    for telecom in django_contact.telecom_points.all():
        fhir_telecom = convert_contact_point(telecom)
        if fhir_telecom:
            telecom_points.append(fhir_telecom)
    if telecom_points:
        data['telecom'] = telecom_points
    
    # Address
    if django_contact.address:
        data['address'] = convert_address(django_contact.address)
    
    # Gender
    if django_contact.gender:
        data['gender'] = django_contact.gender
    
    # Organization
    if django_contact.organization:
        data['organization'] = {'reference': f'Organization/{django_contact.organization.fhir_id}'}
    
    # Period
    if django_contact.period:
        data['period'] = convert_period(django_contact.period)
    
    return data


def convert_patient_communication(django_comm):
    """Convert Django PatientCommunication to FHIR Patient.communication"""
    if not django_comm:
        return None
    
    data = {}
    if django_comm.language:
        data['language'] = convert_codeable_concept(django_comm.language)
    if django_comm.preferred is not None:
        data['preferred'] = django_comm.preferred
    
    return data


def convert_patient_link(django_link):
    """Convert Django PatientLink to FHIR Patient.link"""
    if not django_link:
        return None
    
    data = {
        'type': django_link.type
    }
    
    # Other reference (choice type)
    if django_link.other_patient:
        data['other'] = {'reference': f'Patient/{django_link.other_patient.fhir_id}'}
    elif django_link.other_related_person:
        data['other'] = {'reference': f'RelatedPerson/{django_link.other_related_person.fhir_id}'}
    
    return data


def convert_patient(django_patient):
    """Convert Django Patient to FHIR Patient"""
    if not django_patient:
        return None
    
    data = {
        'resourceType': 'Patient',
        'id': django_patient.fhir_id
    }
    
    # Basic fields
    if django_patient.active is not None:
        data['active'] = django_patient.active
    if django_patient.gender:
        data['gender'] = django_patient.gender
    if django_patient.birthDate:
        data['birthDate'] = django_patient.birthDate.isoformat()
    
    # Deceased choice type
    if django_patient.deceasedBoolean is not None:
        data['deceasedBoolean'] = django_patient.deceasedBoolean
    elif django_patient.deceasedDateTime:
        data['deceasedDateTime'] = django_patient.deceasedDateTime.isoformat()
    
    # Multiple birth choice type
    if django_patient.multipleBirthBoolean is not None:
        data['multipleBirthBoolean'] = django_patient.multipleBirthBoolean
    elif django_patient.multipleBirthInteger is not None:
        data['multipleBirthInteger'] = django_patient.multipleBirthInteger
    
    # Marital status
    if django_patient.maritalStatus:
        data['maritalStatus'] = convert_codeable_concept(django_patient.maritalStatus)
    
    # Managing organization
    if django_patient.managingOrganization:
        data['managingOrganization'] = {'reference': f'Organization/{django_patient.managingOrganization.fhir_id}'}
    
    # Identifiers
    identifiers = []
    for identifier in django_patient.identifiers.all():
        fhir_identifier = convert_identifier(identifier)
        if fhir_identifier:
            identifiers.append(fhir_identifier)
    if identifiers:
        data['identifier'] = identifiers
    
    # Names
    names = []
    for name in django_patient.names.all():
        fhir_name = convert_human_name(name)
        if fhir_name:
            names.append(fhir_name)
    if names:
        data['name'] = names
    
    # Telecom
    telecom_points = []
    for telecom in django_patient.telecom_points.all():
        fhir_telecom = convert_contact_point(telecom)
        if fhir_telecom:
            telecom_points.append(fhir_telecom)
    if telecom_points:
        data['telecom'] = telecom_points
    
    # Addresses
    addresses = []
    for address in django_patient.addresses.all():
        fhir_address = convert_address(address)
        if fhir_address:
            addresses.append(fhir_address)
    if addresses:
        data['address'] = addresses
    
    # Photos
    photos = []
    for photo in django_patient.photos.all():
        fhir_photo = convert_attachment(photo)
        if fhir_photo:
            photos.append(fhir_photo)
    if photos:
        data['photo'] = photos
    
    # Contacts
    contacts = []
    for contact in django_patient.contacts.all():
        fhir_contact = convert_patient_contact(contact)
        if fhir_contact:
            contacts.append(fhir_contact)
    if contacts:
        data['contact'] = contacts
    
    # Communications
    communications = []
    for comm in django_patient.communications.all():
        fhir_comm = convert_patient_communication(comm)
        if fhir_comm:
            communications.append(fhir_comm)
    if communications:
        data['communication'] = communications
    
    # General practitioners
    general_practitioners = []
    for gp in django_patient.generalPractitioner.all():
        general_practitioners.append({'reference': f'Practitioner/{gp.fhir_id}'})
    for gp_role in django_patient.generalPractitionerRole.all():
        general_practitioners.append({'reference': f'PractitionerRole/{gp_role.fhir_id}'})
    for gp_org in django_patient.generalPractitionerOrg.all():
        general_practitioners.append({'reference': f'Organization/{gp_org.fhir_id}'})
    if general_practitioners:
        data['generalPractitioner'] = general_practitioners
    
    # Links
    links = []
    for link in django_patient.links.all():
        fhir_link = convert_patient_link(link)
        if fhir_link:
            links.append(fhir_link)
    if links:
        data['link'] = links
    
    return patient.Patient(**data)


def convert_related_person_communication(django_comm):
    """Convert Django RelatedPersonCommunication to FHIR RelatedPerson.communication"""
    if not django_comm:
        return None
    
    data = {}
    if django_comm.language:
        data['language'] = convert_codeable_concept(django_comm.language)
    if django_comm.preferred is not None:
        data['preferred'] = django_comm.preferred
    
    return data


def convert_related_person(django_related_person):
    """Convert Django RelatedPerson to FHIR RelatedPerson"""
    if not django_related_person:
        return None
    
    data = {
        'resourceType': 'RelatedPerson',
        'id': django_related_person.fhir_id
    }
    
    # Basic fields
    if django_related_person.active is not None:
        data['active'] = django_related_person.active
    if django_related_person.gender:
        data['gender'] = django_related_person.gender
    if django_related_person.birthDate:
        data['birthDate'] = django_related_person.birthDate.isoformat()
    
    # Required patient reference
    data['patient'] = {'reference': f'Patient/{django_related_person.patient.fhir_id}'}
    
    # Period
    if django_related_person.period:
        data['period'] = convert_period(django_related_person.period)
    
    # Identifiers
    identifiers = []
    for identifier in django_related_person.identifiers.all():
        fhir_identifier = convert_identifier(identifier)
        if fhir_identifier:
            identifiers.append(fhir_identifier)
    if identifiers:
        data['identifier'] = identifiers
    
    # Relationships
    relationships = []
    for relationship in django_related_person.relationships.all():
        fhir_relationship = convert_codeable_concept(relationship)
        if fhir_relationship:
            relationships.append(fhir_relationship)
    if relationships:
        data['relationship'] = relationships
    
    # Names
    names = []
    for name in django_related_person.names.all():
        fhir_name = convert_human_name(name)
        if fhir_name:
            names.append(fhir_name)
    if names:
        data['name'] = names
    
    # Telecom
    telecom_points = []
    for telecom in django_related_person.telecom_points.all():
        fhir_telecom = convert_contact_point(telecom)
        if fhir_telecom:
            telecom_points.append(fhir_telecom)
    if telecom_points:
        data['telecom'] = telecom_points
    
    # Addresses
    addresses = []
    for address in django_related_person.addresses.all():
        fhir_address = convert_address(address)
        if fhir_address:
            addresses.append(fhir_address)
    if addresses:
        data['address'] = addresses
    
    # Photos
    photos = []
    for photo in django_related_person.photos.all():
        fhir_photo = convert_attachment(photo)
        if fhir_photo:
            photos.append(fhir_photo)
    if photos:
        data['photo'] = photos
    
    # Communications
    communications = []
    for comm in django_related_person.communications.all():
        fhir_comm = convert_related_person_communication(comm)
        if fhir_comm:
            communications.append(fhir_comm)
    if communications:
        data['communication'] = communications
    
    return relatedperson.RelatedPerson(**data)