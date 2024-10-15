# Generated by Django 4.2.5 on 2024-04-21 11:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('news', '0005_newsthemes_slug'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tag',
            options={'ordering': ['title'], 'verbose_name': 'Тэг', 'verbose_name_plural': 'Тэги'},
        ),
        migrations.AlterField(
            model_name='news',
            name='date_updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Имя')),
                ('text', models.TextField(blank=True, null=True)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_comments', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('news', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='news_comments', to='news.news', verbose_name='Новость')),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='news.comments')),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарии',
            },
        ),
    ]