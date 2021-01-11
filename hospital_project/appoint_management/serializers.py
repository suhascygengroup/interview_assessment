from rest_framework import serializers
from .models import *
from django.core.validators import RegexValidator 
from django.conf import settings
from datetime import datetime, timedelta

SHIFT_INTERVALS = {
		'M':['08:00','17:00'],
		'A':['14:00','23:00'],
		'E':['17:00','02:00'],
		'N':['00:00','09:00'],
	}

def timeSlots(k,slot_time):
	hours = []
	is_breaktime = []
	start_time,end_time=SHIFT_INTERVALS[k][0],SHIFT_INTERVALS[k][1]
	time = datetime.strptime(start_time, '%H:%M')
	end = datetime.strptime(end_time, '%H:%M')
	print(time,end)
	gt24=0
	if time > end:
		gt24=1
		time = time-timedelta(hours=12)
		end = end+timedelta(hours=12)
	breaktime = time+timedelta(hours=3,minutes=30)
	while time < end:
		if gt24 ==1:
			hours.append((time+timedelta(hours=12)).strftime("%H:%M:%S"))
		else:	
			hours.append(time.strftime("%H:%M:%S"))
		if time ==breaktime:
			if gt24==1:
				is_breaktime.append((time+timedelta(hours=12,minutes=30)).strftime("%H:%M:%S"))
				is_breaktime.append((time+timedelta(hours=13,minutes=30)).strftime("%H:%M:%S"))
			else:
				is_breaktime.append((time+timedelta(minutes=30)).strftime("%H:%M:%S"))
				is_breaktime.append((time+timedelta(hours=1,minutes=30)).strftime("%H:%M:%S"))
			time += timedelta(hours=1)
		time += timedelta(minutes=slot_time)
	# print(hours,is_breaktime)
	return hours,is_breaktime

class DoctorsSerializer(serializers.ModelSerializer):
	phone_regex = RegexValidator(regex=r'^\+?1?\d{10,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
	mobile = serializers.CharField(validators=[phone_regex], max_length=15,required=True)
	age_regex = RegexValidator(regex=r'^\d{2,3}$',message="Age must be in natural number format and greater than 23")
	age = serializers.IntegerField(validators=[age_regex],required=True)

	full_name = serializers.CharField(max_length=255,required=True)
	address = serializers.CharField(max_length=255,required=True)
	qualification = serializers.CharField(max_length=255,required=True)
	class Meta:
		model = Doctors
		fields = '__all__'

	def validate_mobile(self, value):
		check_query = Doctors.objects.filter(mobile=value)
		# if self.parent is not None and self.parent.instance is not None:
		#     genre = getattr(self.parent.instance, self.field_name)
		#     check_query = check_query.exclude(pk=genre.pk)
		if self.instance:
			check_query = check_query.exclude(pk=self.instance.pk)
		if check_query.exists():
			raise serializers.ValidationError('A User with this phone number already exists.')
		return value

class PatientSerializer(serializers.ModelSerializer):
	phone_regex = RegexValidator(regex=r'^\+?1?\d{10,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
	mobile = serializers.CharField(validators=[phone_regex], max_length=15)
	age_regex = RegexValidator(regex=r'^\d{1,3}$',message="Age must be in natural number format")
	age = serializers.IntegerField(validators=[age_regex])
	full_name = serializers.CharField(max_length=255,required=True)
	address = serializers.CharField(max_length=255,required=True)
	class Meta:
		model = Patients
		fields = '__all__'
	def validate_mobile(self, value):
		check_query = Patients.objects.filter(mobile=value)
		if self.instance:
			check_query = check_query.exclude(pk=self.instance.pk)
		if check_query.exists():
			raise serializers.ValidationError('A User with this phone number already exists.')
		return value

'''
class ScheduleSerializer(serializers.ModelSerializer):
	class Meta:
		many=True
		model = Schedule
		fields = '__all__'
The above serializer is not in use currently
'''
class AppointmentSerializer(serializers.ModelSerializer):
	timing = serializers.TimeField(format=settings.TIME_FORMAT,required=True)
	appointment_date = serializers.DateField(required=True)
	class Meta:
		model = Appointment
		fields = '__all__'

	@classmethod
	def validate(self,data):
		errors={}
		if data.get('doctor')!= None and data.get('patient') !=None:
			doc = data.get('doctor').id
			patient = data.get('patient').id
			date = data.get('appointment_date')
			timing = data.get('timing')
			schedule = Schedule.objects.filter(doctor=doc,available_date=date)
			if schedule:
				appointment = Appointment.objects.filter(doctor=doc,appointment_date=date,timing=timing)
				if appointment :
					print(appointment[0].patient)
					if appointment[0].patient.id == patient:
						errors['msg'] = "Appointment Already Exist!!!"
					else:
						errors['msg'] = "This slot is appointed to somebody else. "
				else:
					print(schedule[0].shift)
					if schedule[0].shift in SHIFT_INTERVALS:
						intervals,breaks=timeSlots(schedule[0].shift,30)
						print(intervals,breaks)
						print(timing ,intervals[9])
						if str(timing) not in intervals:
							errors['msg'] = "You can only have appointment in these slots("+','.join(intervals)+") on selected date."
							errors['msg']+="Lunch Break is in between "+' and '.join(breaks)
			else:
				errors['msg'] = "Appointment Schedule will be available soon for the selected doctor and day respectively."
			
		if errors :
			raise serializers.ValidationError(errors)
		return super(AppointmentSerializer, self).validate(self, data)