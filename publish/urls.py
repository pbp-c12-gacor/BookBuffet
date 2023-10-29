from django.urls import path
from publish.views import *
from main.views import *
from django.conf import settings
from django.conf.urls.static import static

app_name = 'publish'

urlpatterns = [
    path('', publish_book, name='publish_book'),
    path('get-publish/<int:id>', get_publish_by_id, name='get_publish_by_id'),
    path('get-publish/', get_publish, name='get_publish'),
    path('verify-publish/', verify_publish, name='verify_publish'),
    path('my-publish/', my_publish, name='my_publish'),
    path('show-publish-detail/<int:id>/', show_publish_detail, name='show_publish_detail'),
    path('delete-all-publish/', delete_all_publish, name='delete_all_publish'),
    path('get-unverified-publish/', get_unverified_publish, name='get_unverified_publish'),
    path('get-user/<int:id>/', get_user, name='get_user'),
    path('confirming-publish/<int:id>/', confirming_publish, name='confirming_publish'),
    path('my-publish/delete-publish/<int:id>/', delete_publish_by_id, name='delete_publish_by_id')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)