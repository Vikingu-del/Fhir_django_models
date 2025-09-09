from django.db import models
from django.core.exceptions import ValidationError
from abstractClasses.models import DomainResource, BackboneElement


class HealthcareServiceEligibility(BackboneElement):
    """Specific eligibility requirements required to use the service"""
    # HealthcareService this eligibility belongs to
    healthcare_service = models.ForeignKey('HealthcareService', on_delete=models.CASCADE, related_name='eligibilities', null=True, blank=True)
    # Coded value for the eligibility (0..1 CodeableConcept)
    code = models.ForeignKey('components.CodeableConcept', null=True, blank=True, on_delete=models.SET_NULL, related_name='healthcare_service_eligibilities')
    # Describes the eligibility conditions for the service (0..1 markdown)
    comment = models.TextField(null=True, blank=True)
    
    class Meta:
        db_table = 'healthcare_service_eligibility'


class HealthcareService(DomainResource):
    """The details of a healthcare service available at a location"""
    
    # Whether this HealthcareService record is in active use (0..1 boolean)
    active = models.BooleanField(null=True, blank=True)
    
    # Organization that provides this service (0..1 Reference(Organization))
    providedBy = models.ForeignKey('organization.Organization', null=True, blank=True, on_delete=models.SET_NULL, related_name='provided_healthcare_services')
    
    # The service within which this service is offered (0..* Reference(HealthcareService))
    offeredIn = models.ManyToManyField('self', blank=True, related_name='offered_services', symmetrical=False)
    
    # Location(s) where service may be provided (0..* Reference(Location))
    location = models.ManyToManyField('location.Location', blank=True, related_name='healthcare_services')
    
    # Description of service as presented to a consumer while searching (0..1 string)
    name = models.CharField(max_length=256, null=True, blank=True)
    
    # Additional description and/or any specific issues not covered elsewhere (0..1 markdown)
    comment = models.TextField(null=True, blank=True)
    
    # Extra details about the service that can't be placed in the other fields (0..1 markdown)
    extraDetails = models.TextField(null=True, blank=True)
    
    # Facilitates quick identification of the service (0..1 Attachment)
    photo = models.ForeignKey('components.Attachment', null=True, blank=True, on_delete=models.SET_NULL, related_name='healthcare_services')
    
    # Location(s) service is intended for/available to (0..* Reference(Location))
    coverageArea = models.ManyToManyField('location.Location', blank=True, related_name='coverage_healthcare_services')
    
    # If an appointment is required for access to this service (0..1 boolean)
    appointmentRequired = models.BooleanField(null=True, blank=True)
    
    # Technical endpoints providing access to electronic services (0..* Reference(Endpoint))
    endpoint = models.ManyToManyField('endpoint.Endpoint', blank=True, related_name='healthcare_services')
    
    # Practitioner roles that provide this healthcare service (0..* Reference(PractitionerRole))
    practitioner_roles = models.ManyToManyField('practitioner.PractitionerRole', blank=True, related_name='healthcare_services')
    
    class Meta:
        db_table = 'healthcare_service'
        indexes = [
            models.Index(fields=['active']),
            models.Index(fields=['name']),
            models.Index(fields=['providedBy']),
            models.Index(fields=['appointmentRequired']),
        ]
    
    def __str__(self):
        return f"HealthcareService(name={self.name}, active={self.active})"