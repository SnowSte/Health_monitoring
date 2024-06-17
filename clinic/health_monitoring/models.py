from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class Role(models.Model):
    key = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.key

class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=255, default='')
    passport_data = models.CharField(max_length=14, default='')
    phone = models.CharField(max_length=20, default='')
    email = models.EmailField(max_length=255)
    address = models.CharField(max_length=255, default='')
    other_info = models.TextField(default='')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.username
    
class Doctor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    patients = models.ManyToManyField(CustomUser, related_name='doctor_patients', blank=True, limit_choices_to={'role__key': 'patient'})

    def __str__(self):
        return self.user.username
#Диагноз   
class Diagnosis(models.Model):
    patient = models.OneToOneField(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role__key': 'patient'})
    diagnosis_text = models.TextField()

    def __str__(self):
        return f"Diagnosis for {self.patient.full_name}"
    
class Symptom(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Medication(models.Model):
    name = models.CharField(max_length=100)
    symptoms = models.ManyToManyField(Symptom, related_name='medications', blank=True)

    def __str__(self):
        return self.name
    
class DoctorVisit(models.Model):
    patient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role__key': 'patient'})
    complaints = models.TextField()
    temperature = models.DecimalField(max_digits=4, decimal_places=1)
    blood_pressure = models.CharField(max_length=7)
    pulse = models.PositiveIntegerField()
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    visit_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Visit by {self.patient.username}'
    
class PrescribedTreatment(models.Model): #Лечение
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role__key': 'patient'})
    doctor_visit = models.ForeignKey(DoctorVisit, on_delete=models.CASCADE)
    medications = models.ManyToManyField(Medication, related_name='prescribed_treatments')
    diagnosis = models.TextField()  # Вывод по жалобе
    date_prescribed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Treatment prescribed by Dr. {self.doctor.user.full_name} for {self.patient.full_name} on {self.date_prescribed}'