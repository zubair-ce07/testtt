from .serializers import *
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import permissions, generics


@api_view(['GET'])
def get_current_user(request):
    serializer = UserSerializerWithToken(request.user)
    # profile_serializer = ProfileSerializer(user)
    return Response(serializer.data)


class CreateUserView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        user = request.data.get('user')
        user['profile'] = {}
        if not user:
            return Response({'status': False, 'message': 'No data found'})
        serializer = UserSerializerWithToken(data=user)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response({'status': False, "message": serializer.errors})

        return Response({'status': True, "message": "user created Successfully"})


class UpdateUserView(APIView):
    # permission_classes = (permissions.IsAuthenticated,)

    def put(self, request):
        user_data = request.data

        serializer_data = {
            'username': user_data.get('username', request.user.username),

            'profile': {
                'bio': user_data.get('bio', request.user.profile.bio),
                'image': user_data.get('image')
            }
        }

        serializer = UserSerializerWithToken(request.user, data=serializer_data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'status': True, "data": serializer.data,
                         "message": "Profile Updated Successfully"})


class PostView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        posts = Post.objects.filter().order_by('-updated_at')
        serializer = PostListSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request):
        post = request.data
        post['author'] = request.user.id
        serializer = PostSerializer(data=post, context={"request": request})
        if serializer.is_valid():
            serializer.save()
        else:
            return Response({'status': False, "message": serializer.errors})

        return Response({'status': True, "data": PostListSerializer(Post.objects.get(pk=serializer.data['id'])).data,
                         "message": "Post Created Successfully"})

    def put(self, request, pk):
        post = request.data
        instance = Post.objects.get(pk=pk)
        post['author'] = request.user.id
        serializer = PostSerializer(instance, data=post, context={"request": request})
        if serializer.is_valid():
            saved_user = serializer.save()
        else:
            return Response({'status': False, "message": serializer.errors})

        return Response({'status': True, "data": PostListSerializer(Post.objects.get(pk=serializer.data['id'])).data,
                         "message": "Post Updated Successfully"})

    def delete(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        post.delete()
        return Response({'status': True, "data": {"id": pk},
                         "message": "Post Deleted Successfully"})


class CommentView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        comments = Post.objects.filter(
            post=request.query_params.get('post'),
        )
        serializer = CommentListSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request):
        comment = request.data
        comment['author'] = request.user.id
        serializer = CommentSerializer(data=comment, context={"request": request})
        if serializer.is_valid():
            serializer.save()
        else:
            return Response({'status': False, "message": serializer.errors})

        return Response({'status': True,
                         "data": CommentListSerializer(Comment.objects.get(pk=serializer.data['id'])).data,
                         "message": "Comment Created Successfully"})

    def put(self, request, pk):
        comment = request.data
        comment['author'] = request.user.id
        instance = Comment.objects.get(pk=pk)
        serializer = CommentSerializer(instance, data=comment, context={"request": request})
        if serializer.is_valid():
            serializer.save()
        else:
            return Response({'status': False, "message": serializer.errors})

        return Response({'status': True,
                         "data": CommentListSerializer(Comment.objects.get(pk=serializer.data['id'])).data,
                         "message": "Comment Updated Successfully"})

    def delete(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        comment.delete()
        return Response({'status': True, "data": {"id": pk, "post": CommentSerializer(comment).data['post']},
                         "message": "Comment Deleted Successfully"})
