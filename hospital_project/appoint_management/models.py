from django.db import models
SHIFT_SLOTS=(

    ('M','Morning'),	#8 to 5
    ('A','Afternoon'),		#2 to 11	
    ('E','Evening'),		#5 to 2
    ('N','Night')		#12 to 9 
)

DAYS=(
	('Mon','Monday'),
	('Tue','Tuesday'),
	('Wed','Wednesday'),
	('Thu','Thursday'),
	('Fri','Friday'),
	('Sat','Saturday'),
	('Sun','Sunday'),
)
# Create your models here.
class SpecialFields(models.Model):
	specialist_in = models.CharField(max_length=255,null=True,blank=True)
	is_delete = models.BooleanField(default=False)
	def __str__(self):
		return self.specialist_in

class Doctors(models.Model):
	full_name = models.CharField(max_length=255,null=True,blank=True)
	mobile = models.CharField(max_length=17,null=True,blank=True)
	age = models.IntegerField()
	address = models.TextField(default='')
	specialist = models.ForeignKey(SpecialFields, on_delete=models.CASCADE,related_name='doctors_specialist')
	qualification = models.CharField(max_length=255,null=True,blank=True)
	is_active=models.BooleanField(default=True)
	is_delete = models.BooleanField(default=False)
	def __str__(self):
		return self.full_name

class Schedule(models.Model):
	doctor=models.ForeignKey(Doctors, on_delete=models.CASCADE,related_name='schedule_doctor')
	day = models.CharField(choices=DAYS, default='Mon', max_length=3)
	available_date = models.DateField(null=True, blank=True)
	shift = models.CharField(choices=SHIFT_SLOTS, default='M', max_length=1)

class Patients(models.Model):
	full_name = models.CharField(max_length=255,null=True,blank=True)
	mobile = models.CharField(max_length=17,null=True,blank=True)
	age = models.IntegerField(default=1)
	address = models.TextField(default='')
	def __str__(self):
		return self.full_name

class Appointment(models.Model):
	doctor = models.ForeignKey(Doctors, on_delete=models.CASCADE,related_name='appointment_doctor')
	patient = models.ForeignKey(Patients, on_delete=models.CASCADE,related_name='appointment_patient')
	appointment_date = models.DateField(null=True, blank=True)
	timing = models.TimeField(null=True, blank=True)
	registered_date = models.DateTimeField(auto_now_add=True)
