# FHIR Django Models

A Django package providing models for FHIR (Fast Healthcare Interoperability Resources) standard. This package allows easy integration of FHIR complex types into Django applications and can be installed via pip for reuse across medical applications.

## Features

- Complete Django models for FHIR complex types
- Ready-to-use Patient, Practitioner, and Observation resources
- Generic relations for flexible FHIR data structures
- Easy integration with existing Django projects
- PostgreSQL and SQL database compatible

## Installation

```bash
pip install fhir-django-models
```

## Quick Start

1. Add `fhir_django_models` to your Django `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    # ... your other apps
    'fhir_django_models',
]
```

2. Run migrations to create the FHIR tables:

```bash
python manage.py makemigrations fhir_django_models
python manage.py migrate
```

3. Start using FHIR models in your code:

```python
from fhir_django_models import Patient, HumanName, Identifier

# Create a patient
patient = Patient.objects.create(
    id="patient-123",
    active=True,
    gender="male",
    birth_date="1990-01-01"
)

# Add a name
name = HumanName.objects.create(
    content_object=patient,
    use="official",
    family="Doe",
    given=["John", "Michael"]
)

# Add an identifier
identifier = Identifier.objects.create(
    content_object=patient,
    use="usual",
    system="http://hospital.example.org/patients",
    value="12345"
)
```

## Available Models

### Core Models
- `FHIRBaseModel` - Base class for all FHIR resources
- `Identifier` - FHIR Identifier complex type
- `CodeableConcept` - FHIR CodeableConcept complex type
- `Coding` - FHIR Coding complex type
- `HumanName` - FHIR HumanName complex type
- `ContactPoint` - FHIR ContactPoint complex type
- `Address` - FHIR Address complex type

### Patient Models
- `Patient` - FHIR Patient resource
- `PatientContact` - Patient contact information
- `PatientCommunication` - Patient communication preferences

### Practitioner Models
- `Practitioner` - FHIR Practitioner resource
- `PractitionerQualification` - Practitioner qualifications

### Observation Models
- `Observation` - FHIR Observation resource
- `ObservationComponent` - Observation components

## Requirements

- Python >= 3.8
- Django >= 3.2

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
