from django.db import models
from django.core.exceptions import ValidationError
from abstractClasses.models import DomainResource, BackboneElement


class OrganizationQualification(BackboneElement):
    """Qualifications, certifications, accreditations, licenses, training, etc."""
    # Organization this qualification belongs to
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE, related_name='qualifications', null=True, blank=True)
    # An identifier for this qualification for the organization (0..* Identifier)
    # Note: Use reverse FK from Identifier model
    # Coded representation of the qualification (1..1 CodeableConcept)
    code = models.ForeignKey('components.CodeableConcept', on_delete=models.CASCADE, related_name='organization_qualifications')
    # Period during which the qualification is valid (0..1 Period)
    period = models.ForeignKey('components.Period', null=True, blank=True, on_delete=models.SET_NULL, related_name='organization_qualifications')
    # Organization that regulates and issues the qualification (0..1 Reference(Organization))
    issuer = models.ForeignKey('Organization', null=True, blank=True, on_delete=models.SET_NULL, related_name='issued_qualifications')
    
    class Meta:
        db_table = 'org_qualification'


class Organization(DomainResource):
    """A grouping of people or organizations with a common purpose"""
    
    # Identifies this organization across multiple systems (0..* Identifier)
    # Note: Identifier has reverse FK to Organization as 'identifiers'
    # Whether the organization's record is still in active use (0..1 boolean)
    active = models.BooleanField(null=True, blank=True)
    # Kind of organization (0..* CodeableConcept)
    # Note: CodeableConcept has reverse FK to Organization as 'org_types'
    # Name used for the organization (0..1 string)
    name = models.CharField(max_length=256, null=True, blank=True)
    # A list of alternate names (0..* string)
    alias = models.JSONField(null=True, blank=True)  # Array of alias strings
    # Additional details about the Organization (0..1 markdown)
    description = models.TextField(null=True, blank=True)
    # Official contact details for the Organization (0..* ExtendedContactDetail)
    # Note: ContactDetail has reverse FK to Organization as 'contacts'
    # The organization of which this organization forms a part (0..1 Reference(Organization))
    partOf = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='child_organizations')
    # Technical endpoints providing access to services (0..* Reference(Endpoint))
    # Note: Endpoint has reverse FK to Organization as 'endpoints'
    # Qualifications, certifications, accreditations, licenses, training, etc. (0..* BackboneElement)
    # Note: OrganizationQualification has reverse FK to Organization
    
    class Meta:
        db_table = 'organization'
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['active']),
        ]
    
    def clean(self):
        super().clean()
        # FHIR Rule: The organization SHALL at least have a name or an identifier
        has_identifier = self.pk and self.identifier.exists()
        has_name = bool(self.name and self.name.strip())
        if not (has_identifier or has_name):
            raise ValidationError("Organization must have at least a name or an identifier")
        
        # FHIR Rules: Organization contact telecom/address cannot be 'home' use
        if self.pk:
            for contact_detail in self.contact.all():
                for telecom in contact_detail.telecom.all():
                    if telecom.use == 'home':
                        raise ValidationError("Organization contact telecom cannot have 'home' use")
                # Note: Address validation would go here when Address model is implemented
    
    def __str__(self):
        return f"Organization(name={self.name})"