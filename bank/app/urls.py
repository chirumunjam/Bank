from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('1/',register, name='register'),
    path('2/',pin, name='pin'),
    path('3/',balance, name='balance'),
    path('4/',withdraw, name='withdraw'),
    path('5/',deposit, name='deposit'),
    path('6/',transfer, name='transfer'),

]