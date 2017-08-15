from rest_framework import status
from django.views.generic import TemplateView
from user.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from blog.models import Blog
from blog.serializers import BlogSerializer
from comment.models import Comment
from comment.serializers import CommentSerializer
from django.shortcuts import get_object_or_404
from django.utils.text import slugify
from rest_framework import permissions

"""
    This view returns blog list and create new blog on GET and POST request respectively.
"""


class APIBlogList(APIView):

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request, format=None):
        return Response(BlogSerializer(Blog.objects.filter(is_published=True, is_public=True), many=True).data,
                        status=status.HTTP_200_OK)

    def post(self, request, format=None):
        form_data = request.POST.copy()
        form_data.update({'slug': slugify(request.data.get('title')), 'created_by': request.user})
        serializer = BlogSerializer(data=form_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class APIUserAllBlogList(APIView):

    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, username, format=None):
        return Response(BlogSerializer(Blog.objects.filter(created_by=User.objects.get(username=username)),
                                       many=True).data, status=status.HTTP_200_OK)


"""
    This view handles the detail, updating and deletion of Blogs based on slug.
"""


class APIBlogDetailUpdateDelete(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, slug, format=None):
        blog = get_object_or_404(Blog, slug=slug)
        comments = CommentSerializer(Comment.objects.filter(comment_for=blog), many=True)
        return Response({'blog': BlogSerializer(blog).data, 'comments': comments.data}, status=status.HTTP_200_OK)

    def put(self, request, slug, format=None):
        blog = Blog.objects.get(slug=slug)
        serializer = BlogSerializer(instance=blog, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, slug, format=None):
        blog = get_object_or_404(Blog, slug=slug)
        blog.delete()
        return Response(status=status.HTTP_200_OK)


class BlogDetail(TemplateView):

    template_name = 'blog/single.html'

    def get_context_data(self, **kwargs):
        print (self.kwargs['slug'])
        return {'slug': self.kwargs['slug']}
