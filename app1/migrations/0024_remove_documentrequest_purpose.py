# Generated by Django 5.1.4 on 2025-01-21 21:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0023_alter_childvaccinehistory_vaccine_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='documentrequest',
            name='purpose',
        ),
    ]
