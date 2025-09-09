from fhir.resources import citation
from components.serializers import (
    convert_identifier, convert_codeable_concept, convert_period
)
from . import models


def convert_citation_summary(django_summary):
    """Convert Django CitationSummary to FHIR Citation.summary"""
    if not django_summary:
        return None
    
    data = {
        'text': django_summary.text
    }
    
    if django_summary.style:
        data['style'] = convert_codeable_concept(django_summary.style)
    
    return data


def convert_citation_classification(django_classification):
    """Convert Django CitationClassification to FHIR Citation.classification"""
    if not django_classification:
        return None
    
    data = {}
    
    if django_classification.type:
        data['type'] = convert_codeable_concept(django_classification.type)
    
    # Get classifiers
    classifiers = []
    for classifier in django_classification.classifiers.all():
        fhir_classifier = convert_codeable_concept(classifier)
        if fhir_classifier:
            classifiers.append(fhir_classifier)
    if classifiers:
        data['classifier'] = classifiers
    
    return data


def convert_citation_status_date(django_status_date):
    """Convert Django CitationStatusDate to FHIR Citation.statusDate"""
    if not django_status_date:
        return None
    
    data = {
        'activity': convert_codeable_concept(django_status_date.activity),
        'period': convert_period(django_status_date.period)
    }
    
    if django_status_date.actual is not None:
        data['actual'] = django_status_date.actual
    
    return data


def convert_cited_artifact_version(django_version):
    """Convert Django CitedArtifactVersion to FHIR CitedArtifact.version"""
    if not django_version:
        return None
    
    data = {
        'value': django_version.value
    }
    
    if django_version.baseCitation:
        data['baseCitation'] = {'reference': f'Citation/{django_version.baseCitation.fhir_id}'}
    
    return data


def convert_cited_artifact_title(django_title):
    """Convert Django CitedArtifactTitle to FHIR CitedArtifact.title"""
    if not django_title:
        return None
    
    data = {
        'text': django_title.text
    }
    
    if django_title.language:
        data['language'] = convert_codeable_concept(django_title.language)
    
    return data


def convert_cited_artifact_abstract(django_abstract):
    """Convert Django CitedArtifactAbstract to FHIR CitedArtifact.abstract"""
    if not django_abstract:
        return None
    
    data = {
        'text': django_abstract.text
    }
    
    if django_abstract.type:
        data['type'] = convert_codeable_concept(django_abstract.type)
    if django_abstract.language:
        data['language'] = convert_codeable_concept(django_abstract.language)
    if django_abstract.copyright:
        data['copyright'] = django_abstract.copyright
    
    return data


def convert_cited_artifact(django_cited_artifact):
    """Convert Django CitedArtifact to FHIR Citation.citedArtifact"""
    if not django_cited_artifact:
        return None
    
    data = {}
    
    if django_cited_artifact.dateAccessed:
        data['dateAccessed'] = django_cited_artifact.dateAccessed.isoformat()
    
    # Identifiers
    identifiers = []
    for identifier in django_cited_artifact.identifiers.all():
        fhir_identifier = convert_identifier(identifier)
        if fhir_identifier:
            identifiers.append(fhir_identifier)
    if identifiers:
        data['identifier'] = identifiers
    
    # Related identifiers
    related_identifiers = []
    for identifier in django_cited_artifact.related_identifiers.all():
        fhir_identifier = convert_identifier(identifier)
        if fhir_identifier:
            related_identifiers.append(fhir_identifier)
    if related_identifiers:
        data['relatedIdentifier'] = related_identifiers
    
    # Version
    if hasattr(django_cited_artifact, 'version') and django_cited_artifact.version:
        data['version'] = convert_cited_artifact_version(django_cited_artifact.version)
    
    # Current state
    current_states = []
    for state in django_cited_artifact.current_states.all():
        fhir_state = convert_codeable_concept(state)
        if fhir_state:
            current_states.append(fhir_state)
    if current_states:
        data['currentState'] = current_states
    
    # Status dates
    status_dates = []
    for status_date in django_cited_artifact.status_dates.all():
        fhir_status_date = convert_citation_status_date(status_date)
        if fhir_status_date:
            status_dates.append(fhir_status_date)
    if status_dates:
        data['statusDate'] = status_dates
    
    # Titles
    titles = []
    for title in django_cited_artifact.titles.all():
        fhir_title = convert_cited_artifact_title(title)
        if fhir_title:
            titles.append(fhir_title)
    if titles:
        data['title'] = titles
    
    # Abstracts
    abstracts = []
    for abstract in django_cited_artifact.abstracts.all():
        fhir_abstract = convert_cited_artifact_abstract(abstract)
        if fhir_abstract:
            abstracts.append(fhir_abstract)
    if abstracts:
        data['abstract'] = abstracts
    
    return data


def convert_citation(django_citation):
    """Convert Django Citation to FHIR Citation"""
    if not django_citation:
        return None
    
    data = {
        'resourceType': 'Citation',
        'id': django_citation.fhir_id,
        'status': django_citation.status
    }
    
    # MetadataResource fields
    if django_citation.url:
        data['url'] = django_citation.url
    if django_citation.version:
        data['version'] = django_citation.version
    if django_citation.name:
        data['name'] = django_citation.name
    if django_citation.title:
        data['title'] = django_citation.title
    if django_citation.experimental is not None:
        data['experimental'] = django_citation.experimental
    if django_citation.date:
        data['date'] = django_citation.date.isoformat()
    if django_citation.publisher:
        data['publisher'] = django_citation.publisher
    if django_citation.description:
        data['description'] = django_citation.description
    if django_citation.purpose:
        data['purpose'] = django_citation.purpose
    if django_citation.copyright:
        data['copyright'] = django_citation.copyright
    if django_citation.copyrightLabel:
        data['copyrightLabel'] = django_citation.copyrightLabel
    
    # Citation-specific fields
    if django_citation.approvalDate:
        data['approvalDate'] = django_citation.approvalDate.isoformat()
    if django_citation.lastReviewDate:
        data['lastReviewDate'] = django_citation.lastReviewDate.isoformat()
    if django_citation.effectivePeriod:
        data['effectivePeriod'] = convert_period(django_citation.effectivePeriod)
    
    # Identifiers
    identifiers = []
    for identifier in django_citation.identifiers.all():
        fhir_identifier = convert_identifier(identifier)
        if fhir_identifier:
            identifiers.append(fhir_identifier)
    if identifiers:
        data['identifier'] = identifiers
    
    # Current states
    current_states = []
    for state in django_citation.current_states.all():
        fhir_state = convert_codeable_concept(state)
        if fhir_state:
            current_states.append(fhir_state)
    if current_states:
        data['currentState'] = current_states
    
    # Status dates
    status_dates = []
    for status_date in django_citation.status_dates.all():
        fhir_status_date = convert_citation_status_date(status_date)
        if fhir_status_date:
            status_dates.append(fhir_status_date)
    if status_dates:
        data['statusDate'] = status_dates
    
    # Summaries
    summaries = []
    for summary in django_citation.summaries.all():
        fhir_summary = convert_citation_summary(summary)
        if fhir_summary:
            summaries.append(fhir_summary)
    if summaries:
        data['summary'] = summaries
    
    # Classifications
    classifications = []
    for classification in django_citation.classifications.all():
        fhir_classification = convert_citation_classification(classification)
        if fhir_classification:
            classifications.append(fhir_classification)
    if classifications:
        data['classification'] = classifications
    
    # Cited artifact
    if hasattr(django_citation, 'cited_artifact') and django_citation.cited_artifact:
        data['citedArtifact'] = convert_cited_artifact(django_citation.cited_artifact)
    
    return citation.Citation(**data)