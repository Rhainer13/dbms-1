# Generated by Django 5.1.4 on 2025-01-21 21:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0022_alter_resident_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='childvaccinehistory',
            name='vaccine_name',
            field=models.TextField(choices=[('BCG Vaccine', 'BCG Vaccine'), ('Hepatitis B Vaccine', 'Hepatitis B Vaccine'), ('Pentavalent Vaccine (DPT -Hep B-HIB)', 'HepatitisPentavalent Vaccine (DPT -Hep B-HIB)'), ('Oral Polio Vaccine', 'Oral Polio Vaccine'), ('Inactivated Polio Vaccine (IPV)', 'Inactivated Polio Vaccine (IPV)'), ('Pneumococcal Conjugate Vaccine (PCV)', 'Pneumococcal Conjugate Vaccine (PCV)'), ('Measles, Mumps, Rubella Vaccine (MMR)', 'Measles, Mumps, Rubella Vaccine (MMR)')], max_length=100),
        ),
        migrations.AlterField(
            model_name='documentrequest',
            name='document_name',
            field=models.TextField(choices=[('BAILBOND', 'BAILBOND'), ('CP GIFTS', 'CP GIFTS'), ('EMPLOYMENT', 'EMPLOYMENT'), ('GOOD MORAL', 'GOOD MORAL'), ('INDIGENCY FINANCIAL', 'INDIGENCY FINANCIAL'), ('INDIGENCY MEDICAL', 'INDIGENCY MEDICAL'), ('LOAN', 'LOAN'), ('NO INCOME', 'NO INCOME'), ('OJT', 'OJT'), ('PAO', 'PAO'), ('POLICE CLEARANCE', 'POLICE CLEARANCE'), ('PROBATION', 'PROBATION'), ('RESIDENCY', 'RESIDENCY'), ('RICE ASSISTANCE', 'RICE ASSISTANCE'), ('SPES', 'SPES')], max_length=50),
        ),
        migrations.AlterField(
            model_name='medicinerequest',
            name='medicine',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app1.medicine'),
        ),
        migrations.AlterField(
            model_name='medicinerequest',
            name='resident',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app1.resident'),
        ),
    ]
