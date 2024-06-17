from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Medication, Symptom, DoctorVisit, PrescribedTreatment

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['full_name', 'username', 'email', 'passport_data', 'phone', 'address', 'other_info', 'role']
        labels = {
            'full_name': 'Полное имя',
            'username': 'Имя прльзователя',
            'email': 'Электронная почта',
            'passport_data': 'Паспортные данные',
            'phone': 'Контактный телефон',
            'address': 'Адрес проживания',
            'other_info': 'Прочая информация',
            'role': 'Роль'
        }

class LoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password')

class CustomForm(forms.Form):
    medication = forms.ModelChoiceField(queryset=Medication.objects.all(), empty_label=None, label='Выберите препарат')
    symptom = forms.ModelMultipleChoiceField(queryset=Symptom.objects.none(), widget=forms.CheckboxSelectMultiple, label='Выберите симптомы')

#Профиль
class DiagnosisForm(forms.Form):
    diagnosis = forms.CharField(widget=forms.Textarea, label='Диагноз')

class DoctorVisitForm(forms.ModelForm):
    class Meta:
        model = DoctorVisit
        fields = ['complaints', 'temperature', 'blood_pressure', 'pulse', 'weight']
        labels = {
            'complaints': 'Жалобы',
            'temperature': 'Температура',
            'blood_pressure': 'Давление',
            'pulse': 'Пульс',
            'weight': 'Вес'
        }
        widgets = {
            'complaints': forms.Textarea(attrs={'class': 'form-control'}),
            'temperature': forms.NumberInput(attrs={'class': 'form-control'}),
            'blood_pressure': forms.TextInput(attrs={'class': 'form-control'}),
            'pulse': forms.NumberInput(attrs={'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     # Установка даты визита для каждого варианта выбора
    #     for choice in self.fields['doctor_visit'].widget.choices:
    #         if choice[0]:
    #             doctor_visit = DoctorVisit.objects.get(pk=choice[0])
    #             visit_date = doctor_visit.visit_date.strftime('%Y-%m-%d %H:%M:%S')
    #             self.fields['doctor_visit'].widget.attrs['data-visit-date'] = visit_date

                
class PrescribedTreatmentForm(forms.ModelForm):
    class Meta:
        model = PrescribedTreatment
        fields = ['doctor_visit', 'medications', 'diagnosis']
        labels = {
            'doctor_visit': 'Визит к врачу',
            'medications': 'Медикаменты',
            'diagnosis': 'Вывод по жалобе'
        }
        widgets = {
            'doctor_visit': forms.Select(attrs={'class': 'form-control'}),
            'medications': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
            'diagnosis': forms.Textarea(attrs={'class': 'form-control'}),
        }