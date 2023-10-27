from django.urls import path
from publish.views import *
from main.views import *

app_name = 'publish'

urlpatterns = [
    path('', show_publish, name='show_publish'),
    path('verify-publish/', verify_publish, name='verify_publish'),
    path('show-publish-detail/<int:id>', show_publish_detail, name='show_publish_detail'),
]