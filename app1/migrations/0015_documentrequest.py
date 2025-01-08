# Generated by Django 5.1.4 on 2025-01-03 06:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0014_alter_childvaccinehistory_vaccine_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_date', models.DateField(auto_now_add=True)),
                ('document_name', models.TextField(max_length=100)),
                ('purpose', models.TextField(max_length=100)),
                ('resident', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.resident')),
            ],
            options={
                'ordering': ['resident'],
            },
        ),
    ]
