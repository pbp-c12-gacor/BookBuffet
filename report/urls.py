from django.urls import path
from forum.views import *
from django.conf.urls.static import static
from django.conf import settings
from report.views import *

app_name = 'report'

urlpatterns = [
    path('', create_report, name='create_report'),
    path('show_report/', show_report, name='show_report'),
    path('delete/<int:id>', delete_report, name='delete_report'),
]