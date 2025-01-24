from django.contrib import admin
from .models import Resident, Staff, Medicine, DocumentRequest

# Register your models here.
admin.site.register(Resident)
admin.site.register(Staff)
admin.site.register(Medicine)
admin.site.register(DocumentRequest)