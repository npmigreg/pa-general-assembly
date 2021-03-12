from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name="home"),
    path('get-hb-data/', get_hb_data, name="get-hb-data"),
    path('get-hr-data/', get_hr_data, name="get-hr-data"),
    path('get-sb-data/', get_sb_data, name="get-sb-data"),
    path('get-sr-data/', get_sr_data, name="get-sr-data"),
    path('house-bills/', HouseBillsList.as_view(template_name = "main/house_bills.html"), name='house-bills'),
    path('house-resolutions/', HouseResolutionsList.as_view(template_name = "main/house_resolutions.html"), name='house-resolutions'),
    path('senate-bills/', SenateBillsList.as_view(template_name = "main/senate_bills.html"), name='senate-bills'),
    path('senate-resolutions/', SenateResolutionsList.as_view(template_name = "main/senate_resolutions.html"), name='senate-resolutions'),
    path('house-bills/dashboard/', hb_dashboard, name="hb-dashboard"),
    path('house-resolutions/dashboard/', hr_dashboard, name="hr-dashboard"),
    path('senate-bills/dashboard/', sb_dashboard, name="sb-dashboard"),
    path('senate-resolutions/dashboard/', sr_dashboard, name="sr-dashboard"),
    path('house-bills/text-analysis', hb_text_analysis, name="hb-text-analysis"),
    path('house-resolutions/text-analysis/', hr_text_analysis, name="hr-text-analysis"),
    path('senate-resolutions/text-analysis/', sr_text_analysis, name="sr-text-analysis"),
    path('senate-bills/text-analysis/', sb_text_analysis, name="sb-text-analysis"),
    path('api/data/hb/', RenderHBData.as_view()),
    path('api/data/hr/', RenderHRData.as_view()),
    path('api/data/sb/', RenderSBData.as_view()),
    path('api/data/sr/', RenderSRData.as_view()),
]