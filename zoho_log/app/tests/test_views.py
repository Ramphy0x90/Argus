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
