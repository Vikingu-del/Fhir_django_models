from django.db import models
from django.core.exceptions import ValidationError
from abstractClasses.models import MetadataResource, BackboneElement
from components.reference import CanonicalField


class CitationSummary(BackboneElement):
    """A human-readable display of key concepts to represent the citation"""
    # Citation this summary belongs to
    citation = models.ForeignKey('Citation', on_delete=models.CASCADE, related_name='summaries', null=True, blank=True)
    # Format for display of the citation summary (0..1 CodeableConcept)
    style = models.ForeignKey('components.CodeableConcept', null=True, blank=True, on_delete=models.SET_NULL, related_name='citation_summary_styles')
    # The human-readable display of the citation summary (1..1 markdown)
    text = models.TextField()
    
    class Meta:
        db_table = 'citation_summary'


class CitationClassification(BackboneElement):
    """The assignment to an organizing scheme"""
    # Citation this classification belongs to
    citation = models.ForeignKey('Citation', on_delete=models.CASCADE, related_name='classifications', null=True, blank=True)
    # The kind of classifier (0..1 CodeableConcept)
    type = models.ForeignKey('components.CodeableConcept', null=True, blank=True, on_delete=models.SET_NULL, related_name='citation_classification_types')
    
    class Meta:
        db_table = 'citation_classification'


class CitationStatusDate(BackboneElement):
    """An effective date or period for a status of the citation record"""
    # Citation this status date belongs to
    citation = models.ForeignKey('Citation', on_delete=models.CASCADE, related_name='status_dates', null=True, blank=True)
    # Classification of the status (1..1 CodeableConcept)
    activity = models.ForeignKey('components.CodeableConcept', on_delete=models.CASCADE, related_name='citation_status_activities')
    # Either occurred or expected (0..1 boolean)
    actual = models.BooleanField(null=True, blank=True)
    # When the status started and/or ended (1..1 Period)
    period = models.ForeignKey('components.Period', on_delete=models.CASCADE, related_name='citation_status_dates')
    
    class Meta:
        db_table = 'citation_status_date'


class CitedArtifactVersion(BackboneElement):
    """The defined version of the cited artifact"""
    # Cited artifact this version belongs to
    cited_artifact = models.OneToOneField('CitedArtifact', on_delete=models.CASCADE, related_name='version', null=True, blank=True)
    # The version number or other version identifier (1..1 string)
    value = models.CharField(max_length=255)
    # Citation for the main version of the cited artifact (0..1 Reference(Citation))
    baseCitation = models.ForeignKey('Citation', null=True, blank=True, on_delete=models.SET_NULL, related_name='version_citations')
    
    class Meta:
        db_table = 'cited_artifact_version'


class CitedArtifactStatusDate(BackboneElement):
    """An effective date or period for a status of the cited artifact"""
    # Cited artifact this status date belongs to
    cited_artifact = models.ForeignKey('CitedArtifact', on_delete=models.CASCADE, related_name='status_dates', null=True, blank=True)
    # Classification of the status (1..1 CodeableConcept)
    activity = models.ForeignKey('components.CodeableConcept', on_delete=models.CASCADE, related_name='cited_artifact_status_activities')
    # Either occurred or expected (0..1 boolean)
    actual = models.BooleanField(null=True, blank=True)
    # When the status started and/or ended (1..1 Period)
    period = models.ForeignKey('components.Period', on_delete=models.CASCADE, related_name='cited_artifact_status_dates')
    
    class Meta:
        db_table = 'cited_artifact_status_date'


class CitedArtifactTitle(BackboneElement):
    """The title details of the article or artifact"""
    # Cited artifact this title belongs to
    cited_artifact = models.ForeignKey('CitedArtifact', on_delete=models.CASCADE, related_name='titles', null=True, blank=True)
    # Used to express the specific language (0..1 CodeableConcept)
    language = models.ForeignKey('components.CodeableConcept', null=True, blank=True, on_delete=models.SET_NULL, related_name='cited_artifact_title_languages')
    # The title of the article or artifact (1..1 markdown)
    text = models.TextField()
    
    class Meta:
        db_table = 'cited_artifact_title'


class CitedArtifactAbstract(BackboneElement):
    """Summary of the article or artifact"""
    # Cited artifact this abstract belongs to
    cited_artifact = models.ForeignKey('CitedArtifact', on_delete=models.CASCADE, related_name='abstracts', null=True, blank=True)
    # The kind of abstract (0..1 CodeableConcept)
    type = models.ForeignKey('components.CodeableConcept', null=True, blank=True, on_delete=models.SET_NULL, related_name='cited_artifact_abstract_types')
    # Used to express the specific language (0..1 CodeableConcept)
    language = models.ForeignKey('components.CodeableConcept', null=True, blank=True, on_delete=models.SET_NULL, related_name='cited_artifact_abstract_languages')
    # Abstract content (1..1 markdown)
    text = models.TextField()
    # Copyright notice for the abstract (0..1 markdown)
    copyright = models.TextField(null=True, blank=True)
    
    class Meta:
        db_table = 'cited_artifact_abstract'


class CitedArtifactPart(BackboneElement):
    """The component of the article or artifact"""
    # Cited artifact this part belongs to
    cited_artifact = models.OneToOneField('CitedArtifact', on_delete=models.CASCADE, related_name='part', null=True, blank=True)
    # The kind of component (0..1 CodeableConcept)
    type = models.ForeignKey('components.CodeableConcept', null=True, blank=True, on_delete=models.SET_NULL, related_name='cited_artifact_part_types')
    # The specification of the component (0..1 string)
    value = models.CharField(max_length=255, null=True, blank=True)
    # The citation for the full article or artifact (0..1 Reference(Citation))
    baseCitation = models.ForeignKey('Citation', null=True, blank=True, on_delete=models.SET_NULL, related_name='part_citations')
    
    class Meta:
        db_table = 'cited_artifact_part'


class CitedArtifactRelatesTo(BackboneElement):
    """The artifact related to the cited artifact"""
    # Cited artifact this relates to belongs to
    cited_artifact = models.ForeignKey('CitedArtifact', on_delete=models.CASCADE, related_name='relates_to', null=True, blank=True)
    # Type of relationship (1..1 code)
    type = models.CharField(max_length=50, choices=[
        ('documentation', 'Documentation'), ('citation', 'Citation'), ('predecessor', 'Predecessor'),
        ('successor', 'Successor'), ('derived-from', 'Derived From'), ('depends-on', 'Depends On'),
        ('composed-of', 'Composed Of'), ('part-of', 'Part Of'), ('cites', 'Cites'), ('cited-by', 'Cited By')
    ])
    # Short label (0..1 string)
    label = models.CharField(max_length=255, null=True, blank=True)
    # Brief description of the related artifact (0..1 string)
    display = models.CharField(max_length=255, null=True, blank=True)
    # Bibliographic citation for the artifact (0..1 markdown)
    citation = models.TextField(null=True, blank=True)
    # What document is being referenced (0..1 Attachment)
    document = models.ForeignKey('components.Attachment', null=True, blank=True, on_delete=models.SET_NULL, related_name='cited_artifact_relates_to')
    # What artifact is being referenced (0..1 canonical)
    resource = CanonicalField(null=True, blank=True)
    # What artifact, if not a conformance resource (0..1 Reference)
    resourceReference = models.ForeignKey('components.Reference', null=True, blank=True, on_delete=models.SET_NULL, related_name='cited_artifact_relates_to')
    
    class Meta:
        db_table = 'cited_artifact_relates_to'


class CitedArtifactPublicationFormPublishedIn(BackboneElement):
    """The collection the cited article or artifact is published in"""
    # Publication form this published in belongs to
    publication_form = models.OneToOneField('CitedArtifactPublicationForm', on_delete=models.CASCADE, related_name='published_in', null=True, blank=True)
    # Kind of container (0..1 CodeableConcept)
    type = models.ForeignKey('components.CodeableConcept', null=True, blank=True, on_delete=models.SET_NULL, related_name='published_in_types')
    # Name of the database or title of the book or journal (0..1 string)
    title = models.CharField(max_length=255, null=True, blank=True)
    # Name of or resource describing the publisher (0..1 Reference(Organization))
    publisher = models.ForeignKey('components.Reference', null=True, blank=True, on_delete=models.SET_NULL, related_name='published_in_publishers')
    # Geographic location of the publisher (0..1 string)
    publisherLocation = models.CharField(max_length=255, null=True, blank=True)
    
    class Meta:
        db_table = 'cited_artifact_publication_form_published_in'


class CitedArtifactPublicationFormPublishedInIdentifier(models.Model):
    """Journal identifiers include ISSN, ISO Abbreviation and NLMuniqueID; Book identifiers include ISBN"""
    # Published in this identifier belongs to
    published_in = models.ForeignKey('CitedArtifactPublicationFormPublishedIn', on_delete=models.CASCADE, related_name='identifiers')
    # The identifier (1..1 Identifier)
    identifier = models.ForeignKey('components.Identifier', on_delete=models.CASCADE, related_name='published_in_identifiers')
    
    class Meta:
        db_table = 'cited_artifact_publication_form_published_in_identifier'


class CitedArtifactPublicationForm(BackboneElement):
    """Alternative forms of the article that are not separate citations"""
    # Cited artifact this publication form belongs to
    cited_artifact = models.ForeignKey('CitedArtifact', on_delete=models.CASCADE, related_name='publication_forms', null=True, blank=True)
    # Internet or Print (0..1 CodeableConcept)
    citedMedium = models.ForeignKey('components.CodeableConcept', null=True, blank=True, on_delete=models.SET_NULL, related_name='cited_artifact_mediums')
    # Volume number (0..1 string)
    volume = models.CharField(max_length=50, null=True, blank=True)
    # Issue, part or supplement (0..1 string)
    issue = models.CharField(max_length=50, null=True, blank=True)
    # Date the article was added to the database (0..1 dateTime)
    articleDate = models.DateTimeField(null=True, blank=True)
    # Copyright notice for the full article or artifact (0..1 markdown)
    copyright = models.TextField(null=True, blank=True)
    
    class Meta:
        db_table = 'cited_artifact_publication_form'


class CitedArtifactWebLocation(BackboneElement):
    """Used for any URL for the article or artifact cited"""
    # Cited artifact this web location belongs to
    cited_artifact = models.ForeignKey('CitedArtifact', on_delete=models.CASCADE, related_name='web_locations', null=True, blank=True)
    # The specific URL (0..1 uri)
    url = models.URLField(null=True, blank=True)
    
    class Meta:
        db_table = 'cited_artifact_web_location'


class CitedArtifact(BackboneElement):
    """The article or artifact being described"""
    # Citation this cited artifact belongs to
    citation = models.OneToOneField('Citation', on_delete=models.CASCADE, related_name='cited_artifact', null=True, blank=True)
    # When the cited artifact was accessed (0..1 dateTime)
    dateAccessed = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'cited_artifact'


class Citation(MetadataResource):
    """A description of identification, location, or contributorship of a publication"""
    
    # Approval date (0..1 date)
    approvalDate = models.DateField(null=True, blank=True)
    # Last review date (0..1 date)
    lastReviewDate = models.DateField(null=True, blank=True)
    # When the citation record is expected to be used (0..1 Period)
    effectivePeriod = models.ForeignKey('components.Period', null=True, blank=True, on_delete=models.SET_NULL, related_name='citations')
    
    class Meta:
        db_table = 'citation'
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['date']),
            models.Index(fields=['publisher']),
        ]
    
    def __str__(self):
        return f"Citation(title={self.title}, status={self.status})"