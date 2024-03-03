# Generated by Django 5.0.2 on 2024-03-03 01:04

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0005_alter_futureplan_remarks_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='Course',
        ),
        migrations.RemoveField(
            model_name='student',
            name='RegistrationNo',
        ),
        migrations.AddField(
            model_name='student',
            name='DateOfBirth',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
