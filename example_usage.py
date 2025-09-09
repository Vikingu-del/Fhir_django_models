#!/usr/bin/env python
"""
Example usage of FHIR Django Models package.

This script demonstrates how to use the fhir-django-models package
in a Django application to create and manage FHIR resources.
"""

import os
import sys
import django
from django.conf import settings
from django.core.management import execute_from_command_line

# Configure Django settings
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
        SECRET_KEY='example-secret-key',
        USE_TZ=True,
    )
    django.setup()

def create_sample_data():
    """Create sample FHIR data to demonstrate the package."""
    
    from fhir_django_models import (
        Patient, HumanName, Identifier, ContactPoint, Address,
        Practitioner, PractitionerQualification,
        Observation, CodeableConcept, Coding
    )
    
    print("=== Creating Sample FHIR Data ===\n")
    
    # Create a patient
    print("1. Creating Patient...")
    patient = Patient.objects.create(
        id="patient-001",
        active=True,
        gender="female",
        birth_date="1985-07-12"
    )
    
    # Add patient name
    patient_name = HumanName.objects.create(
        content_object=patient,
        use="official",
        family="Smith",
        given=["Jane", "Elizabeth"],
        text="Jane Elizabeth Smith"
    )
    
    # Add patient identifier
    patient_id = Identifier.objects.create(
        content_object=patient,
        use="usual",
        system="http://hospital.example.org/patients",
        value="PAT001"
    )
    
    # Add patient contact
    patient_phone = ContactPoint.objects.create(
        content_object=patient,
        system="phone",
        value="+1-555-0123",
        use="home"
    )
    
    # Add patient address
    patient_address = Address.objects.create(
        content_object=patient,
        use="home",
        type="physical",
        line=["123 Main Street", "Apt 4B"],
        city="Springfield",
        state="IL",
        postal_code="62701",
        country="USA"
    )
    
    print(f"   ✓ Created patient: {patient}")
    print(f"   ✓ Added name: {patient_name}")
    print(f"   ✓ Added identifier: {patient_id.value}")
    print(f"   ✓ Added phone: {patient_phone.value}")
    print(f"   ✓ Added address in {patient_address.city}, {patient_address.state}")
    
    # Create a practitioner
    print("\n2. Creating Practitioner...")
    practitioner = Practitioner.objects.create(
        id="practitioner-001",
        active=True,
        gender="male",
        birth_date="1975-03-20"
    )
    
    # Add practitioner name
    practitioner_name = HumanName.objects.create(
        content_object=practitioner,
        use="official",
        family="Johnson",
        given=["Robert", "David"],
        prefix=["Dr."],
        text="Dr. Robert David Johnson"
    )
    
    # Add practitioner qualification
    qualification = PractitionerQualification.objects.create(
        practitioner=practitioner,
        code="MD",
        code_display="Doctor of Medicine",
        issuer="State Medical Board"
    )
    
    print(f"   ✓ Created practitioner: {practitioner}")
    print(f"   ✓ Added qualification: {qualification.code_display}")
    
    # Create an observation
    print("\n3. Creating Observation...")
    observation = Observation.objects.create(
        id="observation-001",
        status="final",
        subject_patient=patient,
        performer_practitioner=practitioner,
        effective_date_time="2024-01-15T10:30:00Z",
        value_quantity_value=98.6,
        value_quantity_unit="°F",
        value_quantity_system="http://unitsofmeasure.org",
        value_quantity_code="[degF]"
    )
    
    # Add observation code
    obs_code_concept = CodeableConcept.objects.create(
        content_object=observation,
        text="Body Temperature"
    )
    
    obs_coding = Coding.objects.create(
        codeable_concept=obs_code_concept,
        system="http://loinc.org",
        code="8310-5",
        display="Body temperature"
    )
    
    print(f"   ✓ Created observation: {observation}")
    print(f"   ✓ Temperature: {observation.value_quantity_value}{observation.value_quantity_unit}")
    print(f"   ✓ Code: {obs_coding.display} ({obs_coding.code})")
    
    return patient, practitioner, observation

def query_sample_data():
    """Demonstrate querying FHIR data."""
    
    from fhir_django_models import Patient, Practitioner, Observation
    
    print("\n=== Querying FHIR Data ===\n")
    
    # Query patients
    patients = Patient.objects.all()
    print(f"Total patients: {patients.count()}")
    
    for patient in patients:
        print(f"  Patient: {patient}")
        print(f"    Active: {patient.active}")
        print(f"    Gender: {patient.gender}")
        print(f"    Birth Date: {patient.birth_date}")
        
        # Get patient names
        names = patient.names.all()
        for name in names:
            print(f"    Name: {name.text} (use: {name.use})")
        
        # Get patient identifiers
        identifiers = patient.identifiers.all()
        for identifier in identifiers:
            print(f"    ID: {identifier.value} (system: {identifier.system})")
        
        # Get patient observations
        observations = patient.observations.all()
        print(f"    Observations: {observations.count()}")
        for obs in observations:
            print(f"      - {obs} (status: {obs.status})")
    
    # Query practitioners
    practitioners = Practitioner.objects.all()
    print(f"\nTotal practitioners: {practitioners.count()}")
    
    for practitioner in practitioners:
        print(f"  Practitioner: {practitioner}")
        qualifications = practitioner.qualifications.all()
        for qual in qualifications:
            print(f"    Qualification: {qual.code_display}")
    
    # Query observations
    observations = Observation.objects.all()
    print(f"\nTotal observations: {observations.count()}")
    
    for obs in observations:
        print(f"  Observation: {obs}")
        print(f"    Value: {obs.value_quantity_value} {obs.value_quantity_unit}")
        print(f"    Date: {obs.effective_date_time}")

def main():
    """Main function to run the example."""
    
    print("FHIR Django Models - Example Usage")
    print("=" * 50)
    
    # Create database tables manually
    from django.db import connection
    from django.core.management.sql import sql_create_index
    from django.core.management.color import no_style
    from fhir_django_models.core.models import (
        Identifier, CodeableConcept, Coding, HumanName, ContactPoint, Address
    )
    from fhir_django_models.patient.models import Patient, PatientContact, PatientCommunication
    from fhir_django_models.practitioner.models import Practitioner, PractitionerQualification
    from fhir_django_models.observation.models import Observation, ObservationComponent
    
    print("Creating database tables...")
    
    # Get all models
    models = [
        Patient, Identifier, CodeableConcept, Coding, HumanName, 
        ContactPoint, Address, PatientContact, PatientCommunication,
        Practitioner, PractitionerQualification,
        Observation, ObservationComponent
    ]
    
    style = no_style()
    
    with connection.cursor() as cursor:
        # Create tables
        for model in models:
            sql = connection.ops.sql_create_model(model, style)[0]
            try:
                cursor.execute(sql)
                print(f"   ✓ Created table: {model._meta.db_table}")
            except Exception as e:
                if "already exists" not in str(e):
                    print(f"   ⚠ Warning creating {model._meta.db_table}: {e}")
    
    print("Database setup complete!")
    
    # Create sample data
    patient, practitioner, observation = create_sample_data()
    
    # Query and display data
    query_sample_data()
    
    print("\n=== Summary ===")
    print("✓ Successfully created and queried FHIR resources")
    print("✓ Package is working correctly")
    print("✓ Ready for use in Django applications")
    print("\nTo use in your Django project:")
    print("1. pip install fhir-django-models")
    print("2. Add 'fhir_django_models' to INSTALLED_APPS")
    print("3. Run: python manage.py makemigrations fhir_django_models")
    print("4. Run: python manage.py migrate")
    print("5. Import and use: from fhir_django_models import Patient, ...")

if __name__ == "__main__":
    main()