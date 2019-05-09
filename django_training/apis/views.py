from pprint import pprint

from rest_framework import generics, permissions

from apis.permissions import IsOwnerOrReadOnly
from blogs.models import Blog
from blogs.serializers import BlogSerializer


class BlogList(generics.ListAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

    def list(self, request, *args, **kwargs):
        pprint(kwargs)
        response = super(BlogList, self).list(request, *args, **kwargs)

        return response
    # def get_serializer_context(self):
    #     context = super().get_serializer_context()
    #     context['can_edit'] = True
    #
    #     for v in context['view']:
    #         pprint(v)
    #     return context


class CreateBlog(generics.CreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = (permissions.IsAuthenticated, )


class BlogDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = (IsOwnerOrReadOnly,)
