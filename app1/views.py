from django.shortcuts import render, redirect
from .models import Resident, Medicine, MedicineRequest, ChildVaccineHistory, DocumentRequest, Staff
from .forms import ResidentForm, MedicineForm, MedicineRequestForm, ChildVaccineHistoryForm, DocumentRequestForm, StaffForm
from django.contrib import messages
from datetime import date, timedelta
from django.db.models import Q
from docxtpl import DocxTemplate
import os
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def index(request):
    resident_count = Resident.objects.count()
    male_residents = Resident.objects.filter(gender='Male').count()
    female_residents = Resident.objects.filter(gender='Female').count()

    # Calculate the date 60 years ago from today
    sixty_years_ago = date.today() - timedelta(days=60*365.25)
    senior_residents = Resident.objects.filter(birth_date__lte=sixty_years_ago).count()

    # Calculate the date 18 years ago from today
    eighteen_years_ago = date.today() - timedelta(days=18*365.25)
    # Filter residents aged 18 to 59
    adult_residents = Resident.objects.filter(birth_date__gt=sixty_years_ago, birth_date__lte=eighteen_years_ago).count()
    
    # Filter residents less than 18 years old
    child_residents = Resident.objects.filter(birth_date__gt=eighteen_years_ago).count()

    solo_parents = Resident.objects.filter(status='Solo Parent').count()
    pwd = Resident.objects.filter(status='PWD').count()

    context = {
        'resident_count': resident_count,
        'male_residents': male_residents,
        'female_residents': female_residents,
        'child_residents': child_residents,
        'adult_residents': adult_residents,
        'senior_residents': senior_residents,
        'solo_parents': solo_parents,
        'pwd': pwd,
    }
    return render(request, 'app1/index.html', context)

def residents(request):
    q = request.GET.get('q')

    if q:
        residents = Resident.objects.filter(
            Q(first_name__icontains=q) |
            Q(middle_name__icontains=q) |
            Q(last_name__icontains=q) |
            Q(phone_number__icontains=q) |
            Q(purok__icontains=q) |
            Q(gender=q.title()) |
            Q(status__icontains=q)
        )
    else:
        residents = Resident.objects.all()

    # resident_count = Resident.objects.count()
    resident_count = residents.count()

    context = {
        'residents': residents, 
        'resident_count': resident_count,
    }
    return render(request, 'app1/residents.html', context)

def add_resident(request):
    form = ResidentForm()

    if request.method == 'POST':
        form = ResidentForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name'].lower()
            middle_name = form.cleaned_data['middle_name'].lower()
            last_name = form.cleaned_data['last_name'].lower()
            birth_date = form.cleaned_data['birth_date']

            if Resident.objects.filter(first_name=first_name, middle_name=middle_name, last_name=last_name).exists():
                messages.error(request, 'Resident already exists.')
            else:
                Resident.objects.create(
                    first_name=first_name,
                    middle_name=middle_name,
                    last_name=last_name,
                    birth_date=birth_date,
                    gender=form.cleaned_data['gender'], 
                    purok=form.cleaned_data['purok'], 
                    phone_number=form.cleaned_data['phone_number'],
                    status=form.cleaned_data['status']
                )
                messages.success(request, f'Resident {first_name.capitalize()} {last_name.capitalize()} has been added successfully.')
                return redirect('barangay-residents')

    context = {
        'form':form,
    }
    return render(request, 'app1/add-resident.html', context)

def update_resident(request, pk):
    resident = Resident.objects.get(id=pk)
    form = ResidentForm(instance=resident)

    if request.method == 'POST':
        form = ResidentForm(request.POST, instance=resident)
        if form.is_valid():
            first_name = form.cleaned_data['first_name'].lower()
            middle_name = form.cleaned_data['middle_name'].lower()
            last_name = form.cleaned_data['last_name'].lower()
            birth_date = form.cleaned_data['birth_date']

            # Check for duplicate resident
            if Resident.objects.filter(first_name=first_name, middle_name=middle_name, last_name=last_name, birth_date=birth_date).exclude(id=pk).exists():
                messages.error(request, 'Resident with the same name and birth date already exists.')
            else:
                form.save()
                messages.success(request, f'Resident {first_name.capitalize()} {last_name.capitalize()} has been updated successfully.')
                return redirect('barangay-residents')
    context = {
        'form':form,
    }
    return render(request, 'app1/update-resident.html', context)

def delete_resident(request, pk):
    resident = Resident.objects.get(id=pk)
    form = ResidentForm(instance=resident)

    first_name = resident.first_name
    last_name = resident.last_name

    if request.method == 'POST':
        resident.delete()
        messages.success(request, f'Resident {first_name.capitalize()} {last_name.capitalize()} has been deleted successfully.')
        return redirect('barangay-residents')
    
    context = {
        'form':form,
    }

    return render(request, 'app1/delete-resident.html', context)

def medicine_inventory(request):
    q = request.GET.get('q')

    if q:
        medicines = Medicine.objects.filter(
            Q(name__icontains=q) |
            Q(generic_name__icontains=q) |
            Q(dosage__icontains=q) |
            Q(type__icontains=q),
            Q(expiry_date__gt=date.today())
        )
    else:
        medicines = Medicine.objects.filter(expiry_date__gt=date.today())

    context = {
        'medicines': medicines,
    }
    return render(request, 'app1/medicine-inventory.html', context)

def add_medicine(request):
    form = MedicineForm()
    
    if request.method == 'POST':
        form = MedicineForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name'].lower()
            generic_name = form.cleaned_data['generic_name'].lower()
            dosage = form.cleaned_data['dosage']
            type = form.cleaned_data['type']
            expiry_date = form.cleaned_data['expiry_date']
            quantity = form.cleaned_data['quantity']

            if Medicine.objects.filter(name=name, generic_name=generic_name, expiry_date=expiry_date).exists():
                messages.error(request, 'Medicine already exists.')
            else:
                Medicine.objects.create(
                    name=name,
                    generic_name=generic_name,
                    dosage=dosage,
                    type=type,
                    expiry_date=expiry_date,
                    quantity=quantity
                )
                messages.success(request, f'Medicine {name.capitalize()} has been added successfully.')
                return redirect('barangay-medicine-inventory')

    context = {
        'form': form,
    }
    return render(request, 'app1/add-medicine.html', context)

def update_medicine(request, pk):
    medicine = Medicine.objects.get(id=pk)
    form = MedicineForm(instance=medicine)

    if request.method == 'POST':
        form = MedicineForm(request.POST, instance=medicine)
        if form.is_valid():
            name = form.cleaned_data['name'].lower()
            generic_name = form.cleaned_data['generic_name'].lower()
            dosage = form.cleaned_data['dosage']
            type = form.cleaned_data['type']
            expiry_date = form.cleaned_data['expiry_date']
            quantity = form.cleaned_data['quantity']

            if Medicine.objects.filter(name=name, generic_name=generic_name, expiry_date=expiry_date).exclude(id=pk).exists():
                messages.error(request, 'Medicine already exists.')
            else:
                form.save()
                messages.success(request, f'{name.capitalize()} has been updated successfully.')
                return redirect('barangay-medicine-inventory')

    context = {
        'form': form,
    }
    return render(request, 'app1/update-medicine.html', context)

def delete_medicine(request, pk):
    medicine = Medicine.objects.get(id=pk)
    form = MedicineForm(instance=medicine)

    name = medicine.name

    if request.method == 'POST':
        medicine.delete()
        messages.success(request, f'{name.capitalize()} has been deleted successfully.')
        return redirect('barangay-medicine-inventory')
    
    context = {
        'form':form,
    }

    return render(request, 'app1/delete-medicine.html', context)

def medicine_request(request):
    if request.method == 'POST':
        form = MedicineRequestForm(request.POST)
        if form.is_valid():
            medicine_request = form.save(commit=False)
            medicine = medicine_request.medicine
            requested_quantity = medicine_request.quantity

            if requested_quantity > medicine.quantity:
                messages.error(request, 'Requested quantity exceeds available stock.')
            else:
                medicine.quantity -= requested_quantity
                medicine.save()
                medicine_request.save()
                messages.success(request, 'Medicine request submitted successfully.')
                return redirect('barangay-medicine-request-history')
    else:
        form = MedicineRequestForm()

    context = {
        'form': form,
    }

    return render(request, 'app1/medicine-request.html', context)

def medicine_request_history(request):
    medicine_requests = MedicineRequest.objects.all()

    context = {
        'medicine_requests': medicine_requests,
    }
    return render(request, 'app1/medicine-request-history.html', context)

def children_list(request):
    # Calculate the date 18 years ago from today
    eighteen_years_ago = date.today() - timedelta(days=18*365.25)

    children = Resident.objects.filter(birth_date__gt=eighteen_years_ago)
    
    context = {
        'children': children,
    }
    
    return render(request, 'app1/children-list.html', context)

def update_visit(request, pk=None):
    resident = Resident.objects.get(id=pk)

    if request.method == 'POST':
        form = ChildVaccineHistoryForm(request.POST)
        if form.is_valid():
            vaccine_history = form.save(commit=False)
            vaccine_history.resident = resident
            vaccine_history.save()
            # messages.success(request, 'Vaccine history updated successfully.')
            return redirect('children-list')
    else:
        form = ChildVaccineHistoryForm()

    context = {
        'form': form,
        'resident': resident,
    }

    return render(request, 'app1/update-visit.html', context)

def visit_history(request, pk):
    resident = Resident.objects.get(id=pk)
    vaccine_history = ChildVaccineHistory.objects.filter(resident=pk)

    context = {
        'resident': resident,
        'vaccine_history': vaccine_history,
    }

    return render(request, 'app1/child-vaccine-history.html', context)
                

def document_request_history(request):
    document_requests = DocumentRequest.objects.all()

    context = {
        'document_requests': document_requests,
    }

    return render(request, 'app1/document-request-history.html', context)

def document_request(request):
    if request.method == 'POST':
        form = DocumentRequestForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['resident'].first_name
            middle_name = form.cleaned_data['resident'].middle_name
            last_name = form.cleaned_data['resident'].last_name
            purpose = form.cleaned_data['purpose']
            document_name = form.cleaned_data['document_name']
            gender = form.cleaned_data['resident'].gender
            purok = form.cleaned_data['resident'].purok

            # Save the form and get the saved instance
            document_request_instance = form.save()

            # Query the saved instance to get the request_date
            request_date = document_request_instance.request_date

            formatted_request_date = request_date.strftime("%B %d, %Y")

            file_name = f'{document_name}.docx'
            output_name = f'[{request_date}] {last_name.capitalize()}, {first_name.capitalize()} {middle_name.capitalize()}.docx'

            template_path = os.path.expanduser(f'~/Desktop/drafts/{file_name}')
            output_path = os.path.expanduser(f'~/Desktop/releasing/{document_name}/{output_name}')

            doc = DocxTemplate(template_path)

            context = { 
                'first_name' : first_name,
                'middle_name' : middle_name,
                'last_name' : last_name,
                'purpose' : purpose,
                'formatted_request_date' : formatted_request_date,
                'gender' : gender,
                'purok' : purok,
            }

            doc.render(context)
            doc.save(output_path)

            # form.save()
            messages.success(request, 'Document request submitted successfully.')
            return redirect('document-request-history')
    else:
        form = DocumentRequestForm()

    context = {
        'form': form,
    }

    return render(request, 'app1/document-request.html', context)

def staff(request):
    q = request.GET.get('q')

    if q:
        staff = Staff.objects.filter(
            Q(first_name__icontains=q) |
            Q(middle_name__icontains=q) |
            Q(last_name__icontains=q) |
            Q(phone_number__icontains=q) |
            Q(gender=q.title())
        )
    else:
        staff = Staff.objects.all()

    context = {
        'staff': staff, 
    }
    return render(request, 'app1/staff.html', context)

def add_staff(request):
    form = StaffForm()

    if request.method == 'POST':
        form = StaffForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name'].lower()
            middle_name = form.cleaned_data['middle_name'].lower()
            last_name = form.cleaned_data['last_name'].lower()
            birth_date = form.cleaned_data['birth_date']

            if Staff.objects.filter(first_name=first_name, middle_name=middle_name, last_name=last_name).exists():
                messages.error(request, 'Staff already exists.')
            else:
                Staff.objects.create(
                    first_name=first_name,
                    middle_name=middle_name,
                    last_name=last_name,
                    birth_date=birth_date,
                    gender=form.cleaned_data['gender'],
                    role=form.cleaned_data['role'],
                    phone_number=form.cleaned_data['phone_number']
                )
                messages.success(request, f'Staff {first_name.capitalize()} {last_name.capitalize()} has been added successfully.')
                return redirect('staff')

    context = {
        'form':form,
    }
    return render(request, 'app1/add-staff.html', context)

def update_staff(request, pk):
    staff = Staff.objects.get(id=pk)
    form = StaffForm(instance=staff)

    if request.method == 'POST':
        form = StaffForm(request.POST, instance=staff)
        if form.is_valid():
            first_name = form.cleaned_data['first_name'].lower()
            middle_name = form.cleaned_data['middle_name'].lower()
            last_name = form.cleaned_data['last_name'].lower()
            birth_date = form.cleaned_data['birth_date']

            # Check for duplicate staff
            if Staff.objects.filter(first_name=first_name, middle_name=middle_name, last_name=last_name, birth_date=birth_date).exclude(id=pk).exists():
                messages.error(request, 'Staff with the same name and birth date already exists.')
            else:
                form.save()
                messages.success(request, f'Staff {first_name.capitalize()} {last_name.capitalize()} has been updated successfully.')
                return redirect('staff')
    context = {
        'form':form,
    }
    return render(request, 'app1/update-staff.html', context)

def delete_staff(request, pk):
    staff = Staff.objects.get(id=pk)
    form = StaffForm(instance=staff)

    first_name = staff.first_name
    last_name = staff.last_name

    if request.method == 'POST':
        staff.delete()
        messages.success(request, f'Staff {first_name.capitalize()} {last_name.capitalize()} has been deleted successfully.')
        return redirect('staff')
    
    context = {
        'form':form,
    }

    return render(request, 'app1/delete-staff.html', context)

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # if username == 'admin' and password == 'admin':
        #     return redirect('barangay-home')
        # else:
        #     messages.error(request, 'Invalid credentials')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, 'Invalid credentials')
            # return redirect('login')
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('barangay-home')

    return render(request, 'app1/login.html')

def logout_page(request):
    logout(request)
    return redirect('login')