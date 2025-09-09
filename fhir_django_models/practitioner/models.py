"""FHIR Practitioner resource models."""

from django.db import models
from django.contrib.contenttypes.fields import GenericRelation

from ..core.models import FHIRBaseModel, Identifier, HumanName, ContactPoint, Address


class Practitioner(FHIRBaseModel):
    """FHIR Practitioner resource."""
    
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
        ('unknown', 'Unknown'),
    ]
    
    # Practitioner identifiers
    identifiers = GenericRelation(Identifier)
    
    # Active status
    active = models.BooleanField(default=True, help_text="Whether this practitioner record is in active use")
    
    # Practitioner names
    names = GenericRelation(HumanName)
    
    # Contact details
    telecoms = GenericRelation(ContactPoint)
    
    # Addresses
    addresses = GenericRelation(Address)
    
    # Gender
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    
    # Birth date
    birth_date = models.DateField(blank=True, null=True)
    
    # Photo (simplified as URL)
    photo_url = models.URLField(blank=True, null=True, help_text="URL to practitioner photo")
    
    class Meta:
        db_table = 'fhir_practitioner'
        verbose_name = 'Practitioner'
        verbose_name_plural = 'Practitioners'
    
    def __str__(self):
        """String representation of the practitioner."""
        if self.names.exists():
            name = self.names.first()
            if name.text:
                return f"Practitioner: {name.text}"
            elif name.family or name.given:
                family = name.family or ""
                given = " ".join(name.given) if name.given else ""
                return f"Practitioner: {given} {family}".strip()
        return f"Practitioner: {self.id}"


class PractitionerQualification(models.Model):
    """FHIR Practitioner.qualification complex type."""
    
    practitioner = models.ForeignKey(Practitioner, on_delete=models.CASCADE, related_name='qualifications')
    
    # Identifiers for this qualification
    identifiers = GenericRelation(Identifier)
    
    # Coded representation of the qualification
    code = models.CharField(max_length=255, help_text="Coded representation of the qualification")
    code_display = models.CharField(max_length=255, blank=True, null=True, help_text="Display name for the qualification")
    
    # Period when qualification is/was valid
    period_start = models.DateTimeField(blank=True, null=True, help_text="Start of qualification period")
    period_end = models.DateTimeField(blank=True, null=True, help_text="End of qualification period")
    
    # Organization that issued the qualification (simplified)
    issuer = models.CharField(max_length=255, blank=True, null=True, help_text="Organization that regulates and issues the qualification")
    
    class Meta:
        db_table = 'fhir_practitioner_qualification'
        verbose_name = 'Practitioner Qualification'
        verbose_name_plural = 'Practitioner Qualifications'
    
    def __str__(self):
        """String representation of the practitioner qualification."""
        return f"Qualification: {self.code_display or self.code} for {self.practitioner}"