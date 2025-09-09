"""FHIR Observation resource models."""

from django.db import models
from django.contrib.contenttypes.fields import GenericRelation

from ..core.models import FHIRBaseModel, Identifier, CodeableConcept
from ..patient.models import Patient
from ..practitioner.models import Practitioner


class Observation(FHIRBaseModel):
    """FHIR Observation resource."""
    
    STATUS_CHOICES = [
        ('registered', 'Registered'),
        ('preliminary', 'Preliminary'),
        ('final', 'Final'),
        ('amended', 'Amended'),
        ('corrected', 'Corrected'),
        ('cancelled', 'Cancelled'),
        ('entered-in-error', 'Entered in Error'),
        ('unknown', 'Unknown'),
    ]
    
    # Observation identifiers
    identifiers = GenericRelation(Identifier)
    
    # Status of the observation
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, help_text="Status of the observation")
    
    # Classification of type of observation
    category = GenericRelation(CodeableConcept, related_query_name='observation_categories')
    
    # Type of observation (what was observed)
    code = GenericRelation(CodeableConcept, related_query_name='observation_codes')
    
    # Who/what this observation is about
    subject_patient = models.ForeignKey(Patient, on_delete=models.CASCADE, blank=True, null=True, related_name='observations')
    
    # Healthcare event during which this observation was made
    encounter = models.CharField(max_length=255, blank=True, null=True, help_text="Healthcare encounter reference")
    
    # Clinically relevant time/time-period for observation
    effective_date_time = models.DateTimeField(blank=True, null=True, help_text="Clinically relevant time")
    effective_period_start = models.DateTimeField(blank=True, null=True, help_text="Start of relevant period")
    effective_period_end = models.DateTimeField(blank=True, null=True, help_text="End of relevant period")
    
    # When observation was made
    issued = models.DateTimeField(blank=True, null=True, help_text="Date/Time this observation was made available")
    
    # Who is responsible for the observation
    performer_practitioner = models.ForeignKey(Practitioner, on_delete=models.SET_NULL, blank=True, null=True, related_name='observations')
    
    # Actual result value
    value_quantity_value = models.DecimalField(max_digits=20, decimal_places=6, blank=True, null=True, help_text="Numerical value")
    value_quantity_unit = models.CharField(max_length=50, blank=True, null=True, help_text="Unit of measurement")
    value_quantity_system = models.URLField(blank=True, null=True, help_text="Unit system")
    value_quantity_code = models.CharField(max_length=50, blank=True, null=True, help_text="Coded form of the unit")
    
    value_string = models.TextField(blank=True, null=True, help_text="String value")
    value_boolean = models.BooleanField(blank=True, null=True, help_text="Boolean value")
    value_date_time = models.DateTimeField(blank=True, null=True, help_text="DateTime value")
    
    # Interpretation of the observation
    interpretation = GenericRelation(CodeableConcept, related_query_name='observation_interpretations')
    
    # Comments about the observation
    note = models.TextField(blank=True, null=True, help_text="Comments about the observation")
    
    # Body site
    body_site = GenericRelation(CodeableConcept, related_query_name='observation_body_sites')
    
    # Method used
    method = GenericRelation(CodeableConcept, related_query_name='observation_methods')
    
    class Meta:
        db_table = 'fhir_observation'
        verbose_name = 'Observation'
        verbose_name_plural = 'Observations'
    
    def __str__(self):
        """String representation of the observation."""
        code_text = "Unknown"
        if self.code.exists():
            code_obj = self.code.first()
            code_text = code_obj.text or "Coded observation"
        
        subject_text = "Unknown subject"
        if self.subject_patient:
            subject_text = str(self.subject_patient)
        
        return f"Observation: {code_text} for {subject_text}"


class ObservationComponent(models.Model):
    """FHIR Observation.component complex type."""
    
    observation = models.ForeignKey(Observation, on_delete=models.CASCADE, related_name='components')
    
    # Type of component observation
    code = GenericRelation(CodeableConcept, related_query_name='observation_component_codes')
    
    # Component result value
    value_quantity_value = models.DecimalField(max_digits=20, decimal_places=6, blank=True, null=True)
    value_quantity_unit = models.CharField(max_length=50, blank=True, null=True)
    value_quantity_system = models.URLField(blank=True, null=True)
    value_quantity_code = models.CharField(max_length=50, blank=True, null=True)
    
    value_string = models.TextField(blank=True, null=True)
    value_boolean = models.BooleanField(blank=True, null=True)
    value_date_time = models.DateTimeField(blank=True, null=True)
    
    # Component interpretation
    interpretation = GenericRelation(CodeableConcept, related_query_name='observation_component_interpretations')
    
    class Meta:
        db_table = 'fhir_observation_component'
        verbose_name = 'Observation Component'
        verbose_name_plural = 'Observation Components'
    
    def __str__(self):
        """String representation of the observation component."""
        code_text = "Component"
        if self.code.exists():
            code_obj = self.code.first()
            code_text = code_obj.text or "Coded component"
        return f"{code_text} of {self.observation}"