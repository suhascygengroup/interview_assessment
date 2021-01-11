from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import *

router =DefaultRouter()
router.register('doctor', DoctorViewSet)
router.register('patient', PatientViewSet)
router.register('appointment', AppointmentViewSet)
urlpatterns = [
    path('', include(router.urls)),
]