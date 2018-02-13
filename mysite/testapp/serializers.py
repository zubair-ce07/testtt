from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
	token = serializers.SerializerMethodField('get_auth_token')

	def get_auth_token(self, user):
		return user.auth_token.key

	class Meta:
		model = User
		fields = ('id', 'username', 'email', 'token')


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
		fields = ('id','caption','privacy','user')


	def to_representation(self,obj):
		
		ret = super(PostSerializer,self).to_representation(obj)

		if isinstance(obj,Audio):
			ret["audio_file"] = obj.audio_file.url
			ret["file_type"] = "audio"
		elif isinstance(obj,Video):
			ret["video_file"] = obj.video_file.url
			ret["file_type"] = "video"
		elif isinstance(obj,Image):
			ret["image_file"] = obj.image_file.url
			ret["file_type"] = "image"

		ret["comments_count"] = obj.comment_set.count()
		ret["likes_count"] = obj.like_set.count()
		ret["posted_at"] = str(obj.posted_at)
		ret ["posted_by"] = obj.user.username

		
		return ret

class LikeSerializer(serializers.ModelSerializer):	
	
	class Meta:
		model = Like
		fields = ('id', 'post', 'user')

	def to_representation(self,obj):
		
		ret = super(LikeSerializer,self).to_representation(obj)

		ret["user"] = UserSerializer(obj.user).data["username"]

		return ret

class CommentSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = Comment
		fields = ('id', 'comment', 'user')

	def to_representation(self,obj):
		
		ret = super(CommentSerializer,self).to_representation(obj)

		ret["user"] = UserSerializer(obj.user).data["username"]

		return ret
