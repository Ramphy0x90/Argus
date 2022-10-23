from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('log-in', views.log_in, name = 'log_in')
]