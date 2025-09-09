"""Core FHIR Django models and base classes."""

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class FHIRBaseModel(models.Model):
    """Base model for all FHIR resources."""
    
    id = models.CharField(max_length=64, primary_key=True, help_text="Logical id of this artifact")
    meta_version_id = models.CharField(max_length=64, blank=True, null=True, help_text="Version specific identifier")
    meta_last_updated = models.DateTimeField(auto_now=True, help_text="When the resource last updated")
    
    class Meta:
        abstract = True


class Identifier(models.Model):
    """FHIR Identifier complex type."""
    
    USE_CHOICES = [
        ('usual', 'Usual'),
        ('official', 'Official'),
        ('temp', 'Temp'),
        ('secondary', 'Secondary'),
        ('old', 'Old'),
    ]
    
    use = models.CharField(max_length=20, choices=USE_CHOICES, blank=True, null=True)
    system = models.URLField(blank=True, null=True, help_text="The namespace for the identifier value")
    value = models.CharField(max_length=255, help_text="The value that is unique")
    
    # Generic relation to link to any FHIR resource
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.CharField(max_length=64)
    content_object = GenericForeignKey('content_type', 'object_id')
    
    class Meta:
        db_table = 'fhir_identifier'


class CodeableConcept(models.Model):
    """FHIR CodeableConcept complex type."""
    
    text = models.TextField(blank=True, null=True, help_text="Plain text representation of the concept")
    
    # Generic relation to link to any FHIR resource
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.CharField(max_length=64)
    content_object = GenericForeignKey('content_type', 'object_id')
    
    class Meta:
        db_table = 'fhir_codeable_concept'


class Coding(models.Model):
    """FHIR Coding complex type."""
    
    system = models.URLField(blank=True, null=True, help_text="Identity of the terminology system")
    version = models.CharField(max_length=255, blank=True, null=True, help_text="Version of the system")
    code = models.CharField(max_length=255, blank=True, null=True, help_text="Symbol in syntax defined by the system")
    display = models.CharField(max_length=255, blank=True, null=True, help_text="Representation defined by the system")
    user_selected = models.BooleanField(default=False, help_text="If this coding was chosen by a user")
    
    codeable_concept = models.ForeignKey(CodeableConcept, on_delete=models.CASCADE, related_name='codings')
    
    class Meta:
        db_table = 'fhir_coding'


class HumanName(models.Model):
    """FHIR HumanName complex type."""
    
    USE_CHOICES = [
        ('usual', 'Usual'),
        ('official', 'Official'),
        ('temp', 'Temp'),
        ('nickname', 'Nickname'),
        ('anonymous', 'Anonymous'),
        ('old', 'Old'),
        ('maiden', 'Maiden'),
    ]
    
    use = models.CharField(max_length=20, choices=USE_CHOICES, blank=True, null=True)
    text = models.CharField(max_length=255, blank=True, null=True, help_text="Full name as displayed")
    family = models.CharField(max_length=255, blank=True, null=True, help_text="Family name")
    given = models.JSONField(default=list, blank=True, help_text="Given names (not always 'first'). List of strings")
    prefix = models.JSONField(default=list, blank=True, help_text="Parts that come before the name. List of strings")
    suffix = models.JSONField(default=list, blank=True, help_text="Parts that come after the name. List of strings")
    
    # Generic relation to link to any FHIR resource
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.CharField(max_length=64)
    content_object = GenericForeignKey('content_type', 'object_id')
    
    class Meta:
        db_table = 'fhir_human_name'


class ContactPoint(models.Model):
    """FHIR ContactPoint complex type."""
    
    SYSTEM_CHOICES = [
        ('phone', 'Phone'),
        ('fax', 'Fax'),
        ('email', 'Email'),
        ('pager', 'Pager'),
        ('url', 'URL'),
        ('sms', 'SMS'),
        ('other', 'Other'),
    ]
    
    USE_CHOICES = [
        ('home', 'Home'),
        ('work', 'Work'),
        ('temp', 'Temp'),
        ('old', 'Old'),
        ('mobile', 'Mobile'),
    ]
    
    system = models.CharField(max_length=20, choices=SYSTEM_CHOICES, blank=True, null=True)
    value = models.CharField(max_length=255, blank=True, null=True, help_text="The actual contact point details")
    use = models.CharField(max_length=20, choices=USE_CHOICES, blank=True, null=True)
    rank = models.PositiveIntegerField(blank=True, null=True, help_text="Specify preferred order of use (1 = highest)")
    
    # Generic relation to link to any FHIR resource
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.CharField(max_length=64)
    content_object = GenericForeignKey('content_type', 'object_id')
    
    class Meta:
        db_table = 'fhir_contact_point'


class Address(models.Model):
    """FHIR Address complex type."""
    
    USE_CHOICES = [
        ('home', 'Home'),
        ('work', 'Work'),
        ('temp', 'Temporary'),
        ('old', 'Old / Incorrect'),
        ('billing', 'Billing'),
    ]
    
    TYPE_CHOICES = [
        ('postal', 'Postal'),
        ('physical', 'Physical'),
        ('both', 'Both'),
    ]
    
    use = models.CharField(max_length=20, choices=USE_CHOICES, blank=True, null=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, blank=True, null=True)
    text = models.TextField(blank=True, null=True, help_text="Full address as displayed")
    line = models.JSONField(default=list, blank=True, help_text="Street name, number, direction & P.O. Box etc. List of strings")
    city = models.CharField(max_length=255, blank=True, null=True)
    district = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    
    # Generic relation to link to any FHIR resource
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.CharField(max_length=64)
    content_object = GenericForeignKey('content_type', 'object_id')
    
    class Meta:
        db_table = 'fhir_address'