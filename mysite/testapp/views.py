# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import JsonResponse
from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *

class UserListCreate(APIView):

	
	"""

	List all users and create a single user.
	"""

	#permission_classes = (IsAuthenticated,)
	serializer_class = UserSerializer

	def get(self, request, format=None):
		
		users = User.objects.all()
		user_serializer = UserSerializer(users , many=True)
		return JsonResponse(user_serializer.data, safe=False)

	def post(self, request, format=None):
		username = request.POST.get('username')
		password = request.POST.get('password')
		email = request.POST.get('email')

		if username and password and email:
			try:
				user = User.create_user(username, password, email)
			except Exception as e:
				#serializers.serialize('json',e)
				return JsonResponse({"status": str(e)}, status=status.HTTP_409_CONFLICT, 
																			safe=False)

			user_serializer = UserSerializer(user)
			return JsonResponse(user_serializer.data, safe=False)

		return JsonResponse({"status": "Some Params are missing"}, safe=False)


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
	
	"""

	Get, update and delete a single user.
	"""
	
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)

	queryset = User.objects.all()
	serializer_class = UserSerializer


class FriendList(APIView):

	"""

	List all friends of a given user
	"""

	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)

	def get(self,request, format=None):

		user = request.user
		friends = user.friends.all()
		friends_serializer = FriendSerializer(friends,many=True)

		return JsonResponse(friends_serializer.data,safe=False)


class FriendCreate(APIView):
	
	"""

	Make friends
	"""

	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)

	def post(self, request, friend_id, format=None):

		user = request.user

		try:
			friend = User.objects.get(pk=friend_id)
		except:
			return JsonResponse({"status_message": "Friend not found"}, 
									status=status.HTTP_404_NOT_FOUND)
		try:
			Friend(user=user,friend=friend).save()
		except:
			return JsonResponse({"status_message": "already friend"}, 
								status=status.HTTP_200_OK)
		try:
			Friend(user=friend,friend=user).save()
		except:
			return JsonResponse({"status_message": "already friend"}, 
								status=status.HTTP_200_OK)

		return JsonResponse({"status_message": "Friends made"}, 
									status=status.HTTP_200_OK)

class PostListCreate(APIView):

	"""

	List all posts related to the user and create post for related user
	"""
	
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)

	def get(self, request, format=None):
		
		post_type = request.GET.get('post_type','all')
		user = request.user
		posts = []

		if post_type == 'all':
			posts = Post.objects.filter(user=user)
		elif post_type == 'audio':
			posts = Post.objects.filter(user=user).instance_of(Audio)
		elif post_type == 'video':
			posts = Post.objects.filter(user=user).instance_of(Video)
		elif post_type == 'image':
			posts = Post.objects.filter(user=user).instance_of(Image)

		posts_count = posts.count()
		post_serializer = PostSerializer(posts,many=True)
		resp = {"posts": post_serializer.data , "posts_count": posts_count}
		return JsonResponse(resp,safe=False)

	def post(self, request, format=None):

		caption = request.POST.get('caption')
		file_type = request.POST.get('file_type')
		file = request.data['file']
		user = request.user

		if file_type == 'audio':
			Audio(caption=caption, user=user, audio_file=file).save()
		elif file_type == 'video':
			Video(caption=caption, user=user, video_file=file).save()
		elif file_type == 'image':
			Image(caption=caption, user=user, image_file=file).save()

		return JsonResponse({"status_message": "file saved"}, 
									status=status.HTTP_200_OK)

class CommentListCreate(APIView):

	"""

	List all comments of the related post and do comments on the related post.
	"""

	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)

	def get(self, request, post_id, format=None):
		
		try:
			post = Post.objects.get(pk=post_id)
		except:
			return JsonResponse({"status_message": "Post not found"}, 
									status=status.HTTP_404_NOT_FOUND)

		comments = post.comment_set.all()
		comment_serializer = CommentSerializer(comments,many=True)

		return JsonResponse(comment_serializer.data, safe=False, 
										status=status.HTTP_200_OK)

	def post(self, request, post_id, format=None):

		user = request.user
		comment = request.POST.get('comment')
		
		try:
			post = Post.objects.get(pk=post_id)
		except:
			return JsonResponse({"status": "post not found"}, 
							status=status.HTTP_404_NOT_FOUND)

		comment = Comment(user=user,post=post, comment=comment)
		comment.save()
		comment_serializer = CommentSerializer(comment)

		return JsonResponse(comment_serializer.data, safe=False, 
										status=status.HTTP_200_OK)

class LikeListCreate(APIView):

	"""

	like a related post and list all its likes.
	"""

	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)

	def get(self, request, post_id, format=None):
		
		try:
			post = Post.objects.get(pk=post_id)
		except:
			return JsonResponse({"status_message": "Post not found"}, 
									status=status.HTTP_404_NOT_FOUND)

		likes = post.like_set.all()
		like_serializer = LikeSerializer(likes,many=True)

		return JsonResponse(like_serializer.data,safe=False, 
								status=status.HTTP_200_OK)

	def post(self, request, post_id, format=None):

		user = request.user
		try:
			post = Post.objects.get(pk=post_id)
		except:
			return JsonResponse({"status": "post not found"}, 
							status=status.HTTP_404_NOT_FOUND)

		try:
			like = Like(user=user,post=post)
			like.save()
		except Exception as e:
			return JsonResponse({"status": str(e)}, status=status.HTTP_409_CONFLICT,
																		 safe=False)
		like_serializer = LikeSerializer(like)

		return JsonResponse(like_serializer.data, safe=False, 
										status=status.HTTP_200_OK)