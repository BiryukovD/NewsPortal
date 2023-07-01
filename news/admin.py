from django.contrib import admin
from .models import *
from modeltranslation.admin import TranslationAdmin  # импортируем модель амдинки (вспоминаем модуль про переопределение стандартных админ-инструментов)


# Register your models here.

# Регистрируем модели для перевода в админке

class CategoryAdmin(TranslationAdmin):
    model = Category


class PostAdmin(TranslationAdmin):
    model = Post


admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Author)
admin.site.register(Comment)
admin.site.register(PostCategory)
admin.site.register(Subscriber)


# Register your models here.


