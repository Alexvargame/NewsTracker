from rest_framework import serializers

from .models import NewsThemes, News, Tag, Comments

class NewsThemesSerializer(serializers.ModelSerializer):
    parent = serializers.SlugRelatedField(slug_field='name', read_only=True)
    class Meta:
        model = NewsThemes
        fields = ('name','parent')


class NewsThemesCreateSerializer(serializers.ModelSerializer):
    #parent = serializers.SlugRelatedField(slug_field='name', read_only=True)
    class Meta:
        model = NewsThemes
        fields = ('name','parent')

    def create(self, validated_data):
        new=NewsThemes.objects.update_or_create(
            name = validated_data.get('name',None),
            parent = validated_data.get('parent',None)
        )
        return new

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ('author', 'theme', 'title', 'slug', 'tags', 'body', 'date_pub')

class NewsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ('author', 'theme', 'title', 'slug', 'tags', 'body')

class CommentsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ('author','name','parent','text')

class TagSerializer(serializers.ModelSerializer):
    class Meta: Tag
    fields = ('id','title', 'slug')