from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import viewsets

from .serializers import *
from .utils import notify_on_socket


@api_view(['GET'])
def get_current_user(request):
    serializer = UserSerializerWithToken(request.user)
    return Response(serializer.data)


class CreateUserView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        user = request.data.get('user')
        user['profile'] = {}
        if not user:
            return Response({'status': False, 'message': 'No data found'})

        serializer = UserSerializerWithToken(data=user)
        if not serializer.is_valid():
            return Response({'status': False, "message": serializer.errors, }, status=HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response({'status': True, "message": "user created Successfully"})


class UpdateUserView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def put(self, request):
        user_data = request.data

        serializer_data = {
            'username': user_data.get('username', request.user.username),

            'profile': {
                'bio': user_data.get('bio', request.user.profile.bio),
                'image': user_data.get('image', request.user.profile.image)
            }
        }

        serializer = UserSerializerWithToken(request.user, data=serializer_data, partial=True)
        if not serializer.is_valid():
            return Response({'status': False, "message": serializer.errors, }, status=HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response({'status': True, "data": serializer.data, "message": "Profile Updated Successfully"})


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):
        request.data['author'] = request.user.id
        create_res = super().create(request)
        response = {'status': True, "data": self.get_serialized_post(create_res.data['id']),
                    "message": "Post Created Successfully"}

        notify_on_socket("CREATE_POST_FULFILLED", response)
        return Response(response)

    def update(self, request, pk=None):
        if 'author' not in request.data:
            request.data['author'] = request.user.id
        update_res = super().update(request, pk)
        response = {'status': True, "data": self.get_serialized_post(update_res.data['id']),
                    "message": "Post Updated Successfully"}

        notify_on_socket("UPDATE_POST_FULFILLED", response)
        return Response(response)

    def destroy(self, request, pk=None):
        super().destroy(request, pk)

        response = {'status': True, "data": {"id": pk}, "message": "Post Deleted Successfully"}
        notify_on_socket("DELETE_POST_FULFILLED", response)
        return Response(response)

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return PostSerializer

        return PostListSerializer

    def get_serialized_post(self, pk):
        return PostListSerializer(Post.objects.get(pk=pk)).data


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):
        request.data['author'] = request.user.id
        create_res = super().create(request)

        response = {'status': True, "data": self.get_serialized_comment(create_res.data['id']),
                    "message": "Comment Created Successfully"}
        notify_on_socket("CREATE_COMMENT_FULFILLED", response)
        return Response(response)

    def update(self, request, pk=None):
        request.data['author'] = request.user.id
        update_res = super().update(request, pk)

        response = {'status': True, "data": self.get_serialized_comment(update_res.data['id']),
                    "message": "Comment Updated Successfully"}

        notify_on_socket("UPDATE_COMMENT_FULFILLED", response)
        return Response(response)

    def destroy(self, request, pk=None):
        comment = self.get_serialized_comment(pk)
        super().destroy(request, pk)

        response = {'status': True, "data": {"id": pk, "post": comment['post']},
                    "message": "Post Deleted Successfully"}

        notify_on_socket("DELETE_COMMENT_FULFILLED", response)
        return Response(response)

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return CommentSerializer

        return CommentListSerializer

    def get_serialized_comment(self, pk):
        return CommentListSerializer(Comment.objects.get(pk=pk)).data
