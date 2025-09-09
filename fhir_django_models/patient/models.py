"""FHIR Patient resource models."""

from django.db import models
from django.contrib.contenttypes.fields import GenericRelation

from ..core.models import FHIRBaseModel, Identifier, HumanName, ContactPoint, Address


class Patient(FHIRBaseModel):
    """FHIR Patient resource."""
    
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
        ('unknown', 'Unknown'),
    ]
    
    # Patient identifiers (using generic relation)
    identifiers = GenericRelation(Identifier)
    
    # Active status
    active = models.BooleanField(default=True, help_text="Whether this patient record is in active use")
    
    # Patient names (using generic relation)
    names = GenericRelation(HumanName)
    
    # Contact details (using generic relation)
    telecoms = GenericRelation(ContactPoint)
    
    # Gender
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    
    # Birth date
    birth_date = models.DateField(blank=True, null=True)
    
    # Deceased status
    deceased_boolean = models.BooleanField(default=False, help_text="Indicates if the individual is deceased")
    deceased_date_time = models.DateTimeField(blank=True, null=True, help_text="Date/time of death")
    
    # Addresses (using generic relation)
    addresses = GenericRelation(Address)
    
    # Marital status (simplified)
    marital_status = models.CharField(max_length=50, blank=True, null=True, help_text="Marital status of patient")
    
    # Multiple birth
    multiple_birth_boolean = models.BooleanField(default=False, help_text="Whether patient is part of multiple birth")
    multiple_birth_integer = models.PositiveIntegerField(blank=True, null=True, help_text="Birth order")
    
    class Meta:
        db_table = 'fhir_patient'
        verbose_name = 'Patient'
        verbose_name_plural = 'Patients'
    
    def __str__(self):
        """String representation of the patient."""
        if self.names.exists():
            name = self.names.first()
            if name.text:
                return f"Patient: {name.text}"
            elif name.family or name.given:
                family = name.family or ""
                given = " ".join(name.given) if name.given else ""
                return f"Patient: {given} {family}".strip()
        return f"Patient: {self.id}"


class PatientContact(models.Model):
    """FHIR Patient.contact complex type."""
    
    RELATIONSHIP_CHOICES = [
        ('emergency', 'Emergency'),
        ('family', 'Family'),
        ('guardian', 'Guardian'),
        ('friend', 'Friend'),
        ('partner', 'Partner'),
        ('work', 'Work'),
        ('caregiver', 'Caregiver'),
        ('agent', 'Agent'),
    ]
    
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
        ('unknown', 'Unknown'),
    ]
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='contacts')
    
    # Relationship to patient
    relationship = models.CharField(max_length=20, choices=RELATIONSHIP_CHOICES, blank=True, null=True)
    
    # Contact's name
    names = GenericRelation(HumanName)
    
    # Contact's telecom
    telecoms = GenericRelation(ContactPoint)
    
    # Contact's address
    address = GenericRelation(Address)
    
    # Contact's gender
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    
    # Organization reference (simplified as CharField for now)
    organization = models.CharField(max_length=255, blank=True, null=True, help_text="Organization that is associated with the contact")
    
    class Meta:
        db_table = 'fhir_patient_contact'
        verbose_name = 'Patient Contact'
        verbose_name_plural = 'Patient Contacts'
    
    def __str__(self):
        """String representation of the patient contact."""
        if self.names.exists():
            name = self.names.first()
            if name.text:
                return f"Contact: {name.text}"
        return f"Contact for Patient: {self.patient.id}"


class PatientCommunication(models.Model):
    """FHIR Patient.communication complex type."""
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='communications')
    
    # Language (simplified as CharField)
    language = models.CharField(max_length=10, help_text="Language code (e.g., en, es, fr)")
    language_display = models.CharField(max_length=255, blank=True, null=True, help_text="Language display name")
    
    # Preferred communication language
    preferred = models.BooleanField(default=False, help_text="Language preference indicator")
    
    class Meta:
        db_table = 'fhir_patient_communication'
        verbose_name = 'Patient Communication'
        verbose_name_plural = 'Patient Communications'
    
    def __str__(self):
        """String representation of the patient communication."""
        return f"Communication: {self.language_display or self.language} for Patient: {self.patient.id}"