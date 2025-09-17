# FHIR Django Models

A Django-based implementation of FHIR (Fast Healthcare Interoperability Resources) R5 data models, providing a comprehensive set of Django models that represent FHIR resources and data types.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Running Migrations](#running-migrations)
- [Project Structure](#project-structure)
- [Development Setup](#development-setup)
- [Contributing](#contributing)
- [FHIR Resources Implemented](#fhir-resources-implemented)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [License](#license)

## 🔍 Overview

This project provides Django model implementations for FHIR R5 resources, enabling healthcare applications to store, validate, and manipulate FHIR data using Django's ORM. The models follow FHIR specifications closely while leveraging Django's powerful features for data validation, relationships, and database management.

## ✨ Features

- **Complete FHIR R5 Models**: Implementation of core FHIR resources and data types
- **Django ORM Integration**: Full compatibility with Django's ORM for queries and relationships
- **FHIR Validation**: Built-in validation rules following FHIR specifications
- **RESTful APIs**: Django REST Framework integration for FHIR-compliant APIs
- **Extensible Architecture**: Easy to extend with custom FHIR extensions
- **Database Agnostic**: Works with PostgreSQL, MySQL, SQLite, and other Django-supported databases

## 🚀 Installation

### Prerequisites

- Python 3.11+ 
- PostgreSQL (recommended) or other Django-supported database
- Git

### Step 1: Clone the Repository

```bash
git clone https://github.com/your-username/fhir-django-models.git
cd fhir-django-models
```

### Step 2: Create Virtual Environment

```bash
python -m venv django_env
source django_env/bin/activate  # On Windows: django_env\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Database Setup

#### For PostgreSQL (Recommended):
1. Install PostgreSQL:
   ```bash
   # macOS
   brew install postgresql
   
   # Ubuntu/Debian
   sudo apt-get install postgresql postgresql-contrib
   
   # CentOS/RHEL
   sudo yum install postgresql postgresql-server
   ```

2. Create database:
   ```bash
   createdb fhir_demo
   ```

3. Update `fhir_demo/settings.py` with your database credentials:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'fhir_demo',
           'USER': 'your_username',
           'PASSWORD': 'your_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

#### For SQLite (Development):
The project is configured to use SQLite by default for development. No additional setup required.

### Step 5: Environment Variables

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=postgresql://username:password@localhost:5432/fhir_demo
ALLOWED_HOSTS=localhost,127.0.0.1
```

## 🗃️ Running Migrations

### Step 1: Create Migrations

```bash
python manage.py makemigrations
```

### Step 2: Apply Migrations

```bash
python manage.py migrate
```

### Step 3: Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### Step 4: Run Development Server

```bash
python manage.py runserver
```

Visit `http://localhost:8000` to access the application.

## 📁 Project Structure

```
fhir-django-models/
├── abstractClasses/          # FHIR abstract base classes
│   ├── models.py            # Base FHIR models (Resource, Element, etc.)
│   └── ...
├── components/              # FHIR data types and components
│   ├── models.py           # Complex data types (Identifier, Period, etc.)
│   ├── reference.py        # Reference model and canonical fields
│   └── ...
├── patient/                # Patient resource implementation
├── practitioner/           # Practitioner resource implementation
├── organization/           # Organization resource implementation
├── encounter/              # Encounter resource implementation
├── observation/            # Observation resource implementation
├── location/               # Location resource implementation
├── endpoint/               # Endpoint resource implementation
├── healthcareservice/      # HealthcareService resource implementation
├── citation/               # Citation resource implementation
├── core/                   # Core Django app
├── fhir_demo/              # Django project settings
│   ├── settings.py         # Main settings file
│   ├── urls.py            # URL configuration
│   └── ...
├── requirements.txt        # Python dependencies
├── manage.py              # Django management script
└── README.md              # This file
```

## 🛠️ Development Setup

### Code Style

This project follows PEP 8 and Django coding standards. We recommend using:

```bash
pip install black flake8 isort
```

Format your code before committing:
```bash
black .
isort .
flake8 .
```

### Pre-commit Hooks

Install pre-commit hooks to ensure code quality:

```bash
pip install pre-commit
pre-commit install
```

### Running Tests

```bash
python manage.py test
```

For coverage reporting:
```bash
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html  # Generates HTML coverage report
```

## 🤝 Contributing

We welcome contributions from the open-source community! Here's how you can help:

### Getting Started

1. **Fork the Repository**
   ```bash
   git fork https://github.com/your-username/fhir-django-models.git
   ```

2. **Create a Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make Your Changes**
   - Follow FHIR R5 specifications
   - Write tests for new functionality
   - Update documentation as needed

4. **Test Your Changes**
   ```bash
   python manage.py test
   python manage.py makemigrations --dry-run
   ```

5. **Commit and Push**
   ```bash
   git add .
   git commit -m "Add: your descriptive commit message"
   git push origin feature/your-feature-name
   ```

6. **Create Pull Request**
   - Describe your changes clearly
   - Reference any related issues
   - Ensure all tests pass

### Contribution Guidelines

- **FHIR Compliance**: All models must follow FHIR R5 specifications
- **Documentation**: Update docstrings and README for new features
- **Testing**: Write unit tests for new models and functionality
- **Code Quality**: Follow PEP 8 and Django best practices
- **Validation**: Implement appropriate FHIR validation rules

### Areas for Contribution

1. **New FHIR Resources**: Implement missing FHIR resources
2. **Validation Rules**: Add FHIR-compliant validation logic
3. **API Endpoints**: Create RESTful APIs for resources
4. **Documentation**: Improve documentation and examples
5. **Testing**: Expand test coverage
6. **Performance**: Optimize database queries and indexing
7. **Extensions**: Implement FHIR extension mechanisms

### Reporting Issues

Please use GitHub Issues to report:
- Bugs or errors
- Feature requests
- Documentation improvements
- Performance issues

**Issue Template:**
```markdown
## Description
Brief description of the issue

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Steps to Reproduce
1. Step one
2. Step two
3. Step three

## Environment
- Python version:
- Django version:
- Database:
- OS:
```

## 📊 FHIR Resources Implemented

### ✅ Completed
- **AbstractClasses**: Base FHIR models
- **Components**: Core data types (Identifier, Period, Quantity, etc.)
- **Patient**: Patient resource with related persons
- **Practitioner**: Healthcare providers and roles
- **Organization**: Healthcare organizations
- **Location**: Physical locations
- **Endpoint**: Technical endpoints
- **HealthcareService**: Services offered
- **Encounter**: Patient encounters
- **Observation**: Clinical observations
- **Citation**: Academic citations

### 🚧 In Progress
- **RelatedArtifact**: Supporting documentation (commented out)
- **Additional validation rules**
- **FHIR extensions mechanism**

### 📋 Planned
- **Appointment**: Scheduled appointments
- **Medication**: Medication resources
- **DiagnosticReport**: Diagnostic reports
- **Procedure**: Medical procedures
- **Condition**: Health conditions
- **AllergyIntolerance**: Allergy information

## 📖 API Documentation

### Django Admin Interface

Access the Django admin at `http://localhost:8000/admin/` to:
- Browse and edit FHIR resources
- Test data relationships
- Validate FHIR compliance

### REST API Endpoints

The project includes Django REST Framework for API development:

```python
# Example API endpoints (when implemented)
GET    /api/patients/           # List patients
POST   /api/patients/           # Create patient
GET    /api/patients/{id}/      # Get patient by ID
PUT    /api/patients/{id}/      # Update patient
DELETE /api/patients/{id}/      # Delete patient
```

### Model Usage Examples

```python
from patient.models import Patient
from components.models import Identifier, HumanName

# Create a patient
patient = Patient.objects.create(
    active=True,
    gender='male'
)

# Add identifier
identifier = Identifier.objects.create(
    system='http://hospital.example.org',
    value='123456',
    patient=patient
)

# Add name
name = HumanName.objects.create(
    use='official',
    family='Smith',
    patient=patient
)
name.given.add('John')
```

## 🧪 Testing

### Running Specific Tests

```bash
# Test specific app
python manage.py test patient

# Test specific model
python manage.py test patient.tests.PatientModelTest

# Test with verbose output
python manage.py test --verbosity=2
```

### Test Data

Use Django fixtures for consistent test data:

```bash
python manage.py loaddata test_data.json
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: Check this README and inline documentation
- **Issues**: Report bugs and request features on GitHub Issues
- **Discussions**: Join community discussions on GitHub Discussions
- **Email**: Contact maintainers at [your-email@example.com]

## 🙏 Acknowledgments

- **FHIR Community**: For developing the FHIR standards
- **Django Community**: For the excellent web framework
- **Contributors**: All open-source contributors to this project

## 🔄 Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history and updates.

---

**Made with ❤️ by the open-source community**

*This project is not affiliated with HL7 or the official FHIR specification, but aims to provide a Django-compatible implementation of FHIR resources.*
