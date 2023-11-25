from django.urls import path
from forum.views import *
from django.conf.urls.static import static
from django.conf import settings


app_name = 'forum'

urlpatterns = [
    path('', show_forum, name='show_forum'),
    path('post/<int:post_id>', show_post, name='show_post'),
    path('mypost/', show_mypost, name='show_mypost'),
    path('create-post/', create_post, name='create_post'),
    path('get-post/', get_post, name='get_post'),
    path('get-post/<int:post_id>/', get_post_by_id, name='get_post_by_id'),
    path('get-user/<int:user_id>/', get_user_by_id, name='get_user_by_id'),
    path('get-comments/', get_comment, name='get_comment'),
    path('create-comment/<int:post_id>/', create_comment, name='create_comment'),
    path('get-comments/<int:post_id>/', get_comments_by_post_id, name='get_comments_by_post_id'),
    path('get-comment/<int:comment_id>/', get_comment_by_id, name='get_comment_by_id'),
    path('delete-comment/<int:comment_id>/', delete_comment, name='delete_comment'),
    path('delete-post/<int:post_id>/', delete_post, name='delete_post'),
    path('edit-post/<int:post_id>/', edit_post, name='edit_post'),
    path('edit-comment/<int:comment_id>/', edit_comment, name='edit_comment'),
    path('post/json/', show_post_json, name='show_post'),
    path('comment/json/', show_comment, name='show_comment'),
    path('create-post-flutter/', create_post_flutter, name='create_post_flutter'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)