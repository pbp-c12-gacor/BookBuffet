from django.urls import path
from publish.views import *
from main.views import *

app_name = 'publish'

urlpatterns = [
    path('', show_publish, name='show_publish')

]