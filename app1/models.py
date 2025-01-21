from django.db import models
from django.core.validators import RegexValidator

# Create your models here.
class Resident(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]

    PUROK_CHOICES = [
        ('Saging', 'Saging'),
        ('Manga', 'Manga'),
        ('Cassava', 'Cassava'),
        ('Camote', 'Camote'),
        ('Bayabas', 'Bayabas'),
        ('Ampalaya', 'Ampalaya'),
        ('Kapayas', 'Kapayas'),
        ('Talong', 'Talong'),
        ('Sili', 'Sili'),
        ('Batong', 'Batong'),
        ('Agbate', 'Agbate'),
        ('Gabi', 'Gabi'),
    ]

    STATUS_CHOICES = [
        ('None', 'None'),
        ('Employed', 'Employed'),
        ('Unemployed', 'Unemployed'),
        ('PWD', 'PWD'),
        ('OFW', 'OFW'),
        ('Solo Parent', 'Solo Parent'),
        ('Out of School Youth', 'Out of School Youth'),
        ('Out of School Children', 'Out of School Children'),
        ('Indigenous Person', 'Indigenous Person'),
    ]
    
    phone_number_validator = RegexValidator(
        regex=r'^\d{11}$',
        message='Phone number must be exactly 11 digits.'
    )

    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50)
    birth_date = models.DateField() 
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, blank=False)
    purok = models.CharField(max_length=20, choices=PUROK_CHOICES, blank=False)
    phone_number = models.CharField(max_length=11, validators=[phone_number_validator])
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, blank=False)
    
    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f'{self.last_name.capitalize()}, {self.first_name.capitalize()} {self.middle_name.capitalize()}'
    
class Staff(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]

    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Health Worker', 'Health Worker'),
        ('Front Desk', 'Front Desk'),
    ]
    
    phone_number_validator = RegexValidator(
        regex=r'^\d{11}$',
        message='Phone number must be exactly 11 digits.'
    )

    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50)
    birth_date = models.DateField() 
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, blank=False)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, blank=False)
    phone_number = models.CharField(max_length=11, validators=[phone_number_validator])
    
    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f'{self.last_name.capitalize()}, {self.first_name.capitalize()} {self.middle_name.capitalize()}'

class Medicine(models.Model):
    name = models.CharField(max_length=50)
    generic_name = models.CharField(blank=True)
    dosage = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    date_added = models.DateField(auto_now_add=True)
    expiry_date = models.DateField()
    quantity = models.PositiveIntegerField()
    
    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.generic_name} ({self.quantity})'
    
class MedicineRequest(models.Model):
    resident = models.ForeignKey(Resident, on_delete=models.SET_NULL, null=True)
    medicine = models.ForeignKey(Medicine, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField()
    request_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.resident} requests {self.quantity} of {self.medicine}'

class ChildVaccineHistory(models.Model):
    VACCINE_CHOICES = [
        ('BCG Vaccine', 'BCG Vaccine'),
        ('Hepatitis B Vaccine', 'Hepatitis B Vaccine'),
        ('Pentavalent Vaccine (DPT -Hep B-HIB)', 'HepatitisPentavalent Vaccine (DPT -Hep B-HIB)'),
        ('Oral Polio Vaccine', 'Oral Polio Vaccine'),
        ('Inactivated Polio Vaccine (IPV)', 'Inactivated Polio Vaccine (IPV)'),
        ('Pneumococcal Conjugate Vaccine (PCV)', 'Pneumococcal Conjugate Vaccine (PCV)'),
        ('Measles, Mumps, Rubella Vaccine (MMR)', 'Measles, Mumps, Rubella Vaccine (MMR)'),
    ]

    resident = models.ForeignKey(Resident, on_delete=models.CASCADE)
    visit_number = models.PositiveIntegerField()
    vaccine_name = models.TextField(max_length=100, choices=VACCINE_CHOICES)
    health_worker = models.ForeignKey(Staff, null=True, on_delete=models.SET_NULL)
    date_given = models.DateField(auto_now_add=True)
    
    class Meta:
        ordering = ['resident']

    def __str__(self):
        return f'{self.resident} has been given {self.vaccine_name} on {self.date_given}'
    
class DocumentRequest(models.Model):
    DOCUMENT_CHOICES = [
        ('BAILBOND', 'BAILBOND'),
        ('CP GIFTS', 'CP GIFTS'),
        ('EMPLOYMENT', 'EMPLOYMENT'),
        ('GOOD MORAL', 'GOOD MORAL'),
        ('INDIGENCY FINANCIAL', 'INDIGENCY FINANCIAL'),
        ('INDIGENCY MEDICAL', 'INDIGENCY MEDICAL'),
        ('LOAN', 'LOAN'),
        ('NO INCOME', 'NO INCOME'),
        ('OJT', 'OJT'),
        ('PAO', 'PAO'),
        ('POLICE CLEARANCE', 'POLICE CLEARANCE'),
        ('PROBATION', 'PROBATION'),
        ('RESIDENCY', 'RESIDENCY'),
        ('RICE ASSISTANCE', 'RICE ASSISTANCE'),
        ('SPES', 'SPES'),
    ]

    PURPOSE_CHOICES = [
        ('Employment', 'Employment'),
        ('Government', 'Government'),
        ('Identification', 'Identification'),
        ('Personal', 'Personal'),
        ('School', 'School'),
    ]

    request_date = models.DateField(auto_now_add=True)
    resident = models.ForeignKey(Resident, on_delete=models.CASCADE)
    document_name = models.TextField(max_length=50, choices=DOCUMENT_CHOICES, blank=False)
    purpose = models.TextField(max_length=100, choices=PURPOSE_CHOICES, blank=True)
    
    class Meta:
        ordering = ['-request_date']

    def __str__(self):
        return f'{self.resident} requested for {self.document_name} on {self.request_date}'