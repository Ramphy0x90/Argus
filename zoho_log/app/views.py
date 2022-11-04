from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.utils import timezone

from django.views.decorators.http import require_http_methods
from django.views.decorators.http import require_GET
from django.views.decorators.http import require_POST

from .models import Function
from .models import Ticket
from .models import Department
from .models import Log

from ast import literal_eval



@require_GET
def index(request):
    template = loader.get_template('index.html')
    logs_failed_query = """SELECT * FROM app_log
                                    WHERE Cast((JulianDay('now') - JulianDay(log_in)) * 24 * 60 As Integer) > 3
                                    AND log_out IS NULL"""
    logs_failed = [log.id for log in Log.objects.raw(logs_failed_query)]
    logs = Log.objects.all().values('id', 'function__name', 'ticket__number', 'log_in', 'log_out')
    functions = Function.objects.all().values('id', 'name', 'department__name')
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
                'value': len(logs_failed),
                'icon': 'error.svg',
                'color': '#ec00290d'
            }
        },
        'functions': functions,
        'logs': {
            'all': logs,
            'failed': logs_failed
        }
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


@require_GET
def function(request, id):
    template = loader.get_template('function.html')
    function = Function.objects.values('id', 'name', 'department__name').get(id = id)

    logs_failed_query = """SELECT * FROM app_log
                                    WHERE function_id = %s
                                    AND Cast((JulianDay('now') - JulianDay(log_in)) * 24 * 60 As Integer) > 3
                                    AND log_out IS NULL"""
    logs_failed = [log.id for log in Log.objects.raw(logs_failed_query, [id])]
    logs = Log.objects.values('id', 'function__name', 'ticket__number', 'log_in', 'log_out').filter(function_id = id)

    context = {
        'function': function,
        'logs': {
            'all': logs,
            'failed': logs_failed
        }
    }

    return HttpResponse(template.render(context, request))


def handler404(request, exception=None):
    return render(request, '404.html', status=404)
