from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name="home"),
    path('get-data/', get_data, name="get-data"),
]