from django.urls import path
from .views import *

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'api_news_themes', NewsThemesViewSet, basename='api_news_themes')
router_news = DefaultRouter()
router_news.register(r'api_news',NewsModelViewSet, basename='api_news')

urlpatterns = [
        path('',main_page,name='main_page_url'),
        path('<str:slug>/', NewsTableView.as_view(), name='news_table_url'),
        path('news_themes/',NewsThemesListView.as_view(), name='news_themes_list_url'),
        path('news_themes/create/',NewsThemeCreateView.as_view(), name='news_theme_create_url'),
        path('news_themes/<int:pk>/update/',NewsThemeUpdateView.as_view(), name='news_theme_update_url'),
        path('news_themes/<int:pk>/delete/',NewsThemeDeleteView.as_view(), name='news_theme_delete_url'),
        path('news_themes/<int:pk>/',NewsThemeDetailView.as_view(), name='news_theme_detail_url'),

        path('news/',NewsListView.as_view(), name='news_list_url'),
        path('news/create/',NewCreateView.as_view(), name='new_create_url'),
        path('news/<int:pk>/update/',NewUpdateView.as_view(), name='new_update_url'),
        path('news/<int:pk>/delete/',NewDeleteView.as_view(), name='new_delete_url'),
        path('news/<int:pk>/',NewDetailView.as_view(), name='new_detail_url'),
        path('news/<int:pk>/read_all/',NewReadAllView.as_view(), name='new_read_all_url'),
        path('news/<int:pk>/add_comments/',CommentsCreateView.as_view(), name='add_comments_url'),
        path('news/user/<slug:username>/',NewsForAuthorView.as_view(), name='news_author_url'),
        path('comments/user/<slug:username>/',CommentsForAuthorView.as_view(), name='comments_author_url'),

        path('news/update/football/', FootbalNewsParseView.as_view(), name='football_news_update_url'),
        path('news/update/hockey/', HockeyNewsParseView.as_view(), name='hockey_news_update_url'),
        path('tags/<int:pkk>/news/',NewsForTagListView.as_view(),name='news_tags_list_url'),

]

#print('routes',router.urls)
# print('routes_n',router_news.urls)
# print(router_news.routes)
urlpatterns += router.urls
urlpatterns += router_news.urls