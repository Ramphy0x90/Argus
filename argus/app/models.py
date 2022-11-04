from django.db import models

""" Department Model"""
class Department(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    zoho_id = models.IntegerField(default=-1)
    country = models.CharField(max_length=255)

""" Function Model"""
class Function(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

""" Ticket Model"""
class Ticket(models.Model):
    id = models.AutoField(primary_key=True)
    number = models.IntegerField(default=-1)
    zoho_id = models.IntegerField(default=-1)
    subject = models.CharField(max_length=255)
    author = models.CharField(max_length=255)

""" Log Model"""
class Log(models.Model):
    id = models.AutoField(primary_key=True)
    function = models.ForeignKey(Function, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    key = models.CharField(max_length=255, null=True)
    log_in = models.DateTimeField(auto_now=True)
    log_out = models.DateTimeField(null = True)

""" Zoho token Model """
class ZohoToken(models.Model):
    id = models.AutoField(primary_key=True)
    token = models.CharField(max_length=255)
    creation = models.DateTimeField(auto_now=True)
