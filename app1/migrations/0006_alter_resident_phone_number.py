# Generated by Django 5.1.4 on 2024-12-20 12:55

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0005_alter_resident_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resident',
            name='phone_number',
            field=models.CharField(blank=True, max_length=11, validators=[django.core.validators.RegexValidator(message='Phone number must be exactly 11 digits.', regex='^\\d{11}$')]),
        ),
    ]
