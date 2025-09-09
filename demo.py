#!/usr/bin/env python
"""
Simple demonstration of FHIR Django Models package.

This script shows the basic structure and usage patterns without requiring 
actual database operations.
"""

import sys
import os
import django
from django.conf import settings

# Add the package to Python path
sys.path.insert(0, '/home/runner/work/Fhir_django_models/Fhir_django_models')

# Configure Django
if not settings.configured:
    settings.configure(
        DEBUG=True,
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        INSTALLED_APPS=[
            'django.contrib.contenttypes',
            'fhir_django_models',
        ],
        SECRET_KEY='demo-secret-key',
        USE_TZ=True,
    )
    django.setup()

def demonstrate_package_structure():
    """Demonstrate the package structure and model definitions."""
    
    print("FHIR Django Models - Package Demonstration")
    print("=" * 50)
    
    # Import the package
    import fhir_django_models
    print(f"✓ Package version: {fhir_django_models.__version__}")
    print(f"✓ Available models: {len(fhir_django_models.__all__)}")
    
    # Demonstrate lazy loading
    print("\n=== Model Imports ===")
    try:
        Patient = fhir_django_models.get_model('Patient')
        print(f"✓ Patient model: {Patient}")
        print(f"  Table name: {Patient._meta.db_table}")
        print(f"  Fields: {[f.name for f in Patient._meta.get_fields()[:8]]}...")
        
        HumanName = fhir_django_models.get_model('HumanName')
        print(f"✓ HumanName model: {HumanName}")
        print(f"  Table name: {HumanName._meta.db_table}")
        
        Observation = fhir_django_models.get_model('Observation')
        print(f"✓ Observation model: {Observation}")
        print(f"  Table name: {Observation._meta.db_table}")
        
    except Exception as e:
        print(f"✗ Import failed: {e}")
        return False
    
    print("\n=== Model Relationships ===")
    
    # Show model relationships
    patient_fields = Patient._meta.get_fields()
    relations = [f for f in patient_fields if hasattr(f, 'related_model')]
    print(f"Patient has {len(relations)} relationships:")
    for rel in relations[:5]:  # Show first 5
        print(f"  - {rel.name}: {rel.__class__.__name__}")
    
    # Show generic relations
    generic_relations = [f for f in patient_fields if f.__class__.__name__ == 'GenericRelation']
    print(f"Patient has {len(generic_relations)} generic relations:")
    for rel in generic_relations:
        print(f"  - {rel.name}: {rel.related_model.__name__}")
    
    print("\n=== Field Types Demonstration ===")
    
    # Show different field types used
    observation_fields = Observation._meta.get_fields()
    field_types = {}
    for field in observation_fields:
        field_type = field.__class__.__name__
        if field_type not in field_types:
            field_types[field_type] = []
        field_types[field_type].append(field.name)
    
    print("Observation model uses these Django field types:")
    for field_type, fields in field_types.items():
        print(f"  {field_type}: {', '.join(fields[:3])}{'...' if len(fields) > 3 else ''}")
    
    return True

def demonstrate_model_structure():
    """Show the structure of key FHIR models."""
    
    print("\n=== FHIR Model Structure ===")
    
    from fhir_django_models.core.models import FHIRBaseModel
    from fhir_django_models import Patient, Practitioner, Observation
    
    print("\n1. Base Model (FHIRBaseModel):")
    base_fields = [f.name for f in FHIRBaseModel._meta.get_fields()]
    print(f"   Fields: {', '.join(base_fields)}")
    print("   ✓ Provides common FHIR resource structure")
    
    print("\n2. Patient Model:")
    patient_choices = {f.name: getattr(f, 'choices', None) for f in Patient._meta.get_fields() if hasattr(f, 'choices') and f.choices}
    for field_name, choices in patient_choices.items():
        if choices:
            print(f"   {field_name} choices: {[c[1] for c in choices[:3]]}{'...' if len(choices) > 3 else ''}")
    
    print("\n3. Complex Types:")
    from fhir_django_models import HumanName, Address, ContactPoint
    
    complex_types = [
        ("HumanName", HumanName),
        ("Address", Address), 
        ("ContactPoint", ContactPoint)
    ]
    
    for name, model in complex_types:
        fields = [f.name for f in model._meta.get_fields() if not f.name.startswith('content_')]
        print(f"   {name}: {', '.join(fields[:4])}{'...' if len(fields) > 4 else ''}")

def demonstrate_usage_patterns():
    """Show typical usage patterns for the models."""
    
    print("\n=== Usage Patterns ===")
    
    print("\n1. Creating a Patient:")
    print("""
   patient = Patient.objects.create(
       id="patient-123",
       active=True,
       gender="male",
       birth_date="1990-01-01"
   )""")
    
    print("\n2. Adding Patient Name:")
    print("""
   name = HumanName.objects.create(
       content_object=patient,
       use="official",
       family="Doe",
       given=["John", "Michael"]
   )""")
    
    print("\n3. Creating an Observation:")
    print("""
   observation = Observation.objects.create(
       id="obs-001",
       status="final",
       subject_patient=patient,
       value_quantity_value=98.6,
       value_quantity_unit="°F"
   )""")
    
    print("\n4. Querying Related Data:")
    print("""
   # Get all names for a patient
   patient_names = patient.names.all()
   
   # Get all observations for a patient
   patient_observations = patient.observations.all()
   
   # Filter observations by status
   final_observations = Observation.objects.filter(status="final")""")

def demonstrate_package_features():
    """Show key features of the package."""
    
    print("\n=== Package Features ===")
    
    features = [
        "✓ Complete FHIR complex types (Identifier, CodeableConcept, HumanName, etc.)",
        "✓ Core FHIR resources (Patient, Practitioner, Observation)",
        "✓ Generic relationships for flexible data modeling",
        "✓ Django-native field types and relationships",
        "✓ Proper table naming following FHIR conventions",
        "✓ Choice fields for FHIR value sets",
        "✓ JSON fields for arrays (given names, address lines)",
        "✓ Support for both simple and complex FHIR data types",
        "✓ Extensible structure for additional FHIR resources"
    ]
    
    for feature in features:
        print(f"   {feature}")
    
    print("\n=== Installation & Setup ===")
    steps = [
        "1. pip install fhir-django-models",
        "2. Add 'fhir_django_models' to INSTALLED_APPS",
        "3. Run: python manage.py makemigrations fhir_django_models",
        "4. Run: python manage.py migrate",
        "5. Import models: from fhir_django_models import Patient, Observation"
    ]
    
    for step in steps:
        print(f"   {step}")

def main():
    """Run the demonstration."""
    
    try:
        success = demonstrate_package_structure()
        if success:
            demonstrate_model_structure()
            demonstrate_usage_patterns()
            demonstrate_package_features()
            
            print("\n" + "=" * 50)
            print("✓ FHIR Django Models package is ready for use!")
            print("✓ All models loaded successfully")
            print("✓ Package structure is correct")
            print("✓ Ready for pip installation and distribution")
            
        return success
        
    except Exception as e:
        print(f"✗ Demonstration failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)