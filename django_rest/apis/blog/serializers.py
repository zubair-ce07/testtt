from rest_framework import serializers

from rest_framework_recursive.fields import RecursiveField

from .models import Blog, Tag, Comment


class TagSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return Tag.objects.get_or_create(**validated_data)[0]

    class Meta:
        model = Tag
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    writer = serializers.ReadOnlyField(source='writer.get_full_name')
    comments = RecursiveField(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'


class BlogSerializer(serializers.ModelSerializer):
    writer = serializers.ReadOnlyField(source='writer.id')
    tags = TagSerializer(many=True)
    # comments = CommentSerializer(many=True, read_only=True)

    def create(self, validated_data):
        tags = [Tag.objects.get_or_create(
            **tag)[0].id for tag in validated_data.pop('tags', [])]

        blog = Blog(**validated_data)
        blog.save()
        blog.tags.add(*tags)
        return blog

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.body = validated_data.get('body', instance.body)
        instance.save()

        if validated_data.get('tags', None):
            existing_tags = set(instance.tags.values_list('id', flat=True))
            new_tags = set([Tag.objects.get_or_create(
                **tag)[0].id for tag in validated_data.pop('tags', [])])

            tags_to_remove = existing_tags - new_tags
            tags_to_add = new_tags - existing_tags

            instance.tags.remove(*tags_to_remove)
            instance.tags.add(*tags_to_add)
        return instance

    class Meta:
        model = Blog
        fields = ('id', 'title', 'body', 'writer',
                  'tags', 'created_at')
