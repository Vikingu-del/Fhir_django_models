from fhir.resources import (
    identifier, codeableconcept, contactpoint, humanname, 
    address, attachment, period, coding, quantity
)
from . import models


def convert_identifier(django_identifier):
    """Convert Django Identifier to FHIR Identifier"""
    if not django_identifier:
        return None
    
    data = {}
    if django_identifier.use:
        data['use'] = django_identifier.use
    if django_identifier.system:
        data['system'] = django_identifier.system
    if django_identifier.value:
        data['value'] = django_identifier.value
    if django_identifier.type:
        data['type'] = convert_codeable_concept(django_identifier.type)
    if django_identifier.period:
        data['period'] = convert_period(django_identifier.period)
    if django_identifier.assigner:
        data['assigner'] = {'reference': f'Organization/{django_identifier.assigner.fhir_id}'}
    
    return identifier.Identifier(**data)


def convert_codeable_concept(django_cc):
    """Convert Django CodeableConcept to FHIR CodeableConcept"""
    if not django_cc:
        return None
    
    data = {}
    if django_cc.text:
        data['text'] = django_cc.text
    
    # Get codings
    codings = []
    for coding_obj in django_cc.codings.all():
        coding_data = {}
        if coding_obj.system:
            coding_data['system'] = coding_obj.system
        if coding_obj.version:
            coding_data['version'] = coding_obj.version
        if coding_obj.code:
            coding_data['code'] = coding_obj.code
        if coding_obj.display:
            coding_data['display'] = coding_obj.display
        if coding_obj.userSelected is not None:
            coding_data['userSelected'] = coding_obj.userSelected
        
        if coding_data:
            codings.append(coding.Coding(**coding_data))
    
    if codings:
        data['coding'] = codings
    
    return codeableconcept.CodeableConcept(**data)


def convert_contact_point(django_cp):
    """Convert Django ContactPoint to FHIR ContactPoint"""
    if not django_cp:
        return None
    
    data = {}
    if django_cp.system:
        data['system'] = django_cp.system
    if django_cp.value:
        data['value'] = django_cp.value
    if django_cp.use:
        data['use'] = django_cp.use
    if django_cp.rank:
        data['rank'] = django_cp.rank
    if django_cp.period:
        data['period'] = convert_period(django_cp.period)
    
    return contactpoint.ContactPoint(**data)


def convert_human_name(django_name):
    """Convert Django HumanName to FHIR HumanName"""
    if not django_name:
        return None
    
    data = {}
    if django_name.use:
        data['use'] = django_name.use
    if django_name.text:
        data['text'] = django_name.text
    if django_name.family:
        data['family'] = django_name.family
    if django_name.given:
        data['given'] = django_name.given
    if django_name.prefix:
        data['prefix'] = django_name.prefix
    if django_name.suffix:
        data['suffix'] = django_name.suffix
    if django_name.period:
        data['period'] = convert_period(django_name.period)
    
    return humanname.HumanName(**data)


def convert_address(django_address):
    """Convert Django Address to FHIR Address"""
    if not django_address:
        return None
    
    data = {}
    if django_address.use:
        data['use'] = django_address.use
    if django_address.type:
        data['type'] = django_address.type
    if django_address.text:
        data['text'] = django_address.text
    if django_address.line:
        data['line'] = django_address.line
    if django_address.city:
        data['city'] = django_address.city
    if django_address.district:
        data['district'] = django_address.district
    if django_address.state:
        data['state'] = django_address.state
    if django_address.postalCode:
        data['postalCode'] = django_address.postalCode
    if django_address.country:
        data['country'] = django_address.country
    if django_address.period:
        data['period'] = convert_period(django_address.period)
    
    return address.Address(**data)


def convert_attachment(django_attachment):
    """Convert Django Attachment to FHIR Attachment"""
    if not django_attachment:
        return None
    
    data = {}
    if django_attachment.contentType:
        data['contentType'] = django_attachment.contentType
    if django_attachment.language:
        data['language'] = django_attachment.language
    if django_attachment.data:
        data['data'] = django_attachment.data
    if django_attachment.url:
        data['url'] = django_attachment.url
    if django_attachment.size:
        data['size'] = django_attachment.size
    if django_attachment.hash:
        data['hash'] = django_attachment.hash
    if django_attachment.title:
        data['title'] = django_attachment.title
    if django_attachment.creation:
        data['creation'] = django_attachment.creation.isoformat()
    if django_attachment.height:
        data['height'] = django_attachment.height
    if django_attachment.width:
        data['width'] = django_attachment.width
    if django_attachment.frames:
        data['frames'] = django_attachment.frames
    if django_attachment.duration:
        data['duration'] = float(django_attachment.duration)
    if django_attachment.pages:
        data['pages'] = django_attachment.pages
    
    return attachment.Attachment(**data)


def convert_period(django_period):
    """Convert Django Period to FHIR Period"""
    if not django_period:
        return None
    
    data = {}
    if django_period.start:
        data['start'] = django_period.start.isoformat()
    if django_period.end:
        data['end'] = django_period.end.isoformat()
    
    return period.Period(**data)


def convert_quantity(django_quantity):
    """Convert Django Quantity to FHIR Quantity"""
    if not django_quantity:
        return None
    
    data = {}
    if django_quantity.value:
        data['value'] = float(django_quantity.value)
    if django_quantity.comparator:
        data['comparator'] = django_quantity.comparator
    if django_quantity.unit:
        data['unit'] = django_quantity.unit
    if django_quantity.system:
        data['system'] = django_quantity.system
    if django_quantity.code:
        data['code'] = django_quantity.code
    
    return quantity.Quantity(**data)