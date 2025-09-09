from django.db import models
from django.core.exceptions import ValidationError
from abstractClasses.models import DomainResource, BackboneElement


class PatientContact(BackboneElement):
    """A contact party for the patient"""
    # Patient this contact belongs to
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE, related_name='contacts', null=True, blank=True)
    # A name associated with the contact person (0..1 HumanName)
    name = models.ForeignKey('components.HumanName', null=True, blank=True, on_delete=models.SET_NULL, related_name='patient_contacts')
    # Address for the contact person (0..1 Address)
    address = models.ForeignKey('components.Address', null=True, blank=True, on_delete=models.SET_NULL, related_name='patient_contacts')
    # male | female | other | unknown (0..1 code)
    gender = models.CharField(max_length=16, null=True, blank=True, choices=[
        ('male', 'Male'), ('female', 'Female'), ('other', 'Other'), ('unknown', 'Unknown')
    ])
    # Organization that is associated with the contact (0..1 Reference(Organization))
    organization = models.ForeignKey('organization.Organization', null=True, blank=True, on_delete=models.SET_NULL, related_name='patient_contacts')
    # The period during which this contact is valid (0..1 Period)
    period = models.ForeignKey('components.Period', null=True, blank=True, on_delete=models.SET_NULL, related_name='patient_contacts')
    
    class Meta:
        db_table = 'patient_contact'
    
    def clean(self):
        super().clean()
        # FHIR Rule: SHALL at least contain a contact's details or a reference to an organization
        has_telecom = hasattr(self, 'telecom_points') and self.telecom_points.exists()
        if not (self.name or has_telecom or self.address or self.organization):
            raise ValidationError("Patient contact must have name, telecom, address, or organization")


class PatientCommunication(BackboneElement):
    """A language which may be used to communicate with the patient"""
    # Patient this communication belongs to
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE, related_name='communications', null=True, blank=True)
    # The language which can be used to communicate (1..1 CodeableConcept)
    language = models.ForeignKey('components.CodeableConcept', on_delete=models.CASCADE, related_name='patient_communications')
    # Language preference indicator (0..1 boolean)
    preferred = models.BooleanField(null=True, blank=True)
    
    class Meta:
        db_table = 'patient_communication'


class PatientLink(BackboneElement):
    """Link to another patient or related person resource"""
    # Patient this link belongs to
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE, related_name='links', null=True, blank=True)
    # The other patient or related person resource (1..1 Reference(Patient | RelatedPerson))
    other_patient = models.ForeignKey('Patient', null=True, blank=True, on_delete=models.CASCADE, related_name='linked_from')
    other_related_person = models.ForeignKey('RelatedPerson', null=True, blank=True, on_delete=models.CASCADE, related_name='linked_from')
    # replaced-by | replaces | refer | seealso (1..1 code)
    type = models.CharField(max_length=16, choices=[
        ('replaced-by', 'Replaced By'), ('replaces', 'Replaces'), 
        ('refer', 'Refer'), ('seealso', 'See Also')
    ])
    
    class Meta:
        db_table = 'patient_link'
    
    def clean(self):
        super().clean()
        # FHIR Rule: exactly one other reference must be set
        others = [self.other_patient, self.other_related_person]
        set_others = [o for o in others if o is not None]
        if len(set_others) != 1:
            raise ValidationError("PatientLink must reference exactly one other Patient or RelatedPerson")


class Patient(DomainResource):
    """Information about an individual or animal receiving health care services"""
    
    # Whether this patient's record is in active use (0..1 boolean)
    active = models.BooleanField(null=True, blank=True)
    
    # male | female | other | unknown (0..1 code)
    gender = models.CharField(max_length=16, null=True, blank=True, choices=[
        ('male', 'Male'), ('female', 'Female'), ('other', 'Other'), ('unknown', 'Unknown')
    ])
    
    # The date of birth for the individual (0..1 date)
    birthDate = models.DateField(null=True, blank=True)
    
    # Indicates if the individual is deceased (0..1 choice)
    deceasedBoolean = models.BooleanField(null=True, blank=True)
    deceasedDateTime = models.DateTimeField(null=True, blank=True)
    
    # Marital status of a patient (0..1 CodeableConcept)
    maritalStatus = models.ForeignKey('components.CodeableConcept', null=True, blank=True, on_delete=models.SET_NULL, related_name='patient_marital_status')
    
    # Whether patient is part of a multiple birth (0..1 choice)
    multipleBirthBoolean = models.BooleanField(null=True, blank=True)
    multipleBirthInteger = models.IntegerField(null=True, blank=True)
    
    # Patient's nominated primary care provider (0..* Reference(Organization | Practitioner | PractitionerRole))
    generalPractitioner = models.ManyToManyField('practitioner.Practitioner', blank=True, related_name='patients')
    generalPractitionerRole = models.ManyToManyField('practitioner.PractitionerRole', blank=True, related_name='patients')
    generalPractitionerOrg = models.ManyToManyField('organization.Organization', blank=True, related_name='patients')
    
    # Organization that is the custodian of the patient record (0..1 Reference(Organization))
    managingOrganization = models.ForeignKey('organization.Organization', null=True, blank=True, on_delete=models.SET_NULL, related_name='managed_patients')
    
    class Meta:
        db_table = 'patient'
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
        # FHIR invariant: only one multipleBirth[x] can be set
        if self.multipleBirthBoolean is not None and self.multipleBirthInteger is not None:
            raise ValidationError("Only one multipleBirth[x] field can be set")
    
    def __str__(self):
        return f"Patient(id={self.fhir_id}, active={self.active})"


class RelatedPersonCommunication(BackboneElement):
    """A language which may be used to communicate with the related person"""
    # RelatedPerson this communication belongs to
    related_person = models.ForeignKey('RelatedPerson', on_delete=models.CASCADE, related_name='communications', null=True, blank=True)
    # The language which can be used to communicate (1..1 CodeableConcept)
    language = models.ForeignKey('components.CodeableConcept', on_delete=models.CASCADE, related_name='related_person_communications')
    # Language preference indicator (0..1 boolean)
    preferred = models.BooleanField(null=True, blank=True)
    
    class Meta:
        db_table = 'related_person_communication'


class RelatedPerson(DomainResource):
    """A person that is related to a patient, but who is not a direct target of care"""
    
    # Whether this related person's record is in active use (0..1 boolean)
    active = models.BooleanField(null=True, blank=True)
    
    # The patient this person is related to (1..1 Reference(Patient))
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE, related_name='related_persons')
    
    # male | female | other | unknown (0..1 code)
    gender = models.CharField(max_length=16, null=True, blank=True, choices=[
        ('male', 'Male'), ('female', 'Female'), ('other', 'Other'), ('unknown', 'Unknown')
    ])
    
    # The date on which the related person was born (0..1 date)
    birthDate = models.DateField(null=True, blank=True)
    
    # Period of time that this relationship is considered valid (0..1 Period)
    period = models.ForeignKey('components.Period', null=True, blank=True, on_delete=models.SET_NULL, related_name='related_persons')
    
    class Meta:
        db_table = 'related_person'
        indexes = [
            models.Index(fields=['active']),
            models.Index(fields=['patient']),
            models.Index(fields=['gender']),
        ]
    
    def __str__(self):
        return f"RelatedPerson(patient={self.patient}, active={self.active})"