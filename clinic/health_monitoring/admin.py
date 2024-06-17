from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Role, Doctor, Symptom, Medication, DoctorVisit, PrescribedTreatment, Diagnosis
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role',)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Role)

class PatientInline(admin.TabularInline):
    model = Doctor.patients.through
    extra = 1

class DoctorAdmin(admin.ModelAdmin):
    inlines = (PatientInline,)

admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Symptom)
admin.site.register(Medication) 
admin.site.register(DoctorVisit)
admin.site.register(PrescribedTreatment)
admin.site.register(Diagnosis)  