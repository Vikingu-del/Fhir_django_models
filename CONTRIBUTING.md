# Contributing to FHIR Django Models

Thank you for your interest in contributing to FHIR Django Models! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

### 1. Types of Contributions

We welcome the following types of contributions:

- **Bug Reports**: Found a bug? Please report it!
- **Feature Requests**: Have an idea for improvement? Let us know!
- **Code Contributions**: Implement new features or fix bugs
- **Documentation**: Improve documentation and examples
- **Tests**: Add or improve test coverage
- **Performance**: Optimize queries and database operations

### 2. Getting Started

#### Fork and Clone
```bash
# Fork the repository on GitHub
git clone https://github.com/YOUR_USERNAME/fhir-django-models.git
cd fhir-django-models
```

#### Set Up Development Environment
```bash
# Create virtual environment
python -m venv django_env
source django_env/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Development dependencies

# Set up pre-commit hooks
pre-commit install
```

#### Create Feature Branch
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b bugfix/issue-number
```

### 3. Development Guidelines

#### Code Style
- Follow PEP 8 for Python code
- Use Django coding conventions
- Write clear, descriptive variable and function names
- Add docstrings to all classes and functions

#### FHIR Compliance
- All models must follow FHIR R5 specifications
- Implement proper validation rules
- Use correct FHIR data types and cardinalities
- Reference official FHIR documentation: https://hl7.org/fhir/R5/

#### Model Design Principles
```python
# Example of a well-designed FHIR model
class Patient(DomainResource):
    """A person or animal receiving care or other health-related services"""
    
    # Use appropriate field types
    active = models.BooleanField(null=True, blank=True)
    
    # Follow FHIR naming conventions
    birthDate = models.DateField(null=True, blank=True)
    
    # Implement proper relationships
    name = models.ManyToManyField('components.HumanName', blank=True, related_name='patients')
    
    # Add validation
    def clean(self):
        super().clean()
        # FHIR-specific validation rules
        if self.deceased_boolean and self.deceased_datetime:
            raise ValidationError("Cannot have both deceased boolean and datetime")
    
    class Meta:
        db_table = 'patient'
        indexes = [
            models.Index(fields=['active']),
            models.Index(fields=['birthDate']),
        ]
```

#### Testing Requirements
- Write unit tests for all new models
- Include validation testing
- Test model relationships
- Use Django's TestCase or TransactionTestCase

```python
# Example test
class PatientModelTest(TestCase):
    def test_patient_creation(self):
        patient = Patient.objects.create(active=True)
        self.assertTrue(patient.active)
    
    def test_patient_validation(self):
        with self.assertRaises(ValidationError):
            # Test validation rules
            pass
```

### 4. Pull Request Process

#### Before Submitting
1. **Run Tests**: Ensure all tests pass
   ```bash
   python manage.py test
   ```

2. **Check Migrations**: Verify migrations work correctly
   ```bash
   python manage.py makemigrations --dry-run
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Code Quality**: Run linting and formatting
   ```bash
   black .
   isort .
   flake8 .
   ```

4. **Documentation**: Update documentation if needed

#### Pull Request Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## FHIR Compliance
- [ ] Follows FHIR R5 specifications
- [ ] Includes appropriate validation
- [ ] Maintains data type integrity

## Testing
- [ ] Tests pass locally
- [ ] New tests added for new functionality
- [ ] Migration tests completed

## Documentation
- [ ] Code is well-documented
- [ ] README updated if needed
- [ ] Changelog updated

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Tests added/updated
- [ ] Documentation updated
```

### 5. Specific Contribution Areas

#### Adding New FHIR Resources

1. **Research**: Study the FHIR specification for the resource
2. **Plan**: Design the Django model structure
3. **Implement**: Create the model with proper fields and relationships
4. **Validate**: Add FHIR validation rules
5. **Test**: Write comprehensive tests
6. **Document**: Add docstrings and examples

#### Example Implementation Steps:
```python
# 1. Create the model file: newresource/models.py
from abstractClasses.models import DomainResource

class NewResource(DomainResource):
    """FHIR NewResource implementation"""
    # Implementation here
    
# 2. Add to settings.py INSTALLED_APPS
INSTALLED_APPS = [
    # ...
    "newresource",
]

# 3. Create and run migrations
python manage.py makemigrations newresource
python manage.py migrate

# 4. Write tests: newresource/tests.py
# 5. Update documentation
```

#### Improving Validation

Focus areas for validation improvements:
- FHIR invariants and constraints
- Cross-field validation
- Reference validation
- Terminology validation
- Cardinality constraints

#### Performance Optimization

Areas for performance improvements:
- Database indexing
- Query optimization
- Lazy loading
- Caching strategies

### 6. Code Review Process

#### What Reviewers Look For
- FHIR specification compliance
- Code quality and readability
- Test coverage
- Documentation completeness
- Performance implications
- Security considerations

#### Review Criteria
- ✅ Follows FHIR R5 specifications
- ✅ Includes proper validation
- ✅ Has adequate test coverage
- ✅ Is well-documented
- ✅ Follows coding standards
- ✅ Doesn't break existing functionality

### 7. Resources

#### FHIR Documentation
- [FHIR R5 Specification](https://hl7.org/fhir/R5/)
- [FHIR Data Types](https://hl7.org/fhir/R5/datatypes.html)
- [FHIR Resource Definitions](https://hl7.org/fhir/R5/resourcelist.html)

#### Django Documentation
- [Django Models](https://docs.djangoproject.com/en/stable/topics/db/models/)
- [Django Testing](https://docs.djangoproject.com/en/stable/topics/testing/)
- [Django Best Practices](https://docs.djangoproject.com/en/stable/misc/design-philosophies/)

### 8. Getting Help

- **GitHub Issues**: For bug reports and feature requests
- **GitHub Discussions**: For questions and community discussion
- **Documentation**: Check the README and inline documentation
- **FHIR Community**: Join FHIR community discussions

### 9. Recognition

Contributors will be recognized in:
- CHANGELOG.md
- Contributors section in README
- GitHub contributors page

Thank you for helping make FHIR Django Models better! 🚀
