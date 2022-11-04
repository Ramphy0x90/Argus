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

    def test_function_db_data(self):
        func0 = Function.objects.values("name", "department__name").get(name="Test function 0")
        self.assertEqual(func0['name'], "Test function 0")
        self.assertEqual(func0['department__name'], "Test department 0")



class TicketTestCase(TestCase):
    database = '__all__'

    def setUp(self):
        Ticket.objects.create(number=123456, zoho_id=12345678912345678, subject="Test TICKET", author="TEST@TEST.com")

    def test_ticket_db_data(self):
        tck0 = Ticket.objects.values("subject").get(zoho_id=12345678912345678)
        self.assertEqual(tck0['subject'], "Test TICKET")



class LogTestCase(TestCase):
    databases = '__all__'

    def setUp(self):
        new_department = Department.objects.create(name="Test department 0", zoho_id="123", country="TT")
        new_function = Function.objects.create(name="Test function 0", department=new_department)
        new_ticket = Ticket.objects.create(number=123456, zoho_id=12345678912345678, subject="Test TICKET")
        new_log = Log.objects.create(function=new_function, ticket=new_ticket)
    
    def test_log_db_data(self):
        log0 = Log.objects.values("function__name", "ticket__number").get(id=1)
        self.assertEqual(log0['function__name'], "Test function 0")
        self.assertEqual(log0['ticket__number'], 123456)
