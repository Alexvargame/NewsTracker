# Generated by Django 4.2.5 on 2024-04-23 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0009_remove_comments_date_pub_comments_date_create'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='date_create',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
