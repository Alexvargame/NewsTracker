# Generated by Django 4.2.5 on 2024-04-23 10:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0007_alter_comments_text_alter_news_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='date_pub',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 23, 13, 43, 52, 651212)),
        ),
    ]