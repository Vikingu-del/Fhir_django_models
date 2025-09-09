"""Django app configuration for FHIR Django Models."""

from django.apps import AppConfig


class FhirDjangoModelsConfig(AppConfig):
    """Configuration for the FHIR Django Models app."""
    
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fhir_django_models'
    verbose_name = 'FHIR Django Models'
    
    def ready(self):
        """Perform initialization when Django is ready."""
        pass