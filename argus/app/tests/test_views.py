from django.test import TestCase
from django.urls import reverse
from app.models import *


class IndexTest(TestCase):
    def test_url_exists_at_correct_location(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_template(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")



class FunctionTest(TestCase):
    def setUp(self):
        new_department = Department.objects.create(name="Test department 0", zoho_id="123", country="TT")
        Function.objects.create(name="Test function 0", department=new_department)

    def test_url_returns_404(self):
        response = self.client.get("/function")
        self.assertEqual(response.status_code, 404)

    def test_url_exists_at_correct_location(self):
        response = self.client.get("/function/1")
        self.assertEqual(response.status_code, 200)

    def test_template(self):
        response = self.client.get("/function/1")
        self.assertTemplateUsed(response, "function.html")

        response = self.client.get("/function/")
        self.assertTemplateUsed(response, "404.html")



class LogTest(TestCase):
    def setUp(self):
        new_department = Department.objects.create(name="Test department 0", zoho_id="123", country="TT")
        new_function = Function.objects.create(name="Test function 0", department=new_department)
        new_ticket = Ticket.objects.create(number=123456, zoho_id=12345678912345678, subject="Test TICKET")
        new_log = Log.objects.create(function=new_function, ticket=new_ticket)

    def test_url_returns_404(self):
        response = self.client.get("/log")
        self.assertEqual(response.status_code, 404)

    def test_url_exists_at_correct_location(self):
        response = self.client.get("/log/1")
        self.assertEqual(response.status_code, 200)
        
    def test_template(self):
        response = self.client.get("/log/1")
        self.assertTemplateUsed(response, "log.html")

        response = self.client.get("/log/")
        self.assertTemplateUsed(response, "404.html")
