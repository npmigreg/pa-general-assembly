from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name="home"),
    path('get-sb-data/', get_sb_data, name="get-sb-data"),
    path('senate-bills/', senate_bills.as_view(template_name = "main/senate_bills.html"), name='senate-bills'),
]