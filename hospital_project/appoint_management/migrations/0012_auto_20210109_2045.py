# Generated by Django 3.1.5 on 2021-01-09 15:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appoint_management', '0011_auto_20210109_2037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='doctor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointment_doctor', to='appoint_management.doctors'),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointment_patient', to='appoint_management.patients'),
        ),
        migrations.AlterField(
            model_name='doctors',
            name='specialist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doctors_specialist', to='appoint_management.specialfields'),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='doctor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schedule_doctor', to='appoint_management.doctors'),
        ),
    ]
