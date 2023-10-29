from django.urls import path
from publish.views import *
from main.views import *

app_name = 'publish'

urlpatterns = [
    path('', publish_book, name='publish_book'),
    path('get-publish/<int:id>', get_publish_by_id, name='get_publish_by_id'),
    path('get-publish/', get_publish, name='get_publish'),
    path('verify-publish/', verify_publish, name='verify_publish'),
    path('my-publish/', my_publish, name='my_publish'),
    path('show-publish-detail/<int:id>', show_publish_detail, name='show_publish_detail'),
]