from django.test import TestCase
from .models import* 
# Create your tests here.

class DoctorTest(TestCase):
	def setUp(self):
		SpecialFields.objects.create(
				specialist_in='Brain'
			)
		Doctors.objects.create(full_name="Varalaxmi Beesu",age=25,qualification='M.B.B.S',specialist_id=1)

	def test_get_method(self):
		url='http://localhost:8000/api/doctor/'
		response = self.client.get(url)
		self.assertEqual(response.status_code,200)
		qs = Doctors.objects.filter(full_name__icontains="Varalaxmi Beesu")
		self.assertEqual(qs.count(),1)

	def test_post_method_success(self):
		url='http://localhost:8000/api/doctor/'
		data={
		'full_name':"Varalaxmi Beesu",
		'age':25,
		'mobile':'+9184298158',
		'qualification':'M.B.B.S',
		'address':'Mumbai Central',
		'specialist':1
		}
		response = self.client.post(url,data,format='json')
		print('POST success',response.status_code)
		self.assertEqual(response.status_code,201)

	def test_put_method_success(self):
		url = 'http://localhost:8000/api/doctor/1/'
		data={
		'full_name':"Varalaxmi Besu",
		'age':29,
		'mobile':'+9184298158',
		'qualification':'M.B.B.S',
		'address':'Mumbai Central',
		'specialist':1
		}
		response = self.client.put(url,data,content_type='application/json')
		print('response',response.data)
		print("PUT success",response.status_code)
		self.assertEqual(response.status_code,200)

	def test_post_method_fail(self):
		url='http://localhost:8000/api/doctor/'
		data={
		'full_name':"Varalaxmi Beesu",
		'age':25,
		# 'specialist':1
		}
		response = self.client.post(url,data,format='json')
		print('POST FAIL',response.status_code)
		self.assertEqual(response.status_code,400)


	def test_delete_method_success(self):
		url = 'http://localhost:8000/api/doctor/1/'
		response = self.client.delete(url)
		print("Delete success",response.status_code)
		self.assertEqual(response.status_code,204)

class PatientTest(TestCase):
	def setUp(self):
		SpecialFields.objects.create(
				specialist_in='Brain'
			)
		Patients.objects.create(full_name="Roy Beesu",age=25,mobile='+9194952027')

	def test_get_method(self):
		url='http://localhost:8000/api/patient/'
		response = self.client.get(url)
		self.assertEqual(response.status_code,200)
		qs = Patients.objects.filter(full_name__icontains="Roy Beesu")
		self.assertEqual(qs.count(),1)

	def test_post_method_success(self):
		url='http://localhost:8000/api/patient/'
		data={
		'full_name':"Aaradhya Beesu",
		'age':5,
		'mobile':'+9184298158',
		'address':'Mumbai Central',
		}
		response = self.client.post(url,data,format='json')
		print('POST success',response.status_code)
		self.assertEqual(response.status_code,201)

	def test_put_method_success(self):
		url = 'http://localhost:8000/api/patient/1/'
		data={
		'full_name':"Pooja Beesu",
		'age':29,
		'mobile':'+9184298158',
		'address':'Mumbai Central',
		}
		response = self.client.put(url,data,content_type='application/json')
		print('response',response.data)
		print("PUT success",response.status_code)
		self.assertEqual(response.status_code,200)

	def test_post_method_fail(self):
		url='http://localhost:8000/api/patient/'
		data={
		'full_name':"Varalaxmi Beesu",
		'age':25,
		}
		response = self.client.post(url,data,format='json')
		print('POST FAIL',response.status_code)
		self.assertEqual(response.status_code,400)


	def test_delete_method_success(self):
		url = 'http://localhost:8000/api/patient/1/'
		response = self.client.delete(url)
		print("Delete success",response.status_code)
		self.assertEqual(response.status_code,204)

class AppointmentTest(TestCase):
	def setUp(self):
		SpecialFields.objects.create(
				specialist_in='Brain'
			)
		Doctors.objects.create(full_name="Varalaxmi Beesu",age=25,mobile='+9194952025',qualification='M.B.B.S',specialist_id=1)
		Patients.objects.create(full_name="Nitin Beesu",age=20,mobile='+9194952025')
		Schedule.objects.create(doctor_id=1,available_date='2021-01-11',shift='M')
		Appointment.objects.create(
			doctor_id=1,
			patient_id=1,
			timing='12:00',
			appointment_date='2021-01-11')

	def test_get_method(self):
		url='http://localhost:8000/api/appointment/'
		response = self.client.get(url)
		self.assertEqual(response.status_code,200)
		qs = Appointment.objects.filter(doctor_id__full_name__icontains="Varalaxmi Beesu",appointment_date='2021-01-11',timing='12:00')
		self.assertEqual(qs.count(),1)

	def test_post_method_success(self):
		url='http://localhost:8000/api/appointment/'
		data={
		'doctor':1,
		'patient':1,
		'timing':'8:00',
		'appointment_date':'2021-01-11'
		}
		response = self.client.post(url,data,format='json')
		print('Appointment POST success',response.status_code)
		self.assertEqual(response.status_code,201)

	def test_put_method_success(self):
		url = 'http://localhost:8000/api/appointment/1/'
		data={
		'doctor':1,
		'patient':1,
		'timing':'9:30',
		'appointment_date':'2021-01-11'
		}
		response = self.client.put(url,data,content_type='application/json')
		print("Appointment PUT success",response.status_code)
		self.assertEqual(response.status_code,200)

	def test_post_method_fail(self):
		url='http://localhost:8000/api/appointment/'
		data={
		'patient':4,
		'appointment_date':''
		}
		response = self.client.post(url,data,format='json')
		print('Appointment POST FAIL',response.status_code)
		self.assertEqual(response.status_code,400)


	def test_delete_method_success(self):
		url = 'http://localhost:8000/api/appointment/1/'
		response = self.client.delete(url)
		print("Appointment Delete success",response.status_code)
		self.assertEqual(response.status_code,204)
