from django.db import models
from django.core.exceptions import ValidationError
from abstractClasses.models import DomainResource, BackboneElement


class PractitionerQualification(BackboneElement):
    """Qualifications, certifications, accreditations, licenses, training, etc."""
    # Practitioner this qualification belongs to
    practitioner = models.ForeignKey('Practitioner', on_delete=models.CASCADE, related_name='qualifications', null=True, blank=True)
    # Coded representation of the qualification (1..1 CodeableConcept)
    code = models.ForeignKey('components.CodeableConcept', on_delete=models.CASCADE, related_name='practitioner_qualifications')
    # Period during which the qualification is valid (0..1 Period)
    period = models.ForeignKey('components.Period', null=True, blank=True, on_delete=models.SET_NULL, related_name='practitioner_qualifications')
    # Organization that regulates and issues the qualification (0..1 Reference(Organization))
    issuer = models.ForeignKey('organization.Organization', null=True, blank=True, on_delete=models.SET_NULL, related_name='issued_practitioner_qualifications')
    
    class Meta:
        db_table = 'practitioner_qualification'


class PractitionerCommunication(BackboneElement):
    """A language which may be used to communicate with the practitioner"""
    # Practitioner this communication belongs to
    practitioner = models.ForeignKey('Practitioner', on_delete=models.CASCADE, related_name='communications', null=True, blank=True)
    # The language code used to communicate with the practitioner (1..1 CodeableConcept)
    language = models.ForeignKey('components.CodeableConcept', on_delete=models.CASCADE, related_name='practitioner_communications')
    # Language preference indicator (0..1 boolean)
    preferred = models.BooleanField(null=True, blank=True)
    
    class Meta:
        db_table = 'practitioner_communication'


class Practitioner(DomainResource):
    """A person with a formal responsibility in the provisioning of healthcare or related services"""
    
    # Whether this practitioner's record is in active use (0..1 boolean)
    active = models.BooleanField(null=True, blank=True)
    
    # male | female | other | unknown (0..1 code)
    gender = models.CharField(max_length=16, null=True, blank=True, choices=[
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
        ('unknown', 'Unknown')
    ])
    
    # The date on which the practitioner was born (0..1 date)
    birthDate = models.DateField(null=True, blank=True)
    
    # Indicates if the practitioner is deceased or not (0..1 choice)
    deceasedBoolean = models.BooleanField(null=True, blank=True)
    deceasedDateTime = models.DateTimeField(null=True, blank=True)
    
    # Image of the person (0..* Attachment)
    photo = models.JSONField(null=True, blank=True)  # Array of attachment objects
    
    class Meta:
        db_table = 'practitioner'
        indexes = [
            models.Index(fields=['active']),
            models.Index(fields=['gender']),
            models.Index(fields=['birthDate']),
        ]
    
    def clean(self):
        super().clean()
        # FHIR invariant: only one deceased[x] can be set
        if self.deceasedBoolean is not None and self.deceasedDateTime is not None:
            raise ValidationError("Only one deceased[x] field can be set")
    
    def __str__(self):
        return f"Practitioner(id={self.fhir_id}, active={self.active})"


class PractitionerRole(DomainResource):
    """Roles/organizations the practitioner is associated with"""
    
    # Whether this practitioner role record is in active use (0..1 boolean)
    active = models.BooleanField(null=True, blank=True)
    
    # The period during which the practitioner is authorized to perform in these role(s) (0..1 Period)
    period = models.ForeignKey('components.Period', null=True, blank=True, on_delete=models.SET_NULL, related_name='practitioner_roles')
    
    # Practitioner that provides services for the organization (0..1 Reference(Practitioner))
    practitioner = models.ForeignKey('Practitioner', null=True, blank=True, on_delete=models.SET_NULL, related_name='roles')
    
    # Organization where the roles are available (0..1 Reference(Organization))
    organization = models.ForeignKey('organization.Organization', null=True, blank=True, on_delete=models.SET_NULL, related_name='practitioner_roles')
    
    # Location(s) where the practitioner provides care (0..* Reference(Location))
    location = models.ManyToManyField('location.Location', blank=True, related_name='practitioner_roles')
    
    # Endpoints for interacting with the practitioner in this role (0..* Reference(Endpoint))
    endpoint = models.ManyToManyField('endpoint.Endpoint', blank=True, related_name='practitioner_roles')
    
    # Note: Other fields implemented via reverse FK relationships:
    # - identifiers (0..* Identifier) via Identifier.practitioner_role
    # - codes (0..* CodeableConcept) via CodeableConcept.practitioner_role_code  
    # - specialties (0..* CodeableConcept) via CodeableConcept.practitioner_role_specialty
    # - characteristics (0..* CodeableConcept) via CodeableConcept.practitioner_role_characteristic
    # - communications (0..* CodeableConcept) via CodeableConcept.practitioner_role_communication
    # - contacts (0..* ExtendedContactDetail) via ExtendedContactDetail.practitioner_role
    # - healthcareServices (0..* Reference(HealthcareService)) via HealthcareService.practitioner_roles
    # - availabilities (0..* Availability) via Availability.practitioner_role
    
    class Meta:
        db_table = 'practitioner_role'
        indexes = [
            models.Index(fields=['active']),
            models.Index(fields=['practitioner']),
            models.Index(fields=['organization']),
        ]
    
    def __str__(self):
        return f"PractitionerRole(practitioner={self.practitioner}, organization={self.organization})"