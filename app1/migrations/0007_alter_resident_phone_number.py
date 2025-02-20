# Generated by Django 5.1.4 on 2024-12-20 12:59

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0006_alter_resident_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resident',
            name='phone_number',
            field=models.CharField(max_length=11, validators=[django.core.validators.RegexValidator(message='Phone number must be exactly 11 digits.', regex='^\\d{11}$')]),
        ),
    ]
