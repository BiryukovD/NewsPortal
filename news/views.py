from django.http import HttpResponseRedirect, request
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .filters import PostFilter
from .forms import *
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class PostList(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'
    ordering = 'time_in'
    paginate_by = 10



class PostListWithFilter(ListView):
    model = Post
    template_name = 'posts_with_filter.html'
    context_object_name = 'posts'
    ordering = 'time_in'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post', 'news.change_post')
    form_class = PostForm
    model = Post
    template_name = 'news_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = 'NEWS'
        return super().form_valid(form)


class NewsEdit(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.add_post', 'news.change_post')
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'


class NewsDelete(DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('posts')


class ArticleCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post', 'news.change_post')
    form_class = PostForm
    model = Post
    template_name = 'article_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = 'ARTICLE'
        return super().form_valid(form)


class ArticleEdit(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.add_post', 'news.change_post')
    model = Post
    template_name = 'article_edit.html'
    form_class = PostForm


class ArticleDelete(DeleteView):
    model = Post
    template_name = 'article_delete.html'
    success_url = reverse_lazy('posts')

