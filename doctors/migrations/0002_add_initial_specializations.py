from django.db import migrations

def add_initial_specializations(apps, schema_editor):
    Specialization = apps.get_model('doctors', 'Specialization')
    specializations = [
        {'name': 'Cardiology', 'description': 'Deals with heart disorders'},
        {'name': 'Dermatology', 'description': 'Deals with skin disorders'},
        {'name': 'Neurology', 'description': 'Deals with nervous system disorders'},
        {'name': 'Pediatrics', 'description': 'Medical care of infants, children, and adolescents'},
        {'name': 'Orthopedics', 'description': 'Deals with musculoskeletal system'},
        {'name': 'Psychiatry', 'description': 'Deals with mental health disorders'},
        {'name': 'Ophthalmology', 'description': 'Deals with eye disorders'},
        {'name': 'ENT', 'description': 'Deals with ear, nose, and throat disorders'},
    ]
    for spec in specializations:
        Specialization.objects.create(**spec)

def remove_specializations(apps, schema_editor):
    Specialization = apps.get_model('doctors', 'Specialization')
    Specialization.objects.all().delete()

class Migration(migrations.Migration):
    dependencies = [
        ('doctors', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_initial_specializations, remove_specializations),
    ]