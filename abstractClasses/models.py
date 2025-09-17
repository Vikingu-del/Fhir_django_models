from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.core.exceptions import ValidationError

######################################### Abstract Models ####################################

class AbstractExtension(models.Model):
    # url where the extension can be found
    url = models.URLField(max_length=512)

    value_string = models.CharField(max_length=2048, null=True, blank=True)
    value_boolean = models.BooleanField(null=True, blank=True)
    value_integer = models.IntegerField(null=True, blank=True)
    value_decimal = models.DecimalField(max_digits=18, decimal_places=6, null=True, blank=True)
    value_datetime = models.DateTimeField(null=True, blank=True)
    # fhir types
    value_period = models.ForeignKey("Period", null=True, blank=True, on_delete=models.SET_NULL)
    # More types to add as we expend

    # Generic relation fields 
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        abstract = True

    def clean(self):
        # Ensure only one value is set at a time (FHIR invariant)
        value_fields = [
            'value_string', 'value_boolean', 'value_integer',
            'value_decimal', 'value_datetime', 'value_period'
        ]
        set_values = [f for f in value_fields if getattr(self, f) is not None]
        if len(set_values) > 1:
            raise ValidationError("Only one value[x] can be set per Extension.")
        
    def __str__(self):
        value_fields = [
            'value_string', 'value_boolean', 'value_integer',
            'value_decimal', 'value_datetime', 'value_period'
        ]
        for f in value_fields:
            val = getattr(self, f)
            if val is not None:
                return f"{self.url} = {val}"
        return f"{self.url} (no value)"




class Base(models.Model):
    class Meta:
        abstract = True


class Element(Base):
    fhir_id = models.CharField(max_length=64, null=True, blank=True) # Fhir Element.id
    # Extension is optional and it can be multiple
    extension = GenericRelation('components.Extension', blank=True)

    class Meta:
        abstract = True

    def clean(self):
        has_children = hasattr(self, 'children') and self.children
        has_extension = self.extension.exists() if self.pk else False
        if (has_children or has_extension) and not self.fhir_id:
            raise ValidationError("Element.fhir_id is required when element has children or extensions")


class DataType(Element):
    """
    Abstract FHIR DataType.
    All reusable primitive and complex datatypes inherit from this.
    Example children: Period, Coding, HumanName, Quantity, etc.
    """
    class Meta:
        abstract = True


class PrimitiveType(DataType):
    """
    Abstract FHIR PrimitiveType.
    Base for all primitive data types.
    """
    class Meta:
        abstract = True


class BackboneType(DataType):
    # Modifier extensions – cannot be ignored if present
    modifierExtension = GenericRelation(
        'components.Extension',
        related_query_name='backbone_type',
        blank=True
    )

    class Meta:
        abstract = True

    def clean(self):
        super().clean()

        # In FHIR, modifierExtension must be distinguished from extension
        if self.modifierExtension.exists() and not self.fhir_id:
            # FHIR recommends elements with extensions have an id
            raise ValidationError("BackboneType.fhir_id is required when modifierExtension is present")


class BackboneElement(Element):  #element # Base for elements defined inside a resource
    # Optional id (FHIR allows for element IDs)
    modifierExtension = models.JSONField(null=True, blank=True) # Extensions that cannot be ignored even if unrecognized

    class Meta:
        abstract = True

class Resource(Base):
    # Logical id of this artifact
    fhir_id = models.CharField(
        max_length=64, null=True, blank=True, help_text="Logical id of this artifact"
    )
    # Metadata about the resource
    meta = models.OneToOneField(
        'components.MetaElement', on_delete=models.SET_NULL, null=True, blank=True, related_name="%(class)s_resource"
    )
    # A set of rules under which this content was created
    implicitRules = models.URLField(
        max_length=1024, null=True, blank=True, help_text="Rules under which this content was created"
    )
    # Language of the resource content Binding: All Languages (Required) 
    # Additional Bindings	Purpose
    # Common Languages	Starter Set
    language = models.CharField(
        max_length=16, null=True, blank=True, help_text="Language of the resource content"
    )

    class Meta:
        abstract = True

    def clean(self):
        super().clean()
        # FHIR invariant: if resource has implicit rules, fhir_id is recommended
        if self.implicitRules and not self.fhir_id:
            raise ValidationError("Resource.fhir_id is required when resource has implicit rules")
        
    def __str__(self):
        return f"{self.__class__.__name__}(fhir_id={self.fhir_id})"
    

class DomainResource(Resource):
    # Text summary of the resource, for human interpretation
    text = models.OneToOneField(
        'components.Narrative',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='%(class)s_resource'
    )
    # Contained, inline Resources (0..* Resource)
    contained = GenericRelation('self', related_query_name='container_resource', blank=True)
    # Extensions (0..* Extension)
    extension = GenericRelation('components.Extension', related_query_name='domain_resource', blank=True)
    # Modifier Extensions that cannot be ignored (0..* Extension)
    modifierExtension = GenericRelation('components.Extension', related_query_name='modifier_domain_resource', blank=True)
    
    # Track containment relationship
    container_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    container_id = models.PositiveIntegerField(null=True, blank=True)
    container = GenericForeignKey('container_type', 'container_id')
    
    class Meta:
        abstract = True

    def clean(self):
        super().clean()
        
        # FHIR containment rules
        if self.container:
            # Rule 1: Contained resources SHALL NOT contain other resources
            if self.contained.exists():
                raise ValidationError("Contained resources cannot themselves contain other resources")
            
            # Rule 2: Contained resources SHALL NOT have meta.versionId or meta.lastUpdated
            if self.meta and (self.meta.versionId or self.meta.lastUpdated):
                raise ValidationError("Contained resources cannot have meta.versionId or meta.lastUpdated")
            
            # Rule 3: Contained resources SHALL NOT have security labels
            if self.meta and self.meta.security.exists():
                raise ValidationError("Contained resources cannot have security labels")
            

class CanonicalResource(DomainResource):
    # Canonical identifier (0..1 uri)
    url = models.URLField(max_length=1024, null=True, blank=True)
    # Additional identifiers (0..* Identifier)
    identifier = models.ManyToManyField('components.Identifier', blank=True, related_name='canonical_resources')
    
    # Business version (0..1 string)
    version = models.CharField(max_length=64, null=True, blank=True)
    
    # versionAlgorithm[x] choice type (0..1)
    versionAlgorithmString = models.CharField(max_length=128, null=True, blank=True)
    versionAlgorithmCoding = models.ForeignKey('components.Coding', null=True, blank=True, on_delete=models.SET_NULL, related_name='version_algorithm')

    # Computer friendly name (0..1 string)
    name = models.CharField(max_length=128, null=True, blank=True)
    # Human friendly title (0..1 string)
    title = models.CharField(max_length=256, null=True, blank=True)
    # Publication status (1..1 code) - required
    status = models.CharField(max_length=32, choices=[('draft','Draft'),('active','Active'),('retired','Retired'),('unknown','Unknown')])
    # For testing purposes (0..1 boolean)
    experimental = models.BooleanField(null=True, blank=True)
    # Date last changed (0..1 dateTime)
    date = models.DateTimeField(null=True, blank=True)
    # Publisher name (0..1 string)
    publisher = models.CharField(max_length=256, null=True, blank=True)
    
    # Contact details (0..* ContactDetail)
    contact = models.ManyToManyField('components.ContactDetail', blank=True, related_name='canonical_resources')
    
    # Natural language description (0..1 markdown)
    description = models.TextField(null=True, blank=True)
    # Usage context (0..* UsageContext)
    useContext = models.ManyToManyField('components.UsageContext', blank=True, related_name='canonical_resources')
    # Intended jurisdiction (0..* CodeableConcept)
    jurisdiction = models.ManyToManyField('components.CodeableConcept', blank=True, related_name='canonical_resources')
    
    # Why this is defined (0..1 markdown)
    purpose = models.TextField(null=True, blank=True)
    # Use and publishing restrictions (0..1 markdown)
    copyright = models.TextField(null=True, blank=True)
    # Copyright holder and year(s) (0..1 string)
    copyrightLabel = models.CharField(max_length=128, null=True, blank=True)
    
    class Meta:
        abstract = True

    def clean(self):
        super().clean()
        # FHIR invariant: only one versionAlgorithm[x] can be set
        if self.versionAlgorithmString and self.versionAlgorithmCoding:
            raise ValidationError("Only one versionAlgorithm[x] field can be set")
        
        # URL validation - should not contain | or #
        if self.url and ('|' in self.url or '#' in self.url):
            raise ValidationError("URL should not contain | or # characters")

    def __str__(self):
        return f"{self.__class__.__name__}(url={self.url}, version={self.version})"


class MetadataResource(CanonicalResource):
    """Common Interface declaration for definitional resources"""
    
    # When the resource was approved by publisher (0..1 date)
    approvalDate = models.DateField(null=True, blank=True)
    # When the resource was last reviewed by the publisher (0..1 date)
    lastReviewDate = models.DateField(null=True, blank=True)
    # When the resource is expected to be used (0..1 Period)
    effectivePeriod = models.ForeignKey('components.Period', null=True, blank=True, on_delete=models.SET_NULL, related_name='metadata_resources')
    
    # E.g. Education, Treatment, Assessment, etc (0..* CodeableConcept)
    topic = models.ManyToManyField('components.CodeableConcept', blank=True, related_name='metadata_resources_topic')
    
    # Who authored the resource (0..* ContactDetail)
    author = models.ManyToManyField('components.ContactDetail', blank=True, related_name='authored_metadata_resources')
    # Who edited the resource (0..* ContactDetail)
    editor = models.ManyToManyField('components.ContactDetail', blank=True, related_name='edited_metadata_resources')
    # Who reviewed the resource (0..* ContactDetail)
    reviewer = models.ManyToManyField('components.ContactDetail', blank=True, related_name='reviewed_metadata_resources')
    # Who endorsed the resource (0..* ContactDetail)
    endorser = models.ManyToManyField('components.ContactDetail', blank=True, related_name='endorsed_metadata_resources')
    
    # Additional documentation, citations, etc (0..* RelatedArtifact)
    # TODO: Uncomment when RelatedArtifact model is created
    # relatedArtifact = models.ManyToManyField('components.RelatedArtifact', blank=True, related_name='metadata_resources')
    
    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.__class__.__name__}(url={self.url}, title={self.title})"
            

#########################################
# Primitive FHIR types
#########################################

class FHIRBoolean(PrimitiveType):
    value = models.BooleanField(null=True, blank=True)

    class Meta:
        abstract = True

class FHIRInteger(PrimitiveType):
    value = models.IntegerField(null=True, blank=True)

    class Meta:
        abstract = True

class FHIRDecimal(PrimitiveType):
    value = models.DecimalField(max_digits=18, decimal_places=6, null=True, blank=True)

    class Meta:
        abstract = True

class FHIRString(PrimitiveType):
    value = models.CharField(max_length=2048, null=True, blank=True)

    class Meta:
        abstract = True

class FHIRUri(PrimitiveType):
    value = models.URLField(max_length=1024, null=True, blank=True)

    class Meta:
        abstract = True

class FHIRCode(PrimitiveType):
    value = models.CharField(max_length=256, null=True, blank=True)

    class Meta:
        abstract = True

class FHIRDateTime(PrimitiveType):
    value = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

class FHIRInstant(PrimitiveType):
    value = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

class FHIRId(PrimitiveType):
    value = models.CharField(max_length=64, null=True, blank=True)

    class Meta:
        abstract = True

class FHIRMarkdown(PrimitiveType):
    value = models.TextField(null=True, blank=True)

    class Meta:
        abstract = True

class FHIROid(PrimitiveType):
    value = models.CharField(max_length=64, null=True, blank=True)

    class Meta:
        abstract = True

class FHIRUnsignedInt(PrimitiveType):
    value = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        abstract = True

class FHIRPositiveInt(PrimitiveType):
    value = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        abstract = True

class FHIRTime(PrimitiveType):
    value = models.TimeField(null=True, blank=True)

    class Meta:
        abstract = True

class FHIRCanonical(PrimitiveType):
    # Canonical URI (reference to StructureDefinition or other canonical resources)
    value = models.URLField(max_length=1024, null=True, blank=True)

    class Meta:
        abstract = True

class FHIRUrl(PrimitiveType):
    value = models.URLField(max_length=1024, null=True, blank=True)

    class Meta:
        abstract = True