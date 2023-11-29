import datetime
import json
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from forum.models import Post, User, Comment
from booksdatabase.models import Book
from forum.forms import PostForm, CommentForm, PostEditForm, CommentEditForm
from django.contrib import messages 
from django.contrib.auth import logout
from django.core import serializers
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def show_forum(request):
    posts = Post.objects.all()
    formP = PostForm()
    formPE = PostEditForm()
    request.COOKIES['authenticated'] = request.user.is_authenticated
    context = {
        'username' : request.user.username,
        'user_id' : request.user.id,
        'posts' : posts,
        'authenticated' : request.COOKIES['authenticated'],
                'formP' : formP,
        'formP' : formP,
        'formPE' : formPE
    }

    return render(request, "forum.html", context)

def show_post(request, post_id):
    post = Post.objects.get(pk = post_id)
    formCE = CommentEditForm()
    formC = CommentForm()
    formP = PostForm()
    formPE = PostEditForm()
    request.COOKIES['authenticated'] = request.user.is_authenticated
    context = {
        'username' : request.user.username,
        'user_id' : request.user.id,
        'post_id' : post.pk,
        'authenticated' : request.COOKIES['authenticated'],
        'formC' : formC,
        'formP' : formP,
        'formCE' : formCE,
        'formPE' : formPE
    }
    return render(request, "detail_post.html", context)

def show_mypost(request):
    request.COOKIES['authenticated'] = request.user.is_authenticated
    formPE = PostEditForm()
    context = {
        'authenticated' : request.COOKIES['authenticated'],
    }
    if request.user.is_authenticated:
        posts = Post.objects.filter(user = request.user)
        context = {
            'username' : request.user.username,
            'user_id' : request.user.id,
            'posts' : posts,
            'authenticated' : request.COOKIES['authenticated'],
            'formPE' : formPE
        }
    return render(request, "my_post.html", context)

@login_required
@csrf_exempt
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES or None)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            if 'book' in form.cleaned_data and form.cleaned_data['book']:
                post.book = form.cleaned_data['book']
            else:
                post.book = None
            post.save()
            return HttpResponse(b"CREATED", status=201)
    else:
        form = PostForm()

    context = {'form': form}
    return render(request, "forum.html", context)

@login_required
@csrf_exempt
def create_comment(request, post_id):
    if request.method == "POST":
        form = CommentForm(request.POST or None)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = get_object_or_404(Post, id=post_id)
            comment.save()
            return HttpResponse(b"CREATED", status=201)
    else:
        form = CommentForm()

    context = {'form': form}
    return render(request, "forum.html", context)

@login_required
@csrf_exempt
def edit_post(request, post_id):
    post = get_object_or_404(Post,id=post_id)
    if request.method == "POST":
        form = PostEditForm(request.POST or None, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return HttpResponse(b"UPDATED", status=200)
    else:
        # Populate the form with the existing post instance
        form = PostEditForm(instance=post)

    context = {'form': form}
    return render(request, "forum.html", context)

@login_required
@csrf_exempt
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.method == "POST":
        form = CommentEditForm(request.POST or None, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.save()
            return HttpResponse(b"UPDATED", status=200)
    else:
        form = PostForm(instance=comment)

    context = {'form': form}
    return render(request, "forum.html", context)

def get_post(request):
    if request.method == 'GET':
        posts = Post.objects.select_related('book').all()
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
    
@csrf_exempt
def create_post_flutter(request):
    if request.method == 'POST':
        
        data = json.loads(request.body)

        new_post = Post.objects.create(
            user = request.user,
            title = data["title"],
            text = data["text"],
        )

        new_post.save()

        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)
    
@csrf_exempt
def create_comment_flutter(request):
    if request.method == 'POST':
        
        data = json.loads(request.body)
        post = Post.objects.get(id=data['post_id'])
        new_comment = Comment.objects.create(
            user = request.user,
            post = post,
            text = data["text"],
        )

        new_comment.save()

        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)
    

@login_required
@csrf_exempt
def delete_post(request, post_id):
    if request.method == "DELETE":
        post = Post.objects.get(pk=post_id, user=request.user)
        post.delete()
        return HttpResponse(b"DELETED", status=201)
    return HttpResponseNotFound()

@login_required
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

def get_comments_by_post_id(request, post_id):
    post = Post.objects.get(pk=post_id)
    comments = post.comments.all()
    return HttpResponse(serializers.serialize("json", comments), content_type="application/json")

def get_comment_by_id(request, comment_id):
    comment = Comment.objects.get(pk=comment_id)
    return HttpResponse(serializers.serialize("json", [comment]), content_type="application/json")

def show_post_json(request):
    data = Post.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_comment(request):
    data = Comment.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")


