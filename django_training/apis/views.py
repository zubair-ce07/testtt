from pprint import pprint

from rest_framework import generics, permissions

from apis.permissions import IsOwnerOrReadOnly
from blogs.models import Blog
from blogs.serializers import BlogSerializer


class BlogList(generics.ListAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

    def list(self, request, *args, **kwargs):
        response = super(BlogList, self).list(request, *args, **kwargs)

        for d in response.data:
            d['is_owner'] = d['user_id'] == request.user.id

        return response


class CreateBlog(generics.CreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = (permissions.IsAuthenticated, )


class BlogDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = (IsOwnerOrReadOnly,)
