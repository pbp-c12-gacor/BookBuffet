from django.forms import ModelForm
from forum.models import Post, Comment

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ["title","image", "text"]
class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]