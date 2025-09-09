#!/usr/bin/env python
"""Setup script for FHIR Django Models package."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="fhir-django-models",
    version="0.1.0",
    author="Erik",
    author_email="",
    description="Django models for FHIR (Fast Healthcare Interoperability Resources) standard",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Vikingu-del/Fhir_django_models",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Healthcare Industry",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Framework :: Django",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.0",
        "Framework :: Django :: 4.1",
        "Framework :: Django :: 4.2",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
    ],
    python_requires=">=3.8",
    install_requires=[
        "Django>=3.2",
    ],
    keywords="fhir healthcare django models medical interoperability",
    project_urls={
        "Bug Reports": "https://github.com/Vikingu-del/Fhir_django_models/issues",
        "Source": "https://github.com/Vikingu-del/Fhir_django_models",
    },
)