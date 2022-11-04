from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.views.decorators.http import require_POST
from django.core.management.utils import get_random_secret_key

from app.models import Function
from app.models import Ticket
from app.models import Department
from app.models import Log

from ast import literal_eval
from app.services.Zoho import Zoho

from django.views.decorators.csrf import csrf_exempt
import datetime

zoho_service = Zoho()


@csrf_exempt
@require_POST
def log_in(request):
    # Transform POST body data to dictionary
    body_data = literal_eval(request.body.decode('utf-8'))

    # Get POST data
    function = body_data['function']
    departmentId = body_data['department']
    ticketId = body_data['ticket']

    # Get data from ZOHO
    get_ticket = zoho_service.get_ticket(ticketId)
    get_department = zoho_service.get_department(departmentId)

    # Search on database for the required entities
    # to create a new log
    function_data = Function.objects.filter(name = function)
    ticket_data = Ticket.objects.filter(zoho_id = ticketId)
    department_data = Department.objects.filter(zoho_id = departmentId)

    if ticket_data.count() == 0:
        new_ticket = Ticket(zoho_id = ticketId, number=get_ticket['ticketNumber'], subject=get_ticket['subject'], author=get_ticket['email'])
        new_ticket.save()
        ticket_data = Ticket.objects.filter(zoho_id = ticketId)

    if department_data.count() == 0:
        new_department = Department(name = get_department['name'], zoho_id = departmentId)
        new_department.save()
        department_data = Department.objects.filter(zoho_id = departmentId)

    if function_data.count() == 0:
        department_instance = Department(id = department_data.values()[0]['id'])
        new_function = Function(name = function, department = department_instance)
        new_function.save()
        function_data = Function.objects.filter(name = function)

    # Create a new function log
    new_key = get_key()
    function_instance = Function(id = function_data.values()[0]['id'])
    ticket_instance = Ticket(id = ticket_data.values()[0]['id'])
    new_log = Log(function = function_instance, ticket = ticket_instance, key = new_key)
    new_log.save()

    return JsonResponse({'key':new_key})


@csrf_exempt
@require_POST
def log_out(request):
    # Transform POST body data to dictionary
    body_data = literal_eval(request.body.decode('utf-8'))

    # Get POST data
    function = body_data['function']
    departmentId = body_data['department']
    ticketId = body_data['ticket']
    key = body_data['key']

    # Search data on db
    function_data = Function.objects.filter(name = function)
    ticket_data = Ticket.objects.filter(zoho_id = ticketId)
    # Prepare instances
    function_instance = Function(id = function_data.values()[0]['id'])
    ticket_instance = Ticket(id = ticket_data.values()[0]['id'])

    # Search log
    log = Log.objects.filter(function = function_instance, ticket = ticket_instance, key = key)
    log.update(log_out = datetime.datetime.now())

    return HttpResponse(status = 200)


def get_key():
    return get_random_secret_key()


