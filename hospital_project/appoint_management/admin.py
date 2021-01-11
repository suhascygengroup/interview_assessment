from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(SpecialFields)
admin.site.register(Doctors)
admin.site.register(Schedule)
admin.site.register(Appointment)
admin.site.register(Patients)
