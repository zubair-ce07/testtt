# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import JsonResponse
from django.db.models import Q
from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .models import *
from .serializers import *



class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({'token': token.key, 'id': token.user_id})

class UserList(APIView):

	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)

	def get(self, request, format=None):
		
		user = request.user


		users = User.objects.all().exclude(pk=user.id)
 
		user_serializer = UserSerializer(users , many=True)
		users_data = user_serializer.data

		friends_ids = user.friends.all().values_list("user_id", flat=True)
		print(friends_ids)
		for u in users_data:
			if u["id"] in friends_ids:
				u["is_friend"] = True
			else:
				u["is_friend"] = False

		return JsonResponse(users_data, safe=False)

class UserCreate(APIView):

	
	"""

	List all users and create a single user.
	"""

	#permission_classes = (IsAuthenticated,)
	serializer_class = UserSerializer


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


class UserDetail(APIView):
	
	"""

	Get, update and delete a single user.
	"""
	
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)

	def get(self, request, user_id, format=None):

		user = request.user
		if(user_id == "self"):
			user_serializer = UserSerializer(user)
			return JsonResponse(user_serializer.data,safe=False)

		try:
			user2 = User.objects.get(pk=user_id)
		except:
			return JsonResponse({"status_message": "User not found"}, 
									status=status.HTTP_404_NOT_FOUND)

		user_serializer = UserSerializer(user2)
		user_data = user_serializer.data
		
		friends_ids = user.friends.all().values_list("user_id",flat=True)
		
		if user2.id in friends_ids:
			user_data["is_friend"] = True
		else:
			user_data["is_friend"] = False

		return JsonResponse(user_data,safe=False)




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
		user_serializer = UserSerializer(friend)
		return JsonResponse({"user": user_serializer.data}, 
							status=status.HTTP_200_OK)

class UpdatePost(APIView):

	"""
	Updates a post.
	"""

	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)

	def post(self, request, format=None):

		user = request.user
		print(request)

		privacy = request.POST.get('privacy')
		post_id = request.POST.get('post_id')

		if privacy not in ("public","friends","only_me"):
			return JsonResponse({"error": "privacy setting is invalid."},
							status=status.HTTP_400_BAD_REQUEST,safe=False,)
		

		try:
			post = Post.objects.get(pk=post_id)
		except:
			return JsonResponse({"status_message": "Post not found"}, 
									status=status.HTTP_404_NOT_FOUND)


		post.privacy = privacy
		post.save()

		post_serializer = PostSerializer(post)

		return JsonResponse({post_id: post_serializer.data},safe=False)



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
		friend_posts = []

		friend_ids = user.friends.all().values_list('user_id', flat=True)

		if post_type == 'all':
			posts = Post.objects.filter(Q(user=user) | Q(user__in=friend_ids, privacy__in=("public","friends"))).order_by("-posted_at")
		elif post_type == 'audio':
			posts = Post.objects.filter(Q(user=user) | Q(user__in=friend_ids, privacy__in=("public","friends"))).instance_of(Audio).order_by("-posted_at")
		elif post_type == 'video':
			posts = Post.objects.filter(Q(user=user) | Q(user__in=friend_ids, privacy__in=("public","friends"))).instance_of(Video).order_by("-posted_at")
		elif post_type == 'image':
			posts = Post.objects.filter(Q(user=user) | Q(user__in=friend_ids, privacy__in=("public","friends"))).instance_of(Image).order_by("-posted_at")

		posts_count = posts.count()
		post_serializer = PostSerializer(posts,many=True)
		posts_data = post_serializer.data

		user_like_post_ids = user.like_set.all().values_list('post_id',flat=True)
		#user_post_ids = user.post_set.all().values_list("id",flat=True)

		for post in posts_data:
			if post["id"] in user_like_post_ids:
				post["is_liked"] = True
			else:
				post["is_liked"] = False




		resp = {"posts": posts_data , "posts_count": posts_count}
		return JsonResponse(resp,safe=False)

	


	def post(self, request, format=None):

		caption = request.POST.get('caption')
		file_type = request.POST.get('file_type')
		file = request.FILES.get('file')
		privacy = request.POST.get('privacy')
		print("here")
		if privacy not in ("public","friends","only_me"):
			return JsonResponse({"error": "privacy setting is invalid."},
							status=status.HTTP_400_BAD_REQUEST,safe=False,)

		user = request.user
		post = None
		if file_type == 'audio':
			post = Audio(caption=caption, user=user, audio_file=file, privacy=privacy)
			post.save()
			post = Post.objects.get(Q(Audio___id=post.id))
		elif file_type == 'video':
			post = Video(caption=caption, user=user, video_file=file, privacy=privacy)
			post.save()
			post = Post.objects.get(Q(Video___id=post.id))
		elif file_type == 'image':
			post = Image(caption=caption, user=user, image_file=file, privacy=privacy)
			post.save()
			post = Post.objects.get(Q(Image___id=post.id))

		post_serializer = PostSerializer(post)
		return JsonResponse({"post": post_serializer.data}, 
									safe=False)

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

		commentsByPost = {post_id: comment_serializer.data}

		return JsonResponse(commentsByPost, safe=False, 
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

		return JsonResponse({post_id: comment_serializer.data}, safe=False, 
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

		return JsonResponse({post_id: like_serializer.data},safe=False, 
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

		return JsonResponse({post_id: like_serializer.data}, safe=False, 
										status=status.HTTP_200_OK)