from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name="home"),
    path('get-sb-data/', get_sb_data, name="get-sb-data"),
    path('get-sr-data/', get_sr_data, name="get-sr-data"),
    path('senate-bills/', SenateBillsList.as_view(template_name = "main/senate_bills.html"), name='senate-bills'),
    path('senate-resolutions/', SenateResolutionsList.as_view(template_name = "main/senate_resolutions.html"), name='senate-resolutions'),
    path('senate-bills/dashboard/', sb_dashboard, name="sb-dashboard"),
    path('senate-resolutions/dashboard/', sr_dashboard, name="sr-dashboard"),
    path('senate-resolutions/text-analysis/', sr_text_analysis, name="sr-text-analysis"),
    path('api/data/sb/', RenderSBData.as_view()),
    path('api/data/sr/', RenderSRData.as_view()),
]