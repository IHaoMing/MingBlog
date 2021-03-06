#coding:utf-8
import markdown
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from comments.forms import CommentForm
from .models import Post, Category

def index(request):
    post_list = Post.objects.all().order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})

#文章详情的视图
def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # 阅读量 +1
    post.increase_views()
    post.body = markdown.markdown(post.body,
                                  extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                      'markdown.extensions.toc',
                                  ])
    # 记得在顶部导入 CommentForm
    form = CommentForm()
    # 获取这篇 post 下的全部评论
    comment_list = post.comment_set.all()

    # 将文章、表单、以及文章下的评论列表作为模板变量传给 detail.html 模板，以便渲染相应数据。
    context = {'post': post,
               'form': form,
               'comment_list': comment_list
               }
    return render(request, 'blog/detail.html', context=context)

def archives(request):
    post_list = Post.objects.all().order_by('-created_time')
    return render(request, 'blog/archives.html', context={'post_list': post_list})

def about(request):
    return render(request, 'blog/about.html')

   
