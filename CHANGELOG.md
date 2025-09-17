# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial implementation of FHIR R5 Django models
- Base abstract classes for FHIR resources
- Component models for complex data types
- Patient resource implementation
- Practitioner resource implementation
- Organization resource implementation
- Location resource implementation
- Endpoint resource implementation
- HealthcareService resource implementation
- Encounter resource implementation
- Observation resource implementation
- Citation resource implementation
- Django REST Framework integration setup
- Comprehensive validation rules following FHIR specifications
- Database indexing for performance optimization

### Changed
- Updated requirements.txt to support Python 3.13
- Improved model relationships and foreign key constraints
- Enhanced FHIR validation logic

### Fixed
- Resolved model conflicts between Reference implementations
- Fixed reverse accessor conflicts in encounter models
- Commented out incomplete RelatedArtifact references

### Security
- Added secure settings for production deployment
- Implemented proper validation for FHIR data types

## [0.1.0] - 2024-01-XX

### Added
- Initial project setup
- Basic Django project structure
- FHIR R5 specification research and planning

---

## Release Notes

### Version Numbering
- **Major**: Breaking changes to FHIR model structure
- **Minor**: New FHIR resources or significant features
- **Patch**: Bug fixes and minor improvements

### Migration Notes
When upgrading between versions, always run:
```bash
python manage.py makemigrations
python manage.py migrate
```

### Breaking Changes
None yet - this is the initial release.

### Deprecation Warnings
None yet - this is the initial release.
