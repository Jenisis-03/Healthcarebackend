from django.db import models
from django.conf import settings

class Specialization(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    class Meta:
        db_table = 'specializations'

    def __str__(self):
        return self.name

class Doctor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='doctor_profile')
    specialization = models.ForeignKey(Specialization, on_delete=models.PROTECT)
    license_number = models.CharField(max_length=50, unique=True)
    experience_years = models.PositiveIntegerField()
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2)
    available_days = models.CharField(max_length=100)  # Stored as comma-separated days
    available_time_start = models.TimeField()
    available_time_end = models.TimeField()

    class Meta:
        db_table = 'doctors'

    def __str__(self):
        return f"Dr. {self.user.get_full_name()} - {self.specialization}"
