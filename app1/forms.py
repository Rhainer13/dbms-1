from django.forms import ModelForm
from .models import Resident, Medicine, MedicineRequest, ChildVaccineHistory, DocumentRequest, Staff
from django import forms
from datetime import date, datetime


class ResidentForm(ModelForm):
    class Meta:
        model = Resident
        fields = '__all__'
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-field', 'min': '1900-01-01'}),
        }

    def __init__(self, *args, **kwargs):
        super(ResidentForm, self).__init__(*args, **kwargs)
        self.fields['phone_number'].initial = '09'
        current_year = datetime.now().year
        self.fields['birth_date'].widget.attrs['max'] = f'{current_year}-12-31'

class StaffForm(ModelForm):
    class Meta:
        model = Staff
        fields = '__all__'
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-field', 'min': '1900-01-01'}),
        }

    def __init__(self, *args, **kwargs):
        super(StaffForm, self).__init__(*args, **kwargs)
        self.fields['phone_number'].initial = '09'
        current_year = datetime.now().year
        self.fields['birth_date'].widget.attrs['max'] = f'{current_year}-12-31'


class MedicineForm(ModelForm):
    class Meta:
        model = Medicine
        fields = '__all__'
        widgets = {
            'expiry_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-field'}),
        }

    def clean_expiry_date(self):
        expiry_date = self.cleaned_data.get('expiry_date')
        if expiry_date and expiry_date < date.today():
            raise forms.ValidationError("Expiry date cannot be in the past.")
        return expiry_date
    
# class MedicineRequestForm(forms.ModelForm):
#     class Meta:
#         model = MedicineRequest
#         fields = ['resident', 'medicine', 'quantity']
#         widgets = {
#             'resident': forms.Select(attrs={'id': 'id_resident'}),
#             'medicine': forms.Select(attrs={'id': 'id_medicine'}),
#         }

class MedicineRequestForm(forms.ModelForm):
    class Meta:
        model = MedicineRequest
        fields = ['resident', 'medicine', 'quantity']
        widgets = {
            'medicine': forms.Select(attrs={'class': 'form-field'}),
        }

    def __init__(self, *args, **kwargs):
        super(MedicineRequestForm, self).__init__(*args, **kwargs)
        self.fields['medicine'].queryset = Medicine.objects.filter(expiry_date__gte=date.today())

class ChildVaccineHistoryForm(forms.ModelForm):
    class Meta:
        model = ChildVaccineHistory
        exclude = ['resident']
        widgets = {
            'date_given': forms.DateInput(attrs={'type': 'date', 'class': 'form-field'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter health_worker to only include staff with the role "Health Worker"
        self.fields['health_worker'].queryset = Staff.objects.filter(role='Health Worker')

class DocumentRequestForm(forms.ModelForm):
    class Meta:
        model = DocumentRequest
        fields = '__all__'
        widgets = {
            'request_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-field'}),
        }