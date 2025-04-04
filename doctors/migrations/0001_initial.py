# Generated by Django 4.2.7 on 2025-04-04 07:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Specialization",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("description", models.TextField(blank=True)),
            ],
            options={
                "db_table": "specializations",
            },
        ),
        migrations.CreateModel(
            name="Doctor",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("license_number", models.CharField(max_length=50, unique=True)),
                ("experience_years", models.PositiveIntegerField()),
                (
                    "consultation_fee",
                    models.DecimalField(decimal_places=2, max_digits=10),
                ),
                ("available_days", models.CharField(max_length=100)),
                ("available_time_start", models.TimeField()),
                ("available_time_end", models.TimeField()),
                (
                    "specialization",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="doctors.specialization",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="doctor_profile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "doctors",
            },
        ),
    ]
