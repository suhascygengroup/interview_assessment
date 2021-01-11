from django.shortcuts import render
from .serializers import *
from rest_framework.viewsets import ModelViewSet
from .models import *
from rest_framework.decorators import action

# Create your views here.
class DoctorViewSet(ModelViewSet):
	serializer_class = DoctorsSerializer
	queryset = Doctors.objects.all().order_by('-id')

class PatientViewSet(ModelViewSet):
	serializer_class = PatientSerializer
	queryset = Patients.objects.all().order_by('-id')

class AppointmentViewSet(ModelViewSet):
	serializer_class = AppointmentSerializer
	queryset = Appointment.objects.all().order_by('-id')
