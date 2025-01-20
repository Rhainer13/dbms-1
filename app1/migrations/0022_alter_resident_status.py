# Generated by Django 5.1.4 on 2025-01-20 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0021_resident_status_alter_documentrequest_document_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resident',
            name='status',
            field=models.CharField(choices=[('None', 'None'), ('Employed', 'Employed'), ('Unemployed', 'Unemployed'), ('PWD', 'PWD'), ('OFW', 'OFW'), ('Solo Parent', 'Solo Parent'), ('Out of School Youth', 'Out of School Youth'), ('Out of School Children', 'Out of School Children'), ('Indigenous Person', 'Indigenous Person')], max_length=50),
        ),
    ]
