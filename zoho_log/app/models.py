from django.db import models

""" Department Mmodel"""
class Department(models.Model):
    name = models.CharField(max_length=255)
    zoho_id = models.IntegerField(default=-1)
    country = models.CharField(max_length=255)

""" Function Mmodel"""
class Function(models.Model):
    name = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

""" Ticket Mmodel"""
class Ticket(models.Model):
    number = models.IntegerField(default=-1)
    zoho_id = models.IntegerField(default=-1)
    subject = models.CharField(max_length=255)
    author = models.CharField(max_length=255)

""" Log Mmodel"""
class Log(models.Model):
    function = models.ForeignKey(Function, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    log_in = models.DateTimeField(auto_now=True)
    log_out = models.DateTimeField(null = True)
