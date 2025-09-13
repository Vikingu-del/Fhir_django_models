from django.db import models
from django.core.exceptions import ValidationError
from abstractClasses.models import DomainResource, BackboneElement


class EncounterParticipant(BackboneElement):
    """List of participants involved in the encounter"""
    # Encounter this participant belongs to
    encounter = models.ForeignKey('Encounter', on_delete=models.CASCADE, related_name='participants')
    # Role of participant in encounter (0..* CodeableConcept)
    type = models.ManyToManyField('components.CodeableConcept', blank=True, related_name='encounter_participant_types')
    # Period of time during the encounter that the participant participated (0..1 Period)
    period = models.ForeignKey('components.Period', null=True, blank=True, on_delete=models.SET_NULL, related_name='encounter_participants')
    # Person or device which participated in the encounter (0..1 Reference)
    actor = models.ForeignKey('components.Reference', null=True, blank=True, on_delete=models.SET_NULL, related_name='encounter_participants')
    
    class Meta:
        db_table = 'encounter_participant'


class EncounterReason(BackboneElement):
    """The list of diagnosis relevant to this encounter"""
    # Encounter this reason belongs to
    encounter = models.ForeignKey('Encounter', on_delete=models.CASCADE, related_name='reasons')
    # What the encounter is about (0..* CodeableConcept)
    use = models.ManyToManyField('components.CodeableConcept', blank=True, related_name='encounter_reason_uses')
    # Reason the encounter takes place (coded) (0..* CodeableConcept)
    value = models.ManyToManyField('components.CodeableConcept', blank=True, related_name='encounter_reason_values')
    
    class Meta:
        db_table = 'encounter_reason'


class EncounterDiagnosis(BackboneElement):
    """The list of diagnosis relevant to this encounter"""
    # Encounter this diagnosis belongs to
    encounter = models.ForeignKey('Encounter', on_delete=models.CASCADE, related_name='diagnoses')
    # The diagnosis or procedure relevant to the encounter (1..1 Reference)
    condition = models.ForeignKey('components.Reference', on_delete=models.CASCADE, related_name='encounter_diagnoses')
    # Role that this diagnosis has within the encounter (0..* CodeableConcept)
    use = models.ManyToManyField('components.CodeableConcept', blank=True, related_name='encounter_diagnosis_uses')
    
    class Meta:
        db_table = 'encounter_diagnosis'


class EncounterAdmission(BackboneElement):
    """Details about the admission to a healthcare service"""
    # Encounter this admission belongs to
    encounter = models.OneToOneField('Encounter', on_delete=models.CASCADE, related_name='admission')
    # Pre-admission identifier (0..1 Identifier)
    preAdmissionIdentifier = models.ForeignKey('components.Identifier', null=True, blank=True, on_delete=models.SET_NULL, related_name='encounter_pre_admissions')
    # The location/organization from which the patient came before admission (0..1 Reference)
    origin = models.ForeignKey('components.Reference', null=True, blank=True, on_delete=models.SET_NULL, related_name='encounter_admission_origins')
    # From where patient was admitted (0..1 CodeableConcept)
    admitSource = models.ForeignKey('components.CodeableConcept', null=True, blank=True, on_delete=models.SET_NULL, related_name='encounter_admit_sources')
    # The type of hospital re-admission that has occurred (0..1 CodeableConcept)
    reAdmission = models.ForeignKey('components.CodeableConcept', null=True, blank=True, on_delete=models.SET_NULL, related_name='encounter_readmissions')
    # Diet preferences reported by the patient (0..* CodeableConcept)
    dietPreference = models.ManyToManyField('components.CodeableConcept', blank=True, related_name='encounter_diet_preferences')
    # Special courtesies (0..* CodeableConcept)
    specialCourtesy = models.ManyToManyField('components.CodeableConcept', blank=True, related_name='encounter_special_courtesies')
    # Wheelchair, translator, stretcher, etc. (0..* CodeableConcept)
    specialArrangement = models.ManyToManyField('components.CodeableConcept', blank=True, related_name='encounter_special_arrangements')
    # Location/organization to which the patient is discharged (0..1 Reference)
    destination = models.ForeignKey('components.Reference', null=True, blank=True, on_delete=models.SET_NULL, related_name='encounter_admission_destinations')
    # Category or kind of location after discharge (0..1 CodeableConcept)
    dischargeDisposition = models.ForeignKey('components.CodeableConcept', null=True, blank=True, on_delete=models.SET_NULL, related_name='encounter_discharge_dispositions')
    
    class Meta:
        db_table = 'encounter_admission'


class EncounterLocation(BackboneElement):
    """List of locations where the patient has been during this encounter"""
    # Encounter this location belongs to
    encounter = models.ForeignKey('Encounter', on_delete=models.CASCADE, related_name='locations')
    # Location the encounter takes place (1..1 Reference)
    location = models.ForeignKey('components.Reference', on_delete=models.CASCADE, related_name='encounter_locations')
    # The status of the participants' presence at the specified location (0..1 code)
    status = models.CharField(max_length=16, null=True, blank=True, choices=[
        ('planned', 'Planned'),
        ('active', 'Active'),
        ('reserved', 'Reserved'),
        ('completed', 'Completed')
    ])
    # The physical type of the location (0..1 CodeableConcept)
    form = models.ForeignKey('components.CodeableConcept', null=True, blank=True, on_delete=models.SET_NULL, related_name='encounter_location_forms')
    # Time period during which the patient was present at the location (0..1 Period)
    period = models.ForeignKey('components.Period', null=True, blank=True, on_delete=models.SET_NULL, related_name='encounter_locations')
    
    class Meta:
        db_table = 'encounter_location'


class Encounter(DomainResource):
    """An interaction during which services are provided to the patient"""
    
    # Identifier(s) by which this encounter is known (0..* Identifier)
    # Note: Identifier model handles this via reverse FK
    
    # The current state of the encounter (1..1 code) - Required
    status = models.CharField(max_length=16, choices=[
        ('planned', 'Planned'),
        ('in-progress', 'In Progress'),
        ('on-hold', 'On Hold'),
        ('discharged', 'Discharged'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('discontinued', 'Discontinued'),
        ('entered-in-error', 'Entered in Error'),
        ('unknown', 'Unknown')
    ])
    
    # Concepts representing classification of patient encounter (1..1 CodeableConcept) - Required
    class_field = models.ForeignKey('components.CodeableConcept', on_delete=models.CASCADE, related_name='encounter_classes')
    
    # Indicates the urgency of the encounter (0..1 CodeableConcept)
    priority = models.ForeignKey('components.CodeableConcept', null=True, blank=True, on_delete=models.SET_NULL, related_name='encounter_priorities')
    
    # Specific type of encounter (0..* CodeableConcept)
    type = models.ManyToManyField('components.CodeableConcept', blank=True, related_name='encounter_types')
    
    # Specific type of service (0..* CodeableConcept)
    serviceType = models.ManyToManyField('components.CodeableConcept', blank=True, related_name='encounter_service_types')
    
    # The patient or group present at the encounter (0..1 Reference)
    subject = models.ForeignKey('components.Reference', null=True, blank=True, on_delete=models.SET_NULL, related_name='encounters')
    
    # Where the encounter should occur (0..* Reference)
    subjectStatus = models.ForeignKey('components.CodeableConcept', null=True, blank=True, on_delete=models.SET_NULL, related_name='encounter_subject_statuses')
    
    # Episode(s) of care that this encounter should be recorded against (0..* Reference)
    episodeOfCare = models.ManyToManyField('components.Reference', blank=True, related_name='encounters_episode_of_care')
    
    # The request this encounter satisfies (0..* Reference)
    basedOn = models.ManyToManyField('components.Reference', blank=True, related_name='encounters_based_on')
    
    # Indicates careTeam that is involved in this encounter (0..* Reference)
    careTeam = models.ManyToManyField('components.Reference', blank=True, related_name='encounters_care_team')
    
    # Another Encounter this encounter is part of (0..1 Reference)
    partOf = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='child_encounters')
    
    # The organization that is primarily responsible for this Encounter (0..1 Reference)
    serviceProvider = models.ForeignKey('components.Reference', null=True, blank=True, on_delete=models.SET_NULL, related_name='provided_encounters')
    
    # List of participants involved in the encounter (BackboneElement - handled via reverse FK)
    # Note: EncounterParticipant handles this
    
    # The appointment that scheduled this encounter (0..* Reference)
    appointment = models.ManyToManyField('components.Reference', blank=True, related_name='encounters_appointment')
    
    # The actual start date/time of the encounter (0..1 dateTime) 
    actualPeriod = models.ForeignKey('components.Period', null=True, blank=True, on_delete=models.SET_NULL, related_name='actual_encounters')
    
    # Another Encounter of which this encounter is a revision of (0..* Reference)
    plannedStartDate = models.DateTimeField(null=True, blank=True)
    
    # The planned end date/time (or discharge date) of the encounter (0..1 dateTime)
    plannedEndDate = models.DateTimeField(null=True, blank=True)
    
    # Quantity of time the encounter lasted (0..1 Duration)
    length = models.ForeignKey('components.Duration', null=True, blank=True, on_delete=models.SET_NULL, related_name='encounters')
    
	# The list of reason relevant to this encounter (BackboneElement - handled via reverse FK)
    # Note: EncounterReason handles this
    
    # The list of diagnosis relevant to this encounter (BackboneElement - handled via reverse FK)
    # Note: EncounterDiagnosis handles this
    
    # The set of accounts that may be used for billing for this Encounter (0..* Reference)
    account = models.ManyToManyField('components.Reference', blank=True, related_name='encounters_account')
    
    # Diet preferences reported by the patient (0..* CodeableConcept)
    dietPreference = models.ManyToManyField('components.CodeableConcept', blank=True, related_name='encounter_diet_preferences')
    
    # Wheelchair, translator, stretcher, etc. (0..* CodeableConcept)
    specialArrangement = models.ManyToManyField('components.CodeableConcept', blank=True, related_name='encounter_special_arrangements')
    
    # Special courtesies (VIP, board member) (0..* CodeableConcept)
    specialCourtesy = models.ManyToManyField('components.CodeableConcept', blank=True, related_name='encounter_special_courtesies')
    
    # The start and end time of the encounter (0..1 Period)
    period = models.ForeignKey('components.Period', null=True, blank=True, on_delete=models.SET_NULL, related_name='encounters')
    
    # Additional comments about the encounter (0..1 markdown)
    note = models.TextField(null=True, blank=True)
    
    # Discharge details including disposition (BackboneElement - handled via reverse FK)
    # Note: EncounterAdmission handles admission and discharge details
    
    # List of locations where the patient has been during this encounter (BackboneElement - handled via reverse FK)
    # Note: EncounterLocation handles this
    
    class Meta:
        db_table = 'encounter'
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['plannedStartDate']),
            models.Index(fields=['plannedEndDate']),
        ]
    
    def clean(self):
        super().clean()
        
        # FHIR invariants
        if self.plannedStartDate and self.plannedEndDate:
            if self.plannedStartDate > self.plannedEndDate:
                raise ValidationError("Encounter planned start date must be before or equal to planned end date")
        
        # Status validation
        if self.status in ['completed', 'discharged'] and not self.period:
            raise ValidationError("Completed or discharged encounters should have a period defined")
    
    def __str__(self):
        subject_display = self.subject.display if self.subject else "Unknown subject"
        return f"Encounter({self.status}) - {subject_display}"
