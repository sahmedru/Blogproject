from django.shortcuts import render, get_object_or_404, redirect
from .models import posts, tags, categories, comments
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q

# Create your views here.
def posts_list(request):
    categoryQ=request.GET.get('category', None)
    tagQ=request.GET.get('tag', None)
    if categoryQ:
        post = posts.objects.filter(category__name=categoryQ)
    elif tagQ:
        post = posts.objects.filter(tag__name=tagQ)
    else:
        post = posts.objects.all()
    tag = tags.objects.all()
    category = categories.objects.all()
    
    return render(request, 'blog/All_posts.html', {'post': post, 'tag': tag, 'category': category})

def post_detail(request, id):
    post = get_object_or_404(posts, id=id)
    tag = tags.objects.all()
    category = categories.objects.all()
    comment_Form = CommentForm()
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
        
    if post.liked_users.filter(id=request.user.id):
        is_liked = True
    else:
        is_liked = False

    like_count = post.liked_users.count()
    comment = post.comments_set.all()
    context = {'post': post, 'category': category, 'tag': tag, 'comment': comment, 'comment_form': comment_Form, 'is_liked': is_liked, 'like_count': like_count}
    

    post.view_count += 1
    post.save()
    return render(request, 'blog/post_detail.html', context)
@login_required
def like_post(request, id):
    post = get_object_or_404(posts, id=id)
    if post.liked_users.filter(id=request.user.id):
        post.liked_users.remove(request.user)
    else:
        post.liked_users.add(request.user)
    return redirect('post_detail', id=post.id)


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('posts_list')
    else:
        form = UserCreationForm()

    return render(request, 'registration/signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('posts_list')




@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', id=post.id)
    else:
        form = PostForm()
    return render(request, 'blog/create_post.html', {'form': form})

from django.contrib import messages
@login_required
def post_update(request, id):
    post = get_object_or_404(posts, id=id)
    if request.user!= post.author:
        messages.error(request,'You do not have permission to update this post')
        return redirect('post_detail', id= post.id)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Updated Successfully')
            return redirect('post_detail', id=post.id)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/create_post.html', {'form': form})

@login_required
def post_delete(request, id):
    post = get_object_or_404(posts, id=id)
    if request.user!= post.author:
        messages.error(request,'You do not have permission to delete this post')
        return redirect('post_detail', id= post.id)
    post.delete()
    messages.success(request, 'Deleted Successfully')
    return redirect('posts_list')
