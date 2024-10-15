import os.path
import subprocess

from django.shortcuts import render,redirect, reverse
from django.core.management import call_command
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet,ModelViewSet
from rest_framework.renderers import TemplateHTMLRenderer

from django.contrib.auth.mixins import LoginRequiredMixin

from .models import NewsThemes, News, Tag, Comments
from .add_materials import slovar
from .utils import (ObjectCreateMixin,ObjectListMixin,
                    ObjectDeleteMixin, ObjectDetailMixin,
                    ObjectUpdateMixin, ViewModelSetMixin)
from .serializers import (NewsThemesSerializer,NewsThemesCreateSerializer,
                           NewsSerializer, NewsCreateSerializer,
                           CommentsCreateSerializer,TagSerializer)
from .queue import get_theme_children

from django.contrib.auth.models import User

import json
import io

from news.news_scrap.settings import BASE_DIR as BASE_DIR_SCRAPY
from news_tracker.settings import BASE_DIR as BASE_DIR_TRACKER
# from transliterate import translit, get_available_language_codes
# from googletrans import Translator
# from news.news_scrap import craw_runner
#
# def task():
#     call_command(command_name=craw_runner)
def main_page(request):
    print('RGRRRRRRRRRR')
    #t=task()
    #print('T',t)
    return render(request, 'news/main_page.html')

class NewsThemesViewSet(LoginRequiredMixin,ViewModelSetMixin,ModelViewSet):
    serializer = NewsThemesSerializer
    serializer_create = NewsThemesCreateSerializer
    template = None
    template_name = None
    template_detail= None
    model = NewsThemes

class NewsModelViewSet(LoginRequiredMixin,ViewModelSetMixin,ModelViewSet):
    # renderer_classes = [TemplateHTMLRenderer]
    serializer = NewsSerializer
    serializer_create = NewsCreateSerializer
    model = News
    # template_name = None
    # template_dict = {
    #     'list':'news/news_list.html',
    #     'retrieve': 'news/new_detail.html',
    #     'create':'news/new_create.html',
    #     'update':'',
    #     'delete':''
    # }

class NewsThemesListView(LoginRequiredMixin,ObjectListMixin,APIView):
    renderer_classes = [TemplateHTMLRenderer]
    serializer = NewsThemesSerializer
    template_name = 'news/themes_list.html'
    model = NewsThemes

class NewsThemeCreateView(LoginRequiredMixin,ObjectCreateMixin,APIView):
    renderer_classes = [TemplateHTMLRenderer]
    serializer = NewsThemesCreateSerializer
    template = 'news_themes_list_url'
    template_name = 'news/news_theme_create.html'
    model = NewsThemes

class NewsThemeUpdateView(LoginRequiredMixin,ObjectUpdateMixin,APIView):
    renderer_classes = [TemplateHTMLRenderer]
    serializer = NewsThemesCreateSerializer
    template = 'news_themes_list_url'
    template_name = 'news/news_theme_update.html'
    model = NewsThemes


class NewsThemeDetailView(LoginRequiredMixin,ObjectDetailMixin,APIView):
    renderer_classes = [TemplateHTMLRenderer]
    serializer = NewsThemesSerializer
    template_name = 'news/news_theme_detail.html'
    model = NewsThemes

class NewsThemeDeleteView(LoginRequiredMixin,ObjectDeleteMixin,APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template = 'news_themes_list_url'
    template_name = 'news/news_theme_delete.html'
    model = NewsThemes

class NewsListView(LoginRequiredMixin,ObjectListMixin,APIView):
    renderer_classes = [TemplateHTMLRenderer]
    serializer = NewsSerializer
    template_name = 'news/news_list.html'
    model = News

class NewCreateView(LoginRequiredMixin,ObjectCreateMixin,APIView):
    renderer_classes = [TemplateHTMLRenderer]
    serializer = NewsCreateSerializer
    template = 'news_list_url'
    template_name = 'news/new_create.html'
    model = News

class NewUpdateView(LoginRequiredMixin,ObjectUpdateMixin,APIView):
    renderer_classes = [TemplateHTMLRenderer]
    serializer = NewsCreateSerializer
    template = 'news_list_url'
    template_name = 'news/new_update.html'
    model = News


class NewDetailView(LoginRequiredMixin,ObjectDetailMixin,APIView):
    renderer_classes = [TemplateHTMLRenderer]
    serializer = NewsSerializer
    template_name = 'news/new_detail.html'
    model = News

class NewDeleteView(LoginRequiredMixin,ObjectDeleteMixin,APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template = 'news_list_url'
    template_name = 'news/new_delete.html'
    model = News

class NewsTableView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'news/news_table.html'
    serializer = NewsSerializer
    model = News
    def get(self,request,slug=all):
        if slug not in ['all','news']:
            theme=NewsThemes.objects.get(slug=slug)
            themes_id = list(get_theme_children(theme))
            news=News.objects.filter(theme__in=themes_id)
        else:
            news=News.objects.all()[:5]
        serializer=NewsSerializer(news,many=True)
        return Response({'serializer':serializer,'news':news})

class NewsForAuthorView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'news/news_author.html'
    def get(self, request,username):
        user = User.objects.get(username=username)
        news = user.author_news.all()
        serializer = NewsSerializer(news, many=True)
        return Response({'news': news})

class CommentsForAuthorView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'news/comments_author.html'
    def get(self, request,username):
        user = User.objects.get(username=username)
        comments = user.user_comments.all()
        serializer = CommentsCreateSerializer(comments, many=True)
        return Response({'comments': comments, 'author': user})
class NewReadAllView(ObjectDetailMixin,APIView):
    renderer_classes = [TemplateHTMLRenderer]
    serializer = NewsSerializer
    serializer_comments = CommentsCreateSerializer
    template_name = 'news/new_read_all.html'
    model = News


class CommentsCreateView(LoginRequiredMixin,APIView):
    renderer_classes = [TemplateHTMLRenderer]
    # serializer = CommentsCreateSerializer
    # template = 'news_list_url'
    template_name = 'news/new_read_all.html'

    def post(self, request, pk):
        serializer = CommentsCreateSerializer(data=request.data)
        news = News.objects.get(id=pk)
        if serializer.is_valid():
            serializer.save(news=news)
            if request.data.get("parent", None):
                serializer.parent = int(request.data.get("parent"))
            serializer.save(news=news)
            news.save()
        return redirect(news.read_all_url())

class FootbalNewsParseView(APIView):
    def get(self,request):
        os.chdir(BASE_DIR_SCRAPY)
        try:
            os.system('{} {}'.format('scrapy runspider', 'footballnewsItems.py -O news.json:json'))
            #r=subprocess.check_output('{} {}'.format('scrapy runspider', 'footballnewsItems.py -O news.json:json'), shell=True)
        except subprocess.CalledProcessError as e:
            output = e.output
        os.chdir(BASE_DIR_TRACKER)
        try:
            with io.open('news/news_scrap/news.json',encoding="utf_8") as f:
                templates = json.load(f)
        except io.BlockingIOError as e:
            output = e.output
        save_news(templates,request.user,"Футбол")
        return render(request, 'news/main_page.html')

class HockeyNewsParseView(APIView):
    def get(self,request):
        os.chdir(BASE_DIR_SCRAPY)
        try:
            os.system('{} {}'.format('scrapy runspider', 'hockeynewsItems.py -O news.json:json'))
            #r=subprocess.check_output('{} {}'.format('scrapy runspider', 'footballnewsItems.py -O news.json:json'), shell=True)
        except subprocess.CalledProcessError as e:
            output = e.output
        os.chdir(BASE_DIR_TRACKER)
        try:
            with io.open('news/news_scrap/news.json',encoding="utf_8") as f:
                templates = json.load(f)
        except io.BlockingIOError as e:
            output = e.output
        save_news(templates,request.user,"Хоккей")
        return render(request, 'news/main_page.html')

def save_news(lst,user,type_sport):
    for l in lst:
        if  NewsThemes.objects.filter(name=l['theme_ch']).exists():
            theme = NewsThemes.objects.get(name=l['theme_ch'])
        elif NewsThemes.objects.filter(name=l['theme']).exists():
            if l['theme_ch']:
                theme = NewsThemes.objects.create(name=l['theme_ch'], parent=NewsThemes.objects.get(name=l['theme']))
                # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! если нет в словаре
                theme.slug = theme.create_slug()
                theme.save()
            else:
                theme = NewsThemes.objects.get(name=l['theme'])
        else:
            new_theme=NewsThemes.objects.create(name=l['theme'],parent=NewsThemes.objects.get(name=type_sport))
            new_theme.slug=new_theme.create_slug()
            new_theme.save()
            theme=NewsThemes.objects.create(name=l['theme_ch'],parent=new_theme)
            #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! если нет в словаре
            print('THEME',theme)
            theme.slug=theme.create_slug()
            theme.save()
        if not News.objects.filter(title=l['title']).exists():
            try:
                new_=News.objects.create(
                    author = user,
                    body = l['body'],
                    title = l['title'],
                    theme = theme,
                    slug = theme.name.lower()
                )
                tags=[th.strip() for th in new_.theme.__str__().split('-')]
                tags_lst=[]
                for tag in tags:
                    if Tag.objects.filter(title=tag).exists():
                        tags_lst.append(Tag.objects.get(title=tag).id)
                    else:
                        new_tag=Tag.objects.create(title=tag,slug=tag.translate(str.maketrans(slovar)))
                        tags_lst.append(new_tag.id)
                new_.tags.set(tags_lst)
                new_.save()

            except Exception as e:
                print('failed at latest_article is none')
                print(e)
                pass

class NewsForTagListView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'news/news_for_tags_list.html'

    def get(self,request,pkk):
        tag = Tag.objects.get(pk=pkk)
        news_tags = tag.news_tags.all()[:20]
        serializer = NewsSerializer(news_tags,many=True)
        return Response({'news_tags': news_tags})



