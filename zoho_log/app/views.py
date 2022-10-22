from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

def index(request):
    template = loader.get_template('index.html')

    context = {
        'dashboard_data': {
            'Functions': {
                'value': 3,
                'icon': 'function.svg'
            },
            'Departments': {
                'value': 5,
                'icon': 'department.svg'
            },
            'Fails': {
                'value': 2,
                'icon': 'error.svg'
            }
        }
    }

    return HttpResponse(template.render(context, request))