import datetime

from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User
from django.utils.text import slugify

from mptt.models import MPTTModel, TreeForeignKey

from .add_materials import dict_slug,slovar

class NewsThemes(MPTTModel):
    name = models.CharField(verbose_name='Тема', max_length=100)
    parent = TreeForeignKey('self',
                            related_name='children',
                            on_delete=models.SET_NULL,
                            null=True,
                            blank=True)
    slug = models.SlugField(max_length=50,default='')
    class MPTTMeta:
        order_insertion_by=['name']

    class Meta:
        verbose_name='Тема новости'
        verbose_name_plural='Темы новостей'

    def __str__(self):
        if self.parent==None:
            return f"{self.name}"
        return f'{self.parent} - {self.name}'

    def get_absolute_url(self):
        return reverse('news_theme_detail_url', kwargs={'pk':self.id})
    def get_update_url(self):
        return reverse('news_theme_update_url', kwargs={'pk':self.id})
    def get_delete_url(self):
        return reverse('news_theme_delete_url', kwargs={'pk':self.id})

    def create_slug(self):
        output=''
        a=self.__str__()
        a_lst=[aa.lower().strip() for aa in a.split('-')]
        for th in a_lst:
            if len(th.split())==1:
                if  th in dict_slug.keys():
                    output+=dict_slug[th]
                    output += '_'
                else:
                    dict_slug[th] = th.translate(str.maketrans(slovar))
                    output += dict_slug[th]
                    output += '_'
            else:
                for thh in th.split():
                    if thh in dict_slug.keys():
                        output += dict_slug[thh]
                        output += '_'
                    else:
                        dict_slug[thh]=thh.translate(str.maketrans(slovar))
                        output += dict_slug[thh]
                        output +='_'
        return output.strip('_')


class News(models.Model):

    author = models.ForeignKey(User, related_name='author_news', on_delete=models.DO_NOTHING)
    theme = models.ForeignKey(NewsThemes, related_name='news_themes', on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length= 100, blank= True, null=True)
    tags = models.ManyToManyField('Tag', related_name='news_tags', blank=True)
    body = models.TextField()
    date_pub = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-date_pub']

    def __str__(self):
        return self.title

    def get_tags(self):
        return [tag.slug for tag in self.tags.all()]

    def get_absolute_url(self):
        return reverse('new_detail_url', kwargs={'pk':self.id})
    def get_update_url(self):
        return reverse('new_update_url', kwargs={'pk':self.id})
    def get_delete_url(self):
        return reverse('new_delete_url', kwargs={'pk':self.id})
    def read_all_url(self):
        return reverse('new_read_all_url', kwargs={'pk':self.id})
    # def get_news_for_author(self):
    #     return


class Tag(models.Model):
    title=models.CharField(max_length=50)
    slug=models.SlugField(max_length=50, unique=True)

    def __str__(self):
            return '{}'.format(self.title)
    # def get_absolute_url(self):
    #         return reverse('tag_detail_url', kwargs={'slug':self.slug})
    # def get_update_url(self):
    #         return reverse('tag_update_url', kwargs={'slug':self.slug})
    # def get_delete_url(self):
    #         return reverse('tag_delete_url', kwargs={'slug':self.slug})
    class Meta:
        ordering=['title']
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'


class Comments(MPTTModel):
    author = models.ForeignKey(User, related_name='user_comments', on_delete=models.DO_NOTHING, verbose_name= 'Автор')
    name = models.CharField("Имя", max_length=100)
    news = models.ForeignKey(News, related_name='news_comments', on_delete=models.CASCADE, verbose_name='Новость')
    text = models.TextField("Текст",blank=True, null=True)
    date_create = models.DateTimeField(auto_now_add=True)
    parent = TreeForeignKey('self',
                            related_name='children',
                            on_delete=models.SET_NULL,
                            null=True,
                            blank=True)

    class MPTTMeta:
        order_insertion_by=['author']

    class Meta:
        verbose_name='Комментарий'
        verbose_name_plural='Комментарии'

    def __str__(self):
        return f"{self.news}-{self.name}"
    #
    # def get_absolute_url(self):
    #     return reverse('news_theme_detail_url', kwargs={'pk':self.id})
    # def get_update_url(self):
    #     return reverse('news_theme_update_url', kwargs={'pk':self.id})
    # def get_delete_url(self):
    #     return reverse('news_theme_delete_url', kwargs={'pk':self.id})