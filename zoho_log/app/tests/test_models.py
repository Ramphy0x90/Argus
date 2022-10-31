from django.test import TestCase
from app.models import *


class DepartmentTestCase(TestCase):
    databases = '__all__'

    def setUp(self):
        Department.objects.create(name="Test department 0", zoho_id="123", country="TT")

    def test_department_db_data(self):
        dep0 = Department.objects.values("name").get(zoho_id="123")
        self.assertEqual(dep0['name'], "Test department 0")



class FunctionTestCase(TestCase):
    databases = '__all__'

    def setUp(self):
        new_department = Department.objects.create(name="Test department 0", zoho_id="123", country="TT")
        Function.objects.create(name="Test function 0", department=new_department)
        test = Function.objects.all().values()

    def test_function_db_data(self):
        func0 = Function.objects.values("name", "department__name").get(name="Test function 0")
        self.assertEqual(func0['name'], "Test function 0")
        self.assertEqual(func0['department__name'], "Test department 0")
