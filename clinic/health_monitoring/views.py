from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login
from .forms import CustomUserCreationForm, LoginForm, CustomForm, DoctorVisitForm, PrescribedTreatmentForm, DiagnosisForm
from .models import CustomUser, Doctor, Medication, DoctorVisit, PrescribedTreatment, Diagnosis
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import JsonResponse
from django.contrib import messages
from django.utils import timezone


def index(request):
    return render(request, 'health_monitoring/index.html')

def about(request):
    return render(request, 'health_monitoring/about.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  
    else:
        form = CustomUserCreationForm()
    return render(request, 'health_monitoring/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return render(request, 'health_monitoring/home.html')
            else:
                messages.error(request, 'Вы ввели неверный логин или пароль')
        else:
            messages.error(request, 'Вы ввели неверный логин или пароль')
    else:
        form = LoginForm()
    return render(request, 'health_monitoring/login.html', {'form': form})

def user_logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')  
    return render(request, 'health_monitoring/logout.html')
#Профиль пользователя
@login_required
def profile(request):
    user = request.user
    diagnosis, created = Diagnosis.objects.get_or_create(patient=user) if user.role.key == 'patient' else (None, None)
    
    if request.method == 'POST':
        diagnosis_form = DiagnosisForm(request.POST)
        if diagnosis_form.is_valid():
            diagnosis.diagnosis_text = diagnosis_form.cleaned_data['diagnosis']
            diagnosis.save()
            return redirect('profile')
    else:
        diagnosis_form = DiagnosisForm(initial={'diagnosis': diagnosis.diagnosis_text}) if diagnosis else None

    return render(request, 'health_monitoring/profile.html', {
        'user': user,
        'diagnosis_form': diagnosis_form,
        'current_diagnosis': diagnosis.diagnosis_text if diagnosis else None
    })

def home(request):
    return render(request, 'health_monitoring/home.html')

def all_patients(request):
    if request.user.is_authenticated:
        user = request.user
        if user.role.key == 'doctor':
            doctor = Doctor.objects.get(user=user)
            patients = doctor.patients.all()
            return render(request, 'health_monitoring/all_patients.html', {'patients': patients})
    return render(request, 'health_monitoring/all_patients.html', {'patients': []})

def all_doctors(request):
    current_user = request.user
    
    # Получаем его доктора, если он пациент
    if current_user.role.key == 'patient':
        patient_doctors = Doctor.objects.filter(patients=current_user)
        return render(request, 'health_monitoring/all_doctors.html', {'patient_doctors': patient_doctors})
    else:
        return render(request, 'error.html', {'message': 'Вы не пациент!'})
    
    
def medications_page(request):
    medications = Medication.objects.all()
    return render(request, 'health_monitoring/medications_page.html', {'medications': medications})
    
def create_custom_form(request):
    if request.method == 'POST':
        # Обработка отправки формы
        pass
    else:
        form = CustomForm()
    return render(request, 'health_monitoring/about.html', {'form': form})

def get_symptoms(request, medication_id):
    medication = Medication.objects.get(id=medication_id)
    symptoms = medication.symptom_set.all()
    data = [{'id': symptom.id, 'name': symptom.name} for symptom in symptoms]
    return JsonResponse(data, safe=False)

login_required
def create_doctor_visit(request):
    visit_date = timezone.now()  
    
    if request.method == 'POST':
        form = DoctorVisitForm(request.POST)
        if form.is_valid():
            doctor_visit = form.save(commit=False)
            doctor_visit.patient = request.user
            doctor_visit.visit_date = visit_date
            doctor_visit.save()
            messages.success(request, 'Ваше обращение создано.')
            form = DoctorVisitForm()
    else:
        form = DoctorVisitForm()
    
    return render(request, 'health_monitoring/create_doctor_visit.html', {'form': form, 'visit_date': visit_date})

@login_required
def doctor_visits(request):
    # Получаем текущего пользователя
    user = request.user
    if user.role.key == 'doctor':
        doctor = user.doctor
        # Получаем обращения только для пациентов данного врача
        doctor_visits = DoctorVisit.objects.filter(patient__in=doctor.patients.all())
        return render(request, 'health_monitoring/doctor_visits.html', {'doctor_visits': doctor_visits})
    # Если текущий пользователь не является врачом, возвращаем ошибку
    return render(request, 'error.html', {'message': 'Вы не врач!'})

@login_required
def create_prescribed_treatment(request):
    if request.method == 'POST':
        form = PrescribedTreatmentForm(request.POST)
        if form.is_valid():
            prescribed_treatment = form.save(commit=False)
            prescribed_treatment.doctor = request.user.doctor
            prescribed_treatment.patient = form.cleaned_data['doctor_visit'].patient
            prescribed_treatment.save()
            form.save_m2m()
            return redirect('prescribed_treatment_detail', pk=prescribed_treatment.pk)
    else:
        form = PrescribedTreatmentForm()
    return render(request, 'health_monitoring/create_prescribed_treatment.html', {'form': form})
#назначение врача
@login_required
def prescribed_treatment_detail(request, pk):
    prescribed_treatment = get_object_or_404(PrescribedTreatment, pk=pk)
    return render(request, 'health_monitoring/prescribed_treatment_detail.html', {'prescribed_treatment': prescribed_treatment})

@login_required
def prescribed_treatment_list(request):
    if request.user.role.key == 'doctor':
        treatments = PrescribedTreatment.objects.filter(doctor=request.user.doctor)
    else:
        treatments = PrescribedTreatment.objects.filter(patient=request.user)
    return render(request, 'health_monitoring/prescribed_treatment_list.html', {'treatments': treatments})
#Для просмотра назначенных лечений
def doctor_prescribed_treatments(request):
    if request.user.role.key == 'doctor':
        treatments = PrescribedTreatment.objects.filter(doctor=request.user.doctor)
        return render(request, 'health_monitoring/doctor_prescribed_treatments.html', {'treatments': treatments})
    else:
        return render(request, 'error.html', {'message': 'Вы не врач!'})
    
@login_required
def remove_prescribed_treatment(request, pk):
    if request.method == 'POST':
        # Получаем назначенное лечение по его primary key (pk)
        prescribed_treatment = get_object_or_404(PrescribedTreatment, pk=pk)
        # Проверяем, является ли текущий пользователь врачем, который создал это назначение
        if prescribed_treatment.doctor == request.user.doctor:
            prescribed_treatment.delete()
            return redirect('doctor_prescribed_treatments')
    return redirect('doctor_prescribed_treatments')
#Для пациента
@login_required
def patient_prescribed_treatments(request):
    treatments = PrescribedTreatment.objects.filter(doctor_visit__patient=request.user)

    return render(request, 'health_monitoring/patient_prescribed_treatments.html', {'treatments': treatments})