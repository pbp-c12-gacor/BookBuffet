import datetime
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse
from forum.models import Post, User, Comment
from forum.forms import PostForm, CommentForm
from django.contrib import messages 
from django.contrib.auth import logout
from django.core import serializers
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def logout_user(request):
    logout(request)
    return redirect('forum:login')

def show_forum(request):
    posts = Post.objects.all()
    context = {
        'username' : request.user.username,
        'user_id' : request.user.id,
        'posts' : posts
    }

    return render(request, "forum.html", context)

def show_post(request, post_id):
    post = Post.objects.get(pk = post_id)
    context = {
        'username' : request.user.username,
        'user_id' : request.user.id,
        'post_id' : post.pk
    }
    return render(request, "detail_post.html", context)

def show_mypost(request):
    posts = Post.objects.filter(user = request.user)
    context = {
        'username' : request.user.username,
        'user_id' : request.user.id,
        'posts' : posts
    }
    return render(request, "my_post.html", context)
def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('forum:login'))
    response.delete_cookie('last_login')
    return response

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            response = HttpResponseRedirect(reverse("forum:show_forum")) 
            response.set_cookie('last_login', str(datetime.datetime.now()))
            response.set_cookie('user_id', user.id)
            return response
        else:
            messages.info(request, 'Sorry, incorrect username or password. Please try again.')
    context = {}
    return render(request, 'login.html', context)

def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('forum:login')
    context = {'form':form}
    return render(request, 'register.html', context)

def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        text = request.POST.get("content")
        image = request.FILES.get('image')
        user = request.user
        new_post = Post(title = title, image=image, text=text, user=user)
        new_post.save()
        return HttpResponse(b"CREATED", status=201)

    return HttpResponseNotFound()

def get_post(request):
    if request.method == 'GET':
        posts = Post.objects.all()
        return HttpResponse(serializers.serialize("json", posts), content_type="application/json")
    else:
        return HttpResponse("Invalid HTTP method.", status=405)
def get_comment(request):
    if request.method == 'GET':
        comments = Comment.objects.all()
        return HttpResponse(serializers.serialize("json", comments), content_type="application/json")
    else:
        return HttpResponse("Invalid HTTP method.", status=405)

def get_post_by_id(request, post_id):
    if request.method == 'GET':
        post = get_object_or_404(Post, pk=post_id)
        return HttpResponse(serializers.serialize("json", [post]), content_type="application/json")
    

def create_comment(request, post_id):
    if request.method == 'POST':
        text = request.POST.get("content")
        post = get_object_or_404(Post, id=post_id)
        user = request.user

        # Create the comment
        comment = Comment(text=text, post=post, user=user)
        comment.save()

        return HttpResponse(b"CREATED", status=201)

    return HttpResponseNotFound()

def create_reply(request, comment_id):
    parent_comment = get_object_or_404(Comment, id=comment_id)
    form = CommentForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        reply = form.save(commit=False)
        reply.user = request.user
        reply.post = parent_comment.post
        reply.parent = parent_comment
        reply.save()
        return redirect('forum:show_forum')

    context = {'form': form}
    return render(request, "create_reply.html", context)

@csrf_exempt
def delete_post(request, post_id):
    if request.method == "DELETE":
        post = Post.objects.get(pk=post_id, user=request.user)
        post.delete()
        return HttpResponse(b"DELETED", status=201)
    return HttpResponseNotFound()

@csrf_exempt
def delete_comment(request, comment_id):
    if request.method == "DELETE":
        comment = Comment.objects.get(pk=comment_id, user=request.user)
        comment.delete()
        return HttpResponse(b"DELETED", status=201)
    return HttpResponseNotFound()

def get_user_by_id(request, user_id):
    user = User.objects.filter(id=user_id)
    return HttpResponse(serializers.serialize("json", user), content_type="application/json")

def get_comments_by_id(request, post_id):
    post = Post.objects.get(pk=post_id)
    comments = post.comments.all()
    return HttpResponse(serializers.serialize("json", comments), content_type="application/json")

