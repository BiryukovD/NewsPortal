from django.urls import path
from .views import PostList, PostListWithFilter, PostDetail, NewsCreate, NewsEdit, NewsDelete, ArticleCreate, ArticleEdit, ArticleDelete



urlpatterns = [

    path('posts/', PostList.as_view(), name='posts'),                        # все статьи
    path('posts/search/', PostListWithFilter.as_view()),                     # поиск
    path('posts/detail/<int:pk>', PostDetail.as_view(), name='post_detail'), # текст статьи


    path('news/create/', NewsCreate.as_view(), name='news_create'),    # создание новости
    path('news/<int:pk>/edit/', NewsEdit.as_view(), name='news_edit'),   # редактирование новости
    path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'), # удаление новости

    path('articles/create/', ArticleCreate.as_view(), name='article_create'),           # создание статьи
    path('articles/<int:pk>/edit/', ArticleEdit.as_view(), name='article_edit'),    # редактирование статьи
    path('articles/<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),  # удаление статьи






]