from django.db import models
from django.core.exceptions import ValidationError
from abstractClasses.models import Element


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


class CanonicalField(models.CharField):
    """
    Custom field for FHIR canonical URLs
    A URI that refers to a resource by its canonical URL with optional version
    """
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 512)
        super().__init__(*args, **kwargs)
    
    def validate(self, value, model_instance):
        super().validate(value, model_instance)
        if value and not self._is_valid_canonical(value):
            raise ValidationError("Invalid canonical URL format")
    
    def _is_valid_canonical(self, value):
        """Basic validation for canonical URL format"""
        # Must be absolute URI or fragment identifier
        if value.startswith('#'):
            return True  # Fragment identifier
        # Should be absolute URI (simplified check)
        return '://' in value or value.startswith('urn:')
    
    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        return name, 'components.reference.CanonicalField', args, kwargs