# Generated by Django 5.1.4 on 2025-01-04 09:38

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0017_alter_documentrequest_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('middle_name', models.CharField(blank=True, max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('birth_date', models.DateField()),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=6)),
                ('role', models.CharField(choices=[('Admin', 'Admin'), ('Health Worker', 'Health Worker'), ('Front Desk', 'Front Desk')], max_length=20)),
                ('phone_number', models.CharField(max_length=11, validators=[django.core.validators.RegexValidator(message='Phone number must be exactly 11 digits.', regex='^\\d{11}$')])),
            ],
            options={
                'ordering': ['last_name', 'first_name'],
            },
        ),
    ]
