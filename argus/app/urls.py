from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('log/<int:id>', views.log, name='view-log'),
    path('function/<int:id>', views.function, name='view-function'),
]
