from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from django.views.decorators.http import require_http_methods
from django.views.decorators.http import require_GET
from django.views.decorators.http import require_POST

from .models import Function
from .models import Ticket
from .models import Department
from .models import Log

from ast import literal_eval

from django.views.decorators.csrf import csrf_exempt

@require_GET
def index(request):
    template = loader.get_template('index.html')

    logs = Log.objects.all().values('id', 'function__name', 'ticket__number', 'log_in')
    functions = Function.objects.all().values('name', 'department__name')
    departments = Department.objects.all().values()

    context = {
        'dashboard_data': {
            'Functions': {
                'value': functions.count(),
                'icon': 'function.svg',
                'color': '#9ef01a12'
            },
            'Departments': {
                'value': departments.count(),
                'icon': 'department.svg',
                'color': '#3a86ff0d'
            },
            'Fails': {
                'value': 2,
                'icon': 'error.svg',
                'color': '#ec00290d'
            }
        },
        'functions': functions,
        'logs': logs
    }

    return HttpResponse(template.render(context, request))

@require_GET
def log(request, id):
    template = loader.get_template('log.html')
    log = Log.objects.values('id', 'function_id', 'ticket_id', 'log_in').get(id = id)
    function = Function.objects.values('id', 'name', 'department__name').get(id = log['function_id'])
    ticket = Ticket.objects.values('number', 'zoho_id', 'subject', 'author').get(id = log['ticket_id'])

    context = {
        'log': log,
        'function': function,
        'ticket': ticket
    }

    return HttpResponse(template.render(context, request))


"""
log_in
------
    This request is used to register the
    entry of a Zoho function thats is monitored
"""
@csrf_exempt
@require_POST
def log_in(request):
    # Transform POST body data to dictionary
    body_data = literal_eval(request.body.decode('utf-8'))

    # Get POST data
    function = body_data['function']
    departmentId = body_data['department']
    ticketId = body_data['ticket']

    # Search on database for the required entities
    # to create a new log
    function_data = Function.objects.filter(name = function)
    ticket_data = Ticket.objects.filter(zoho_id = ticketId)
    department_data = Department.objects.filter(zoho_id = departmentId)

    if ticket_data.count() == 0:
        new_ticket = Ticket(zoho_id = ticketId)
        new_ticket.save()
        ticket_data = Ticket.objects.filter(zoho_id = ticketId)

    if department_data.count() == 0:
        new_department = Department(name = 'Test department', zoho_id = departmentId)
        new_department.save()
        department_data = Department.objects.filter(zoho_id = departmentId)

    if function_data.count() == 0:
        department_instance = Department(id = department_data.values()[0]['id'])
        new_function = Function(name = function, department = department_instance)
        new_function.save()
        function_data = Function.objects.filter(name = function)

    # Create a new function log
    function_instance = Function(id = function_data.values()[0]['id'])
    ticket_instamce = Ticket(id = ticket_data.values()[0]['id'])
    new_log = Log(function = function_instance, ticket = ticket_instamce)
    new_log.save()

    return HttpResponse(1)


def log_out(request):
        # Transform POST body data to dictionary
    body_data = literal_eval(request.body.decode('utf-8'))

    # Get POST data
    function = body_data['function']
    departmentId = body_data['department']
    ticketId = body_data['ticket']