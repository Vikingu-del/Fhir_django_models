from django.db import models
from django.core.exceptions import ValidationError
from abstractClasses.models import DomainResource, BackboneElement


class LocationPosition(BackboneElement):
    """The absolute geographic location"""
    # Location this position belongs to
    location = models.OneToOneField('Location', on_delete=models.CASCADE, related_name='position', null=True, blank=True)
    # Longitude with WGS84 datum (1..1 decimal)
    longitude = models.DecimalField(max_digits=10, decimal_places=7)
    # Latitude with WGS84 datum (1..1 decimal)
    latitude = models.DecimalField(max_digits=10, decimal_places=7)
    # Altitude with WGS84 datum (0..1 decimal)
    altitude = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    
    class Meta:
        db_table = 'location_position'


class Location(DomainResource):
    """Details and position information for a place"""
    
    # active | suspended | inactive (0..1 code)
    status = models.CharField(max_length=16, null=True, blank=True, choices=[
        ('active', 'Active'), ('suspended', 'Suspended'), ('inactive', 'Inactive')
    ])
    
    # The operational status of the location (0..1 Coding)
    operationalStatus = models.ForeignKey('components.Coding', null=True, blank=True, on_delete=models.SET_NULL, related_name='location_operational_status')
    
    # Name of the location as used by humans (0..1 string)
    name = models.CharField(max_length=256, null=True, blank=True)
    
    # A list of alternate names (0..* string)
    alias = models.JSONField(null=True, blank=True)  # Array of strings
    
    # Additional details about the location (0..1 markdown)
    description = models.TextField(null=True, blank=True)
    
    # instance | kind (0..1 code)
    mode = models.CharField(max_length=16, null=True, blank=True, choices=[
        ('instance', 'Instance'), ('kind', 'Kind')
    ])
    
    # Physical location (0..1 Address)
    address = models.ForeignKey('components.Address', null=True, blank=True, on_delete=models.SET_NULL, related_name='locations')
    
    # Organization responsible for provisioning and upkeep (0..1 Reference(Organization))
    managingOrganization = models.ForeignKey('organization.Organization', null=True, blank=True, on_delete=models.SET_NULL, related_name='managed_locations')
    
    # Another Location this one is physically a part of (0..1 Reference(Location))
    partOf = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='child_locations')
    
    # Technical endpoints providing access to services (0..* Reference(Endpoint))
    endpoint = models.ManyToManyField('endpoint.Endpoint', blank=True, related_name='locations')
    
    class Meta:
        db_table = 'location'
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['name']),
            models.Index(fields=['managingOrganization']),
        ]
    
    def __str__(self):
        return f"Location(name={self.name}, status={self.status})"