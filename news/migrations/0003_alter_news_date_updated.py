# Generated by Django 4.2.5 on 2024-04-19 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_tag_alter_newsthemes_options_news'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='date_updated',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]