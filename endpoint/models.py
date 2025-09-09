from django.db import models
from django.core.exceptions import ValidationError
from abstractClasses.models import DomainResource, BackboneElement


class EndpointPayload(BackboneElement):
    """Set of payloads that are provided by this endpoint"""
    # Endpoint this payload belongs to
    endpoint = models.ForeignKey('Endpoint', on_delete=models.CASCADE, related_name='payloads', null=True, blank=True)
    # The type of content that may be used at this endpoint (0..* CodeableConcept)
    # Note: CodeableConcept has reverse FK to EndpointPayload as 'payload_types'
    # Mimetype to send (0..* code)
    mimeType = models.JSONField(null=True, blank=True)  # Array of mime type codes
    
    class Meta:
        db_table = 'endpoint_payload_element'


class Endpoint(DomainResource):
    """The technical details of an endpoint that can be used for electronic services"""
    
    # Identifies this endpoint across multiple systems (0..* Identifier)
    # Note: Identifier has reverse FK to Endpoint as 'identifiers'
    
    # active | suspended | error | off | entered-in-error | test (1..1 code)
    status = models.CharField(max_length=32, choices=[
        ('active', 'Active'),
        ('suspended', 'Suspended'), 
        ('error', 'Error'),
        ('off', 'Off'),
        ('entered-in-error', 'Entered In Error'),
        ('test', 'Test')
    ])
    
    # Protocol/Profile/Standard to be used with this endpoint connection (1..* CodeableConcept)
    # Note: CodeableConcept has reverse FK to Endpoint as 'connection_types'
    
    # A name that this endpoint can be identified by (0..1 string)
    name = models.CharField(max_length=256, null=True, blank=True)
    
    # Additional details about the endpoint (0..1 string)
    description = models.TextField(null=True, blank=True)
    
    # The type of environment(s) exposed at this endpoint (0..* CodeableConcept)
    # Note: CodeableConcept has reverse FK to Endpoint as 'environment_types'
    
    # Organization that manages this endpoint (0..1 Reference(Organization))
    managingOrganization = models.ForeignKey('organization.Organization', null=True, blank=True, on_delete=models.SET_NULL, related_name='managed_endpoints')
    # Organization this endpoint belongs to (optional)
    organization = models.ForeignKey('organization.Organization', null=True, blank=True, on_delete=models.CASCADE, related_name='endpoints')
    # Practitioner role this endpoint belongs to (optional)
    practitioner_role = models.ForeignKey('practitioner.PractitionerRole', null=True, blank=True, on_delete=models.CASCADE, related_name='endpoints')
    # Healthcare service this endpoint belongs to (optional)
    healthcare_service = models.ForeignKey('healthcareservice.HealthcareService', null=True, blank=True, on_delete=models.CASCADE, related_name='endpoints')
    
    # Contact details for source (0..* ContactPoint)
    # Note: ContactDetail has reverse FK to Endpoint as 'contacts'
    
    # Interval the endpoint is expected to be operational (0..1 Period)
    period = models.ForeignKey('components.Period', null=True, blank=True, on_delete=models.SET_NULL, related_name='endpoints')
    
    # Set of payloads that are provided by this endpoint (0..* BackboneElement)
    # Note: EndpointPayload has reverse FK to Endpoint as 'payloads'
    
    # The technical base address for connecting to this endpoint (1..1 url)
    address = models.URLField(max_length=1024)
    
    # Usage depends on the channel type (0..* string)
    header = models.JSONField(null=True, blank=True)  # Array of header strings
    
    class Meta:
        db_table = 'endpoint'
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['address']),
        ]
    
    def clean(self):
        super().clean()
        # Ensure connectionType has at least one entry (1..* cardinality)
        if self.pk and not self.connection_types.exists():
            raise ValidationError("Endpoint.connectionType is required (1..* cardinality)")
    
    def __str__(self):
        return f"Endpoint(name={self.name}, address={self.address})"