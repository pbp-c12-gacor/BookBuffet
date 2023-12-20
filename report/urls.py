from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from report.views import *

app_name = 'report'

urlpatterns = [
    path('', create_report, name='create_report'),
    path('show_report/', show_report, name='show_report'),
    path('delete/<int:id>', delete_report, name='delete_report'),
    path('json/', show_report_json, name='show_report_json'),
    path('get-user/<int:user_id>/', get_user_by_id, name='get_user_by_id'),
    path('create-report-flutter/', create_report_flutter, name='create_report_flutter'),
    path('delete-report-flutter/<int:id>', delete_report_flutter, name='delete_report_flutter'),
]