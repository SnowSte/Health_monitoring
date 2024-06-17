from django.urls import path
from . import views
from django.urls import include
from .views import create_prescribed_treatment, prescribed_treatment_detail, prescribed_treatment_list
urlpatterns = [
    # path('', views.index, name='index'),
    path('about/', views.about, name='about'),
     path('accounts/login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'), #профиль
    path('', views.profile, name='profile'),
    path('home/', views.home, name='home'),
    path('all_patients/', views.all_patients, name='all_patients'),
    path('all_doctors/', views.all_doctors, name='all_doctors'),  
    # path('remove_patient/', views.remove_patient, name='remove_patient'),
    # path('remove_patient/<int:doctor_id>/', views.remove_patient, name='remove_patient'),
    path('create-form/', views.create_custom_form, name='create_custom_form'),
    path('medications/', views.medications_page, name='medications_page'),
    path('create_doctor_visit/', views.create_doctor_visit, name='create_doctor_visit'),
    path('doctor_visits/', views.doctor_visits, name='doctor_visits'),
    path('prescribed_treatments/new/', create_prescribed_treatment, name='create_prescribed_treatment'),
    path('prescribed_treatments/<int:pk>/', prescribed_treatment_detail, name='prescribed_treatment_detail'),
    path('prescribed_treatments/', prescribed_treatment_list, name='prescribed_treatment_list'),
    path('my_prescribed_treatments/', views.patient_prescribed_treatments, name='patient_prescribed_treatments'), 
     path('remove_prescribed_treatment/<int:pk>/', views.remove_prescribed_treatment, name='remove_prescribed_treatment'),
     path('doctor_prescribed_treatments/', views.doctor_prescribed_treatments, name='doctor_prescribed_treatments'),
    # другие URL-пути
]

