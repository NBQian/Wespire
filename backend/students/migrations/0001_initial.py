# Generated by Django 5.0.2 on 2024-02-14 04:47

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='FuturePlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_code', models.CharField(max_length=255)),
                ('Type', models.CharField(max_length=100)),
                ('CurrentSumAssured', models.DecimalField(decimal_places=2, max_digits=10)),
                ('RecommendedSumAssured', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Shortfall', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Remarks', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_code', models.CharField(max_length=255)),
                ('Company', models.CharField(max_length=100)),
                ('ProductNumber', models.CharField(max_length=100)),
                ('ProductName', models.CharField(max_length=100)),
                ('Date', models.DateField()),
                ('Type', models.CharField(max_length=100)),
                ('WholeLife', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Endowment', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Term', models.DecimalField(decimal_places=2, max_digits=10)),
                ('InvLinked', models.DecimalField(decimal_places=2, max_digits=10)),
                ('TotalDeathCoverage', models.DecimalField(decimal_places=2, max_digits=10)),
                ('TotalPermanentDisability', models.DecimalField(decimal_places=2, max_digits=10)),
                ('EarlyCriticalIllness', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Accidental', models.DecimalField(decimal_places=2, max_digits=10)),
                ('OtherBenefitsRemarks', models.TextField()),
                ('Mode', models.CharField(max_length=100)),
                ('Monthly', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Quarterly', models.DecimalField(decimal_places=2, max_digits=10)),
                ('SemiAnnual', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Yearly', models.DecimalField(decimal_places=2, max_digits=10)),
                ('MaturityPremiumEndDate', models.CharField(max_length=100)),
                ('CurrentValue', models.DecimalField(decimal_places=2, max_digits=10)),
                ('TotalPremiumsPaid', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='UserAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('studentId', models.AutoField(primary_key=True, serialize=False)),
                ('FirstName', models.CharField(max_length=100)),
                ('LastName', models.CharField(max_length=100)),
                ('RegistrationNo', models.CharField(max_length=100)),
                ('Email', models.CharField(max_length=100)),
                ('Course', models.CharField(max_length=100)),
                ('PhoneNumber', models.CharField(blank=True, max_length=15, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='students', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StudentSummary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_code', models.CharField(blank=True, max_length=255, null=True)),
                ('date_created', models.DateTimeField(default=datetime.datetime.now)),
                ('pdf_file', models.FileField(blank=True, null=True, upload_to='client_summaries/')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='summaries', to='students.student')),
            ],
        ),
    ]
