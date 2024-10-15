from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import NewsThemes, Tag, News, Comments

@admin.register(NewsThemes)
class NewsThemesAdmin(MPTTModelAdmin):
    list_display = ['id','name','parent','slug']
    save_as = True
    save_on_top = True

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'slug')

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'theme', 'title', 'slug', 'get_tags', 'date_pub', 'date_updated')

@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'name','parent','text', 'news','date_create')
    sortable_by = ['date_create']