from django import template
from ..models import NewsThemes, News, Comments
#from django.contrib.auth.models import User
from ..queue import get_theme_children
#from users.model import User

register=template.Library()

@register.simple_tag
def total_news():
    return News.objects.count()
#
# @register.simple_tag
# def total_addmoneys():
#     return AddMoney.objects.count()

# def get_all_categories():
#     return Category.objects.all()
#
# @register.simple_tag()
# def get_list_categories():
#     return get_all_categories()

@register.inclusion_tag('news/include/news_themes_menu.html')
def show_news_themes_menu():
    news_themes = NewsThemes.objects.all()
    return {'news_themes':news_themes}

@register.inclusion_tag('news/include/comments_to_news.html')
def show_comments_to_news(pk):
    news = News.objects.get(id=pk)
    comments = Comments.objects.filter(news=news)
    return {'comments':comments}

@register.inclusion_tag('news/news_themes_menu_children.html')
def show_news_themes_menu_children(pk):
    news_themes_children = NewsThemes.objects.filter(parent=NewsThemes.objects.get(id=pk))
    return {'news_themes_children':news_themes_children}


@register.inclusion_tag('news/latest_news_football.html')
def show_latest_news_football(count=5):
    th=NewsThemes.objects.get(name='Футбол')
    latest_news_football = News.objects.filter(theme__in=list(get_theme_children(th))).order_by('-date_pub')[:count]
    return {'latest_news_football': latest_news_football}

@register.inclusion_tag('news/latest_news_hockey.html')
def show_latest_news_hockey(count=5):
    th = NewsThemes.objects.get(name='Хоккей')
    latest_news_hockey = News.objects.filter(theme__in=list(get_theme_children(th))).order_by('-date_pub')[:count]
    return {'latest_news_hockey': latest_news_hockey}