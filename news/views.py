from django.http import HttpResponseRedirect, request, HttpResponse
from django.shortcuts import render, redirect

from django.template.loader import render_to_string
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View
from .models import Post, Subscriber, Category, User
from .filters import PostFilter
from .forms import *
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .tasks import hello





class Index(View):
    def get(self, request):
        hello.delay()
        return HttpResponse('Привет')

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

        selected_category = self.request.GET.get('category', False)
        context['selected_category'] = self.request.GET.get('category', False)

        context['is_authenticated'] = self.request.user.is_authenticated

        context['is_not_subscriber_of_this_category'] = not Subscriber.objects.filter(user_id=self.request.user.pk,
                                                                                      category__pk=selected_category).exists()
        if selected_category:
            context['name_selected_category'] = Category.objects.get(pk=selected_category)

        return context

    def post(self, request, *args, **kwargs):
        selected_category = self.request.GET.get('category', False)
        category = Category.objects.get(pk=selected_category)

        if not Subscriber.objects.filter(user_id=self.request.user.pk).exists():
            Subscriber.objects.create(user_id=self.request.user.pk)

        subscriber = Subscriber.objects.get(user_id=self.request.user.pk)
        subscriber.category.add(category)

        return HttpResponseRedirect("/posts/")




class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class NewsCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post', 'news.change_post')
    form_class = PostForm
    model = Post
    template_name = 'news_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = 'NEWS'
        return super().form_valid(form)


class NewsEdit(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('news.add_post', 'news.change_post')
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'


class NewsDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('posts')


class ArticleCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post', 'news.change_post')
    form_class = PostForm
    model = Post
    template_name = 'article_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = 'ARTICLE'
        return super().form_valid(form)


class ArticleEdit(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('news.add_post', 'news.change_post')
    model = Post
    template_name = 'article_edit.html'
    form_class = PostForm


class ArticleDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'article_delete.html'
    success_url = reverse_lazy('posts')
