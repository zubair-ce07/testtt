from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):

	class Meta:
		model = User
		fields = ('id', 'username', 'email')


class FriendSerializer(serializers.ModelSerializer):
	
	user = UserSerializer('user')
	
	class Meta:
		model = Friend
		fields = ('user',)

class VideoSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = Video
		fields = ('id', 'video_file')

class AudioSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = Audio
		fields = ('id', 'audio_file')

class ImageSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = Image
		fields = ('id', 'image_file')

class PostSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = Post
		fields = ('caption',)


	def to_representation(self,obj):
		
		ret = super(PostSerializer,self).to_representation(obj)

		if isinstance(obj,Audio):
			ret["audio_file"] = obj.audio_file.url
		elif isinstance(obj,Video):
			ret["video_file"] = obj.video_file.url
		elif isinstance(obj,Video):
			ret["image_file"] = obj.image_file.url

		ret["posted_at"] = str(obj.posted_at)
		
		return ret

class LikeSerializer(serializers.ModelSerializer):	
	
	class Meta:
		model = Like
		fields = ('id', 'post', 'user')

class CommentSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = Comment
		fields = ('id', 'comment', 'user', 'post')