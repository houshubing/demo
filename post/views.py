from math import ceil
from django.shortcuts import render, redirect

from post.models import Post
from post.helper import page_cache
from post.helper import read_count
from post.helper import get_top_n
from user.helper import login_required


@page_cache(10)
def post_list(request):
    page = int(request.GET.get('page', 1))  #页码
    per_page = 10                           #每页文章数
    total = Post.objects.count()            #帖子总数
    pages = ceil(total / per_page)          #总页数

    start = (page - 1) * per_page
    end = start + per_page
    posts = Post.objects.all().order_by('-id')[start:end]   #惰性加载（懒加载）
    return render(request, 'post_list.html',{'posts':posts, 'pages': range(pages)})

@login_required
def create_post(request):
    if request.method == 'POST':
        uid = request.session['uid']
        title = request.POST.get("title")
        content = request.POST.get("content")
        post = Post.objects.create(title=title, content=content)
        return  redirect('/post/read/?post_id=%s' % post.id)
    else:
        return render(request, 'create_post.html')

@login_required
def edit_post(request):
    if request.method == 'POST':
        post_id = int(request.POST.get('post_id'))
        post = Post.objects.get(id=post_id)
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        post.save()

        return redirect('/post/read/?post_id=%s' % post.id)
    else:
        post_id = int(request.GET.get('post_id'))
        post = Post.objects.get(id=post_id)
        return render(request, 'edit_post.html', {'post': post})



@read_count
@page_cache(10)
def read_post(request):
    post_id = int(request.GET.get('post_id'))
    post = Post.objects.get(id=post_id)
    return render(request, 'read_post.html', {'post': post})


def search(request):
    keyword = request.POST.get('keyword')
    posts = Post.objects.filter(content__contains=keyword)
    return render(request, 'search.html', {'posts': posts})


def top10(request):
    '''
    1. aaaa 30
    2. bbbb 27
    3. cccc 19
    '''
    rank_data = get_top_n(10)
    return render(request, 'top10.html', {'rank_data': rank_data})
