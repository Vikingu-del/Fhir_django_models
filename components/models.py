from django.db import models
from django.core.exceptions import ValidationError
from abstractClasses.models import *
import bleach


# Create your models here.

### Complex data types ###

class Identifier(Element):
    """An identifier intended for computation"""
    # usual | official | temp | secondary | old (0..1 code)
    use = models.CharField(max_length=16, null=True, blank=True, choices=[
        ('usual', 'Usual'), ('official', 'Official'), ('temp', 'Temp'),
        ('secondary', 'Secondary'), ('old', 'Old')
    ])
    # Description of identifier (0..1 CodeableConcept)
    type = models.ForeignKey('CodeableConcept', null=True, blank=True, on_delete=models.SET_NULL, related_name='identifiers')
    # The namespace for the identifier value (0..1 uri)
    system = models.URLField(max_length=512, null=True, blank=True)
    # The value that is unique (0..1 string)
    value = models.CharField(max_length=256, null=True, blank=True)
    # Time period when id is/was valid for use (0..1 Period)
    period = models.ForeignKey('Period', null=True, blank=True, on_delete=models.SET_NULL, related_name='identifiers')
    # Organization that issued id (0..1 Reference(Organization))
    assigner = models.ForeignKey('organization.Organization', null=True, blank=True, on_delete=models.SET_NULL, related_name='assigned_identifiers')
    # Organization qualification this identifier belongs to (optional)
    qualification = models.ForeignKey('organization.OrganizationQualification', null=True, blank=True, on_delete=models.CASCADE, related_name='identifiers')
    # Organization this identifier belongs to (optional)
    organization = models.ForeignKey('organization.Organization', null=True, blank=True, on_delete=models.CASCADE, related_name='identifiers')
    # Endpoint this identifier belongs to (optional)
    endpoint = models.ForeignKey('endpoint.Endpoint', null=True, blank=True, on_delete=models.CASCADE, related_name='identifiers')
    # Practitioner this identifier belongs to (optional)
    practitioner = models.ForeignKey('practitioner.Practitioner', null=True, blank=True, on_delete=models.CASCADE, related_name='identifiers')
    # Practitioner qualification this identifier belongs to (optional)
    practitioner_qualification = models.ForeignKey('practitioner.PractitionerQualification', null=True, blank=True, on_delete=models.CASCADE, related_name='identifiers')
    # Practitioner role this identifier belongs to (optional)
    practitioner_role = models.ForeignKey('practitioner.PractitionerRole', null=True, blank=True, on_delete=models.CASCADE, related_name='identifiers')
    # Healthcare service this identifier belongs to (optional)
    healthcare_service = models.ForeignKey('healthcareservice.HealthcareService', null=True, blank=True, on_delete=models.CASCADE, related_name='identifiers')
    # Patient this identifier belongs to (optional)
    patient = models.ForeignKey('patient.Patient', null=True, blank=True, on_delete=models.CASCADE, related_name='identifiers')
    # RelatedPerson this identifier belongs to (optional)
    related_person = models.ForeignKey('patient.RelatedPerson', null=True, blank=True, on_delete=models.CASCADE, related_name='identifiers')
    # Citation this identifier belongs to (optional)
    citation = models.ForeignKey('citation.Citation', null=True, blank=True, on_delete=models.CASCADE, related_name='identifiers')
    # CitedArtifact this identifier belongs to (optional)
    cited_artifact = models.ForeignKey('citation.CitedArtifact', null=True, blank=True, on_delete=models.CASCADE, related_name='identifiers')
    # CitedArtifact related identifier (optional)
    cited_artifact_related = models.ForeignKey('citation.CitedArtifact', null=True, blank=True, on_delete=models.CASCADE, related_name='related_identifiers')
    # CitedArtifactPublicationFormPublishedIn this identifier belongs to (optional)
    published_in = models.ForeignKey('citation.CitedArtifactPublicationFormPublishedIn', null=True, blank=True, on_delete=models.CASCADE, related_name='identifiers')
    
    class Meta:
        db_table = 'identifier'
        indexes = [
            models.Index(fields=['system', 'value']),
            models.Index(fields=['use']),
        ]

class CodeableConcept(Element):
    """Concept - reference to a terminology or just text"""
    # Code defined by a terminology system (0..* Coding)
    # Note: Coding has reverse FK to CodeableConcept as 'codings'
    # Plain text representation of the concept (0..1 string)
    text = models.CharField(max_length=256, null=True, blank=True)
    # Organization this type belongs to (optional)
    organization_type = models.ForeignKey('organization.Organization', null=True, blank=True, on_delete=models.CASCADE, related_name='org_types')
    # Endpoint connection type (optional)
    endpoint_connection = models.ForeignKey('endpoint.Endpoint', null=True, blank=True, on_delete=models.CASCADE, related_name='connection_types')
    # Endpoint environment type (optional)
    endpoint_environment = models.ForeignKey('endpoint.Endpoint', null=True, blank=True, on_delete=models.CASCADE, related_name='environment_types')
    # Endpoint payload type (optional)
    endpoint_payload = models.ForeignKey('endpoint.EndpointPayload', null=True, blank=True, on_delete=models.CASCADE, related_name='payload_types')
    # Practitioner role code (optional)
    practitioner_role_code = models.ForeignKey('practitioner.PractitionerRole', null=True, blank=True, on_delete=models.CASCADE, related_name='codes')
    # Practitioner role specialty (optional)
    practitioner_role_specialty = models.ForeignKey('practitioner.PractitionerRole', null=True, blank=True, on_delete=models.CASCADE, related_name='specialties')
    # Practitioner role characteristic (optional)
    practitioner_role_characteristic = models.ForeignKey('practitioner.PractitionerRole', null=True, blank=True, on_delete=models.CASCADE, related_name='characteristics')
    # Practitioner role communication (optional)
    practitioner_role_communication = models.ForeignKey('practitioner.PractitionerRole', null=True, blank=True, on_delete=models.CASCADE, related_name='communications')
    # Healthcare service category (optional)
    healthcare_service_category = models.ForeignKey('healthcareservice.HealthcareService', null=True, blank=True, on_delete=models.CASCADE, related_name='categories')
    # Healthcare service type (optional)
    healthcare_service_type = models.ForeignKey('healthcareservice.HealthcareService', null=True, blank=True, on_delete=models.CASCADE, related_name='types')
    # Healthcare service specialty (optional)
    healthcare_service_specialty = models.ForeignKey('healthcareservice.HealthcareService', null=True, blank=True, on_delete=models.CASCADE, related_name='specialties')
    # Healthcare service provision code (optional)
    healthcare_service_provision = models.ForeignKey('healthcareservice.HealthcareService', null=True, blank=True, on_delete=models.CASCADE, related_name='service_provision_codes')
    # Healthcare service program (optional)
    healthcare_service_program = models.ForeignKey('healthcareservice.HealthcareService', null=True, blank=True, on_delete=models.CASCADE, related_name='programs')
    # Healthcare service characteristic (optional)
    healthcare_service_characteristic = models.ForeignKey('healthcareservice.HealthcareService', null=True, blank=True, on_delete=models.CASCADE, related_name='characteristics')
    # Healthcare service communication (optional)
    healthcare_service_communication = models.ForeignKey('healthcareservice.HealthcareService', null=True, blank=True, on_delete=models.CASCADE, related_name='communications')
    # Healthcare service referral method (optional)
    healthcare_service_referral = models.ForeignKey('healthcareservice.HealthcareService', null=True, blank=True, on_delete=models.CASCADE, related_name='referral_methods')
    # Location type (optional)
    location_type = models.ForeignKey('location.Location', null=True, blank=True, on_delete=models.CASCADE, related_name='types')
    # Location form (optional)
    location_form = models.ForeignKey('location.Location', null=True, blank=True, on_delete=models.CASCADE, related_name='forms')
    # Location characteristic (optional)
    location_characteristic = models.ForeignKey('location.Location', null=True, blank=True, on_delete=models.CASCADE, related_name='characteristics')
    # Patient contact relationship (optional)
    patient_contact_relationship = models.ForeignKey('patient.PatientContact', null=True, blank=True, on_delete=models.CASCADE, related_name='relationships')
    # RelatedPerson relationship (optional)
    related_person_relationship = models.ForeignKey('patient.RelatedPerson', null=True, blank=True, on_delete=models.CASCADE, related_name='relationships')
    # Citation current state (optional)
    citation_current_state = models.ForeignKey('citation.Citation', null=True, blank=True, on_delete=models.CASCADE, related_name='current_states')
    # Citation classification classifier (optional)
    citation_classification_classifier = models.ForeignKey('citation.CitationClassification', null=True, blank=True, on_delete=models.CASCADE, related_name='classifiers')
    
    class Meta:
        db_table = 'codeable_concept'

class ContactPoint(Element):
    """Details of a Technology mediated contact point (phone, fax, email, etc.)"""
    # ContactDetail this belongs to
    contact_detail = models.ForeignKey('ContactDetail', on_delete=models.CASCADE, related_name='telecom_points', null=True, blank=True)
    # phone | fax | email | pager | url | sms | other (0..1 code)
    system = models.CharField(max_length=16, null=True, blank=True, choices=[
        ('phone', 'Phone'), ('fax', 'Fax'), ('email', 'Email'), 
        ('pager', 'Pager'), ('url', 'URL'), ('sms', 'SMS'), ('other', 'Other')
    ])
    # The actual contact point details (0..1 string)
    value = models.CharField(max_length=256, null=True, blank=True)
    # home | work | temp | old | mobile - purpose of this contact point (0..1 code)
    use = models.CharField(max_length=16, null=True, blank=True, choices=[
        ('home', 'Home'), ('work', 'Work'), ('temp', 'Temp'), 
        ('old', 'Old'), ('mobile', 'Mobile')
    ])
    # Specify preferred order of use (1 = highest) (0..1 positiveInt)
    rank = models.PositiveIntegerField(null=True, blank=True)
    # Time period when the contact point was/is in use (0..1 Period)
    period = models.ForeignKey('Period', null=True, blank=True, on_delete=models.SET_NULL, related_name='contact_points')
    # Practitioner this contact point belongs to (optional)
    practitioner = models.ForeignKey('practitioner.Practitioner', null=True, blank=True, on_delete=models.CASCADE, related_name='telecom_points')
    # Extended contact detail this contact point belongs to (optional)
    extended_contact_detail = models.ForeignKey('ExtendedContactDetail', null=True, blank=True, on_delete=models.CASCADE, related_name='telecom_points')
    # Patient this contact point belongs to (optional)
    patient = models.ForeignKey('patient.Patient', null=True, blank=True, on_delete=models.CASCADE, related_name='telecom_points')
    # RelatedPerson this contact point belongs to (optional)
    related_person = models.ForeignKey('patient.RelatedPerson', null=True, blank=True, on_delete=models.CASCADE, related_name='telecom_points')
    # Patient contact this contact point belongs to (optional)
    patient_contact = models.ForeignKey('patient.PatientContact', null=True, blank=True, on_delete=models.CASCADE, related_name='telecom_points')
    
    class Meta:
        db_table = 'contact_point'
    
    def clean(self):
        super().clean()
        # FHIR Rule: A system is required if a value is provided
        if self.value and not self.system:
            raise ValidationError("ContactPoint.system is required when value is provided")


class ContactDetail(Element):
    """Contact information"""
    # Name of an individual to contact (0..1 string)
    name = models.CharField(max_length=256, null=True, blank=True)
    # Contact details for individual or organization (0..* ContactPoint)
    # Note: ContactPoint has reverse FK to ContactDetail as 'telecom_points'
    # Organization this contact belongs to (optional)
    organization = models.ForeignKey('organization.Organization', null=True, blank=True, on_delete=models.CASCADE, related_name='contacts')
    # Endpoint this contact belongs to (optional)
    endpoint = models.ForeignKey('endpoint.Endpoint', null=True, blank=True, on_delete=models.CASCADE, related_name='contacts')
    # Practitioner role this contact belongs to (optional)
    practitioner_role = models.ForeignKey('practitioner.PractitionerRole', null=True, blank=True, on_delete=models.CASCADE, related_name='contacts')
    # Healthcare service this contact belongs to (optional)
    healthcare_service = models.ForeignKey('healthcareservice.HealthcareService', null=True, blank=True, on_delete=models.CASCADE, related_name='contacts')
    # Citation author (optional)
    citation_author = models.ForeignKey('citation.Citation', null=True, blank=True, on_delete=models.CASCADE, related_name='authors')
    # Citation editor (optional)
    citation_editor = models.ForeignKey('citation.Citation', null=True, blank=True, on_delete=models.CASCADE, related_name='editors')
    # Citation reviewer (optional)
    citation_reviewer = models.ForeignKey('citation.Citation', null=True, blank=True, on_delete=models.CASCADE, related_name='reviewers')
    # Citation endorser (optional)
    citation_endorser = models.ForeignKey('citation.Citation', null=True, blank=True, on_delete=models.CASCADE, related_name='endorsers')
    
    class Meta:
        db_table = 'contact_detail'


class ExtendedContactDetail(Element):
    """Extended Contact information"""
    # The type of contact (0..1 CodeableConcept)
    purpose = models.ForeignKey('CodeableConcept', null=True, blank=True, on_delete=models.SET_NULL, related_name='extended_contact_purposes')
    # Address for the contact (0..1 Address)
    address = models.ForeignKey('Address', null=True, blank=True, on_delete=models.SET_NULL, related_name='extended_contacts')
    # This contact detail is handled/monitored by a specific organization (0..1 Reference(Organization))
    organization = models.ForeignKey('organization.Organization', null=True, blank=True, on_delete=models.SET_NULL, related_name='extended_contacts')
    # Period that this contact was valid for usage (0..1 Period)
    period = models.ForeignKey('Period', null=True, blank=True, on_delete=models.SET_NULL, related_name='extended_contacts')
    # Organization this extended contact belongs to (optional)
    organization_contact = models.ForeignKey('organization.Organization', null=True, blank=True, on_delete=models.CASCADE, related_name='extended_contact_details')
    # Healthcare service this extended contact belongs to (optional)
    healthcare_service_contact = models.ForeignKey('healthcareservice.HealthcareService', null=True, blank=True, on_delete=models.CASCADE, related_name='extended_contact_details')
    
    class Meta:
        db_table = 'extended_contact_detail'


class HumanName(Element):
    """Name of a human or other living entity - parts and usage"""
    # usual | official | temp | nickname | anonymous | old | maiden (0..1 code)
    use = models.CharField(max_length=16, null=True, blank=True, choices=[
        ('usual', 'Usual'), ('official', 'Official'), ('temp', 'Temp'),
        ('nickname', 'Nickname'), ('anonymous', 'Anonymous'), ('old', 'Old'), ('maiden', 'Maiden')
    ])
    # Text representation of the full name (0..1 string)
    text = models.CharField(max_length=256, null=True, blank=True)
    # Family name (often called 'Surname') (0..1 string)
    family = models.CharField(max_length=128, null=True, blank=True)
    # Given names (0..* string)
    given = models.JSONField(null=True, blank=True)  # Array of given names
    # Parts that come before the name (0..* string)
    prefix = models.JSONField(null=True, blank=True)  # Array of prefixes
    # Parts that come after the name (0..* string)
    suffix = models.JSONField(null=True, blank=True)  # Array of suffixes
    # Time period when name was/is in use (0..1 Period)
    period = models.ForeignKey('Period', null=True, blank=True, on_delete=models.SET_NULL, related_name='human_names')
    # Practitioner this name belongs to (optional)
    practitioner = models.ForeignKey('practitioner.Practitioner', null=True, blank=True, on_delete=models.CASCADE, related_name='names')
    # Extended contact detail this name belongs to (optional)
    extended_contact_detail = models.ForeignKey('ExtendedContactDetail', null=True, blank=True, on_delete=models.CASCADE, related_name='names')
    # Patient this name belongs to (optional)
    patient = models.ForeignKey('patient.Patient', null=True, blank=True, on_delete=models.CASCADE, related_name='names')
    # RelatedPerson this name belongs to (optional)
    related_person = models.ForeignKey('patient.RelatedPerson', null=True, blank=True, on_delete=models.CASCADE, related_name='names')
    
    class Meta:
        db_table = 'human_name'


class AvailableTime(Element):
    """Times the item is available"""
    # Availability this belongs to
    availability = models.ForeignKey('Availability', on_delete=models.CASCADE, related_name='available_times', null=True, blank=True)
    # mon | tue | wed | thu | fri | sat | sun (0..* code)
    daysOfWeek = models.JSONField(null=True, blank=True)  # Array of day codes
    # Always available? i.e. 24 hour service (0..1 boolean)
    allDay = models.BooleanField(null=True, blank=True)
    # Opening time of day (ignored if allDay = true) (0..1 time)
    availableStartTime = models.TimeField(null=True, blank=True)
    # Closing time of day (ignored if allDay = true) (0..1 time)
    availableEndTime = models.TimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'available_time'
    
    def clean(self):
        super().clean()
        # FHIR Rule: Cannot include start/end times when selecting all day availability
        if self.allDay and (self.availableStartTime or self.availableEndTime):
            raise ValidationError("Cannot include start/end times when allDay is true")


class NotAvailableTime(Element):
    """Not available during this time due to provided reason"""
    # Availability this belongs to
    availability = models.ForeignKey('Availability', on_delete=models.CASCADE, related_name='not_available_times', null=True, blank=True)
    # Reason presented to the user explaining why time not available (0..1 string)
    description = models.CharField(max_length=512, null=True, blank=True)
    # Service not available during this period (0..1 Period)
    during = models.ForeignKey('Period', null=True, blank=True, on_delete=models.SET_NULL, related_name='not_available_times')
    
    class Meta:
        db_table = 'not_available_time'


class Availability(Element):
    """Availability data for an item"""
    # PractitionerRole this availability belongs to (optional)
    practitioner_role = models.ForeignKey('practitioner.PractitionerRole', null=True, blank=True, on_delete=models.CASCADE, related_name='availabilities')
    # HealthcareService this availability belongs to (optional)
    healthcare_service = models.ForeignKey('healthcareservice.HealthcareService', null=True, blank=True, on_delete=models.CASCADE, related_name='availabilities')
    # Note: availableTime and notAvailableTime are handled via reverse FK
    
    class Meta:
        db_table = 'availability'


class Address(Element):
    """An address expressed using postal conventions"""
    # home | work | temp | old | billing - purpose of this address (0..1 code)
    use = models.CharField(max_length=16, null=True, blank=True, choices=[
        ('home', 'Home'), ('work', 'Work'), ('temp', 'Temp'),
        ('old', 'Old'), ('billing', 'Billing')
    ])
    # postal | physical | both (0..1 code)
    type = models.CharField(max_length=16, null=True, blank=True, choices=[
        ('postal', 'Postal'), ('physical', 'Physical'), ('both', 'Both')
    ])
    # Text representation of the address (0..1 string)
    text = models.CharField(max_length=512, null=True, blank=True)
    # Street name, number, direction & P.O. Box etc. (0..* string)
    line = models.JSONField(null=True, blank=True)  # Array of address lines
    # Name of city, town etc. (0..1 string)
    city = models.CharField(max_length=128, null=True, blank=True)
    # District name (aka county) (0..1 string)
    district = models.CharField(max_length=128, null=True, blank=True)
    # Sub-unit of country (0..1 string)
    state = models.CharField(max_length=128, null=True, blank=True)
    # Postal code for area (0..1 string)
    postalCode = models.CharField(max_length=32, null=True, blank=True)
    # Country (0..1 string)
    country = models.CharField(max_length=128, null=True, blank=True)
    # Time period when address was/is in use (0..1 Period)
    period = models.ForeignKey('Period', null=True, blank=True, on_delete=models.SET_NULL, related_name='addresses')
    # Practitioner this address belongs to (optional)
    practitioner = models.ForeignKey('practitioner.Practitioner', null=True, blank=True, on_delete=models.CASCADE, related_name='addresses')
    # Patient this address belongs to (optional)
    patient = models.ForeignKey('patient.Patient', null=True, blank=True, on_delete=models.CASCADE, related_name='addresses')
    # RelatedPerson this address belongs to (optional)
    related_person = models.ForeignKey('patient.RelatedPerson', null=True, blank=True, on_delete=models.CASCADE, related_name='addresses')
    
    class Meta:
        db_table = 'address'

# class Reference(models.Model): # Element # A reference from one resource to another # Rules: + Rule: SHALL have a contained resource if a local reference is provided + Rule: At least one of reference, identifier and display SHALL be present (unless an extension is provided).
#     reference # Primitive type # string # 	Literal reference, Relative, internal or absolute URL
#     type # Primitive type # uri # Type the reference refers to (e.g. "Patient")  - must be a resource in resources Binding: Resource Types (Extensible)
#     identifier # Data type # Identifier # Logical reference, when literal reference is not known
#     display # Primitive type # string # Text alternative for the resource


# -------------------------------------------MetaElement----------------------------------------- #
# Metadata about a resource
class MetaElement(Element):
    # Version-specific identifier (0..1)
    versionId = models.CharField(max_length=64, null=True, blank=True)
    # When the resource version Last Changed (0..1)
    lastUpdated = models.DateTimeField(null=True, blank=True)
    # Identifies where the resource comes from (0..1)
    source = models.URLField(max_length=512, null=True, blank=True)
    # Profiles this resource claims to conform to (0..*)
    profile = models.JSONField(null=True, blank=True) # list of canonical URLs
    # Security Labels applied to this resource Binding: All Security Labels (Extensible)
    security = GenericRelation('components.Coding', related_query_name='meta_security', blank=True)

    # Tags applied to this resource (0..*)
    tag = GenericRelation('components.Coding', related_query_name='meta_tag', blank=True)

    class Meta:
        db_table = 'meta'
        indexes = [
            models.Index(fields=['versionId']),
            models.Index(fields=['source']),
        ]

    def __str__(self):
        return f"Meta(id={self.id}, versionId={self.versionId})"
    
# -------------------------------------------MetaElement----------------------------------------- #

##################################### Non breakable models ##################################

# -------------------------------------------Coding----------------------------------------- #

class Coding(Element):
    # Identity of the terminology system 
    system = models.URLField(max_length=512, null=True, blank=True)
    # Version of the terminology system (0..1)
    version = models.CharField(max_length=64, null=True, blank=True)
    # Symbol/code defined by the system (0..1) – required if display is present
    code = models.CharField(max_length=64, null=True, blank=True)
    # Human-readable representation defined by the system (0..1) – should only exist if code exists
    display = models.CharField(max_length=64, null=True, blank=True)
    # Flag if user selected this coding directly (0..1)
    userSelected = models.BooleanField(null=True, blank=True)
    # CodeableConcept this coding belongs to (optional)
    codeable_concept = models.ForeignKey('CodeableConcept', null=True, blank=True, on_delete=models.CASCADE, related_name='codings')

    class Meta:
        db_table = 'coding'
        indexes = [
            models.Index(fields=['system']),
            models.Index(fields=['code']),
        ]



# -------------------------------------------PERIOD----------------------------------------- #
                                     
# Suppose you want to capture why a Period ended, which is not part of core FHIR.
# from datetime import datetime
# from myapp.models import Period

# # Create a Period with extensions
# p = Period.objects.create(
#     start=datetime.fromisoformat("2020-01-01T00:00:00"),
#     end=datetime.fromisoformat("2021-01-01T00:00:00"),
#     extension=[
#         {"url": "http://example.org/fhir/StructureDefinition/period-reasonEnded",
#          "value_string": "Patient moved abroad"},
#         {"url": "http://example.org/fhir/StructureDefinition/another-extension",
#          "value_boolean": True}
#     ]
# )

# Access extensions
# print(p.extension)  # will show the list of extension dicts

class Period(Element): # Element # Time range defined by start and end date/time + Rule: If present, start SHALL have a lower or equal value than end - Elements defined in Ancestors: id, extension
    start = models.DateTimeField(null=True, blank=True) # Primitive type # dateTime # Starting time with inclusive boundary
    end = models.DateTimeField(null=True, blank=True) # Primitive type # dateTime # End time with inclusive boundary, if not ongoing

    class Meta:
        db_table = 'period'
        indexes = [
            models.Index(fields=['start']),
            models.Index(fields=['end']),
        ]

    def clean(self):
        # FHIR invariant: start must be <= end
        if self.start and self.end and self.start > self.end:
            raise ValidationError("Period.start must be earlier than or equal to Period.end")
    def __str__(self):
        if self.start and self.end:
            return f"{self.start.isoformat()} → {self.end.isoformat()}"
        elif self.start:
            return f"{self.start.isoformat()} → ongoing"
        elif self.end:
            return f"until {self.end.isoformat()}"
        return "No period defined"
    
# -------------------------------------------PERIOD----------------------------------------- #

# -----------------------------------------NARRATIVE---------------------------------------- #

class Narrative(Element):
    STATUS_CHOICES = [
        ('generated', 'Generated'),
        ('extensions', 'Extensions'),
        ('additional', 'Additional'),
        ('empty', 'Empty'),
    ]

    ALLOWED_TAGS = [
        'b', 'i', 'em', 'strong', 'u', 'p', 'br', 'ul', 'ol', 'li',
        'a', 'img', 'span', 'div', 'table', 'tr', 'td', 'th', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'
    ]

    ALLOWED_ATTRIBUTES = {
        'a': ['href', 'name', 'title'],
        'img': ['src', 'alt', 'title', 'style'],
        'span': ['style'],
        'div': ['style'],
        'p': ['style'],
        'table': ['style'],
        'td': ['style'],
        'th': ['style'],
        # other tags may have 'style' if needed
    }

    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default='generated')
    div = models.TextField() # Will hold XHTML content

    class Meta:
        db_table = 'narrative'
    
    def clean(self):
        super().clean()
        # FHIR invariant: div must have some non-whitespace content
        # Rule 1: Non-whitespace content
        if not self.div or not self.div.strip():
            raise ValidationError("Narrative.div must have some non-whitespace content")
        
        # Rule 2: Limited XHTML content
        cleaned = bleach.clean(
            self.div, 
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRIBUTES,
            strip=True
        )

        # If bleach removed the content entirely, raise an error
        if not cleaned.strip():
            raise ValidationError("Narrative.div must have valid XHTML content")
    
    def __str__(self):
        return f"Narrative(status={self.status})"
    
# -------------------------------------- Range ------------------------------------------#

class Range(Element):
    low = models.ForeignKey(
        'components.SimpleQuantity',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='range_low'
    )
    high = models.ForeignKey(
        'components.SimpleQuantity',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='range_high'
    )

    class Meta:
        db_table = 'range'

    def clean(self):
        super().clean()  # calls Element.clean()
        if self.low and self.high and self.low.value > self.high.value:
            raise ValidationError("Range.low must be less than or equal to Range.high")

    def __str__(self):
        low_val = self.low.value if self.low else 'None'
        high_val = self.high.value if self.high else 'None'
        return f"{low_val} - {high_val}"
    
# --------------------------------------- Range ----------------------------------------- #
    
# -------------------------------------- Quantity --------------------------------------- #
class Quantity(Element):
    value = models.DecimalField(
        max_digits=18, decimal_places=6, null=True, blank=True
    )
    comparator = models.CharField(
        max_length=2, null=True, blank=True,
        choices=[
            ('<', '<'),
            ('<=', '<='),
            ('>=', '>='),
            ('>', '>'),
            ('ad', 'ad')  # ad = approximately equal / "about"
        ]
    )
    unit = models.CharField(max_length=64, null=True, blank=True)
    system = models.URLField(max_length=512, null=True, blank=True)
    code = models.CharField(max_length=64, null=True, blank=True)

    class Meta:
        db_table = 'quantity'
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['system']),
        ]

    def clean(self):
        # FHIR invariant: if code is set, system must also be set
        if self.code and not self.system:
            raise ValidationError("Quantity.system must be set if Quantity.code is present")

    def __str__(self):
        if self.value is not None:
            cmp_str = f"{self.comparator} " if self.comparator else ""
            unit_str = f" {self.unit}" if self.unit else ""
            return f"{cmp_str}{self.value}{unit_str}"
        return f"Quantity(id={self.fhir_id})"
    

# -------------------------------------- Quantity --------------------------------------- #


# -------------------------------------- Simple Quantity --------------------------------------- #


class SimpleQuantity(Quantity):
    class Meta:
        db_table = 'simple_quantity'

    def clean(self):
        super().clean()
        if self.comparator is not None:
            raise ValidationError("SimpleQuantity.comparator must be empty")

# -------------------------------------- Simple Quantity --------------------------------------- #



# -----------------------------------------EXTENSION---------------------------------------- #

class Extension(AbstractExtension):
    class Meta:
        db_table = 'extension'
        indexes = [
            models.Index(fields=['url']),
            models.Index(fields=['content_type', 'object_id']),
        ]

# -----------------------------------------EXTENSION---------------------------------------- #

##################################### Non breakabale models ##################################

# -----------------------------------------USAGE CONTEXT---------------------------------------- #

class UsageContext(Element):
    # Type of context being specified (1..1 Coding)
    code = models.ForeignKey(
        'components.Coding',
        on_delete=models.CASCADE,
        related_name='usage_contexts'
    )
    
    # Value that defines the context - choice type value[x] (1..1)
    valueCodeableConcept = models.ForeignKey(
        'components.CodeableConcept',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='usage_context_values'
    )
    valueQuantity = models.ForeignKey(
        'components.Quantity',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='usage_context_values'
    )
    valueRange = models.ForeignKey(
        'components.Range',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='usage_context_values'
    )
    valueReference = GenericForeignKey('value_reference_type', 'value_reference_id')
    value_reference_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    value_reference_id = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        db_table = 'usage_context'
        indexes = [
            models.Index(fields=['value_reference_type', 'value_reference_id']),
        ]

    def clean(self):
        super().clean()
        # FHIR invariant: exactly one value[x] must be set
        value_fields = [
            self.valueCodeableConcept,
            self.valueQuantity, 
            self.valueRange,
            self.valueReference
        ]
        set_values = [v for v in value_fields if v is not None]
        if len(set_values) != 1:
            raise ValidationError("UsageContext must have exactly one value[x] field set")

    def __str__(self):
        value = None
        if self.valueCodeableConcept:
            value = self.valueCodeableConcept
        elif self.valueQuantity:
            value = self.valueQuantity
        elif self.valueRange:
            value = self.valueRange
        elif self.valueReference:
            value = self.valueReference
        return f"UsageContext(code={self.code}, value={value})"

# -----------------------------------------USAGE CONTEXT---------------------------------------- #


class Attachment(DataType):
    """Content in a format defined elsewhere"""
    # Mime type of the content (0..1 code)
    contentType = models.CharField(max_length=100, null=True, blank=True)
    # Human language of the content (0..1 code)
    language = models.CharField(max_length=10, null=True, blank=True)
    # Data inline, base64ed (0..1 base64Binary)
    data = models.TextField(null=True, blank=True)
    # Uri where the data can be found (0..1 url)
    url = models.URLField(null=True, blank=True)
    # Number of bytes of content (0..1 integer64)
    size = models.BigIntegerField(null=True, blank=True)
    # Hash of the data (0..1 base64Binary)
    hash = models.CharField(max_length=255, null=True, blank=True)
    # Label to display in place of the data (0..1 string)
    title = models.CharField(max_length=255, null=True, blank=True)
    # Date attachment was first created (0..1 dateTime)
    creation = models.DateTimeField(null=True, blank=True)
    # Height of the image in pixels (0..1 positiveInt)
    height = models.PositiveIntegerField(null=True, blank=True)
    # Width of the image in pixels (0..1 positiveInt)
    width = models.PositiveIntegerField(null=True, blank=True)
    # Number of frames if > 1 (0..1 positiveInt)
    frames = models.PositiveIntegerField(null=True, blank=True)
    # Length in seconds (0..1 decimal)
    duration = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    # Number of printed pages (0..1 positiveInt)
    pages = models.PositiveIntegerField(null=True, blank=True)
    
    class Meta:
        db_table = 'attachment'
    
    # Patient this attachment belongs to (optional)
    patient = models.ForeignKey('patient.Patient', null=True, blank=True, on_delete=models.CASCADE, related_name='photos')
    # RelatedPerson this attachment belongs to (optional)
    related_person = models.ForeignKey('patient.RelatedPerson', null=True, blank=True, on_delete=models.CASCADE, related_name='photos')
    
    def clean(self):
        super().clean()
        # Rule: If the Attachment has data, it SHALL have a contentType
        if self.data and not self.contentType:
            raise ValidationError("If the Attachment has data, it SHALL have a contentType")

# -----------------------------------------ATTACHMENT---------------------------------------- #


class VirtualServiceDetail(Element):
    """Virtual Service Contact Details"""
    # Channel Type (0..1 Coding)
    channelType = models.ForeignKey('Coding', null=True, blank=True, on_delete=models.SET_NULL, related_name='virtual_service_channels')
    # Contact address/number - choice type address[x] (0..1)
    addressUrl = models.URLField(null=True, blank=True)
    addressString = models.CharField(max_length=255, null=True, blank=True)
    addressContactPoint = models.ForeignKey('ContactPoint', null=True, blank=True, on_delete=models.SET_NULL, related_name='virtual_service_addresses')
    addressExtendedContactDetail = models.ForeignKey('ExtendedContactDetail', null=True, blank=True, on_delete=models.SET_NULL, related_name='virtual_service_addresses')
    # Address to see alternative connection details (0..* url)
    additionalInfo = models.JSONField(null=True, blank=True)  # Array of URLs
    # Maximum number of participants (0..1 positiveInt)
    maxParticipants = models.PositiveIntegerField(null=True, blank=True)
    # Session Key required by the virtual service (0..1 string)
    sessionKey = models.CharField(max_length=255, null=True, blank=True)
    # Location this virtual service belongs to (optional)
    location = models.ForeignKey('location.Location', null=True, blank=True, on_delete=models.CASCADE, related_name='virtual_services')
    
    class Meta:
        db_table = 'virtual_service_detail'
    
    def clean(self):
        super().clean()
        # FHIR choice type: exactly one address[x] field can be set
        address_fields = [self.addressUrl, self.addressString, self.addressContactPoint, self.addressExtendedContactDetail]
        set_addresses = [a for a in address_fields if a is not None]
        if len(set_addresses) > 1:
            raise ValidationError("VirtualServiceDetail must have exactly one address[x] field set, not multiple")

# -----------------------------------------VIRTUAL SERVICE DETAIL---------------------------------------- #


class Reference(Element):
    """A reference from one resource to another"""
    # Literal reference, Relative, internal or absolute URL (0..1 string)
    reference = models.CharField(max_length=512, null=True, blank=True)
    # Type the reference refers to (0..1 uri)
    type = models.CharField(max_length=64, null=True, blank=True)
    # Logical reference, when literal reference is not known (0..1 Identifier)
    identifier = models.ForeignKey('Identifier', null=True, blank=True, on_delete=models.SET_NULL, related_name='references')
    # Text alternative for the resource (0..1 string)
    display = models.CharField(max_length=256, null=True, blank=True)
    
    class Meta:
        db_table = 'reference'
        indexes = [
            models.Index(fields=['reference']),
            models.Index(fields=['type']),
        ]
    
    def clean(self):
        super().clean()
        # FHIR Rule: At least one of reference, identifier and display SHALL be present
        if not (self.reference or self.identifier or self.display):
            raise ValidationError("Reference must have at least one of reference, identifier, or display")
    
    def __str__(self):
        if self.reference:
            return f"Reference({self.reference})"
        elif self.identifier:
            return f"Reference(identifier={self.identifier})"
        elif self.display:
            return f"Reference(display={self.display})"
        return "Reference(empty)"

# -----------------------------------------REFERENCE---------------------------------------- #