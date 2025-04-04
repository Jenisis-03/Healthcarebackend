from django.db import models
from django.conf import settings
from doctors.models import Doctor

class Patient(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='patient_profile')
    blood_group = models.CharField(max_length=5)
    allergies = models.TextField(blank=True)
    medical_conditions = models.TextField(blank=True)
    emergency_contact_name = models.CharField(max_length=100)
    emergency_contact_number = models.CharField(max_length=15)
    assigned_doctors = models.ManyToManyField(Doctor, through='PatientDoctorMapping', related_name='assigned_patients')

    class Meta:
        db_table = 'patients'

    def __str__(self):
        return f"{self.user.get_full_name()} - Patient"

class PatientDoctorMapping(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='doctor_mappings')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='patient_mappings')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'patient_doctor_mappings'
        unique_together = ('patient', 'doctor')

    def __str__(self):
        return f"{self.patient} - {self.doctor}"

class Appointment(models.Model):
    STATUS_CHOICES = (
        ('SCHEDULED', 'Scheduled'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    )

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='SCHEDULED')
    reason = models.TextField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'appointments'
        ordering = ['-appointment_date', '-appointment_time']

    def __str__(self):
        return f"{self.patient} - {self.doctor} - {self.appointment_date}"

class MedicalRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medical_records')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='medical_records')
    diagnosis = models.TextField()
    prescription = models.TextField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'medical_records'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.patient} - {self.created_at.date()}"
