from django.urls import path
from . import views

urlpatterns = [
    path('get-key', views.get_key, name = 'get_key'),
    path('log-in', views.log_in, name = 'log_in'),
    path('log-out', views.log_out, name = 'log_out'),
]
