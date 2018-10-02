from django.contrib.auth import get_user_model
from django.http import HttpResponse, JsonResponse
from rest_framework import status, viewsets, serializers
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from system.models import Contact, Todo, Item
from system.serializer import SignupSerializer, ContactSerializer, \
    TodoSerializer, ItemSerializer


User = get_user_model()


class SignupAPI(APIView):
    serializer_class = SignupSerializer
    status = status.HTTP_400_BAD_REQUEST
    data = None

    def post(self, request, format=None, pk=None):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            self.status = status.HTTP_201_CREATED
            self.data = serializer.data
        else:
            self.data = serializer.errors
        return Response(self.data, status=self.status)


# class Todo_List(APIView):
#     serializer_class = SignupSerializer
#
#     def get(self, request, format=None, pk=None):
#         queryset = Todo.objects.for_user(request.user)
#         serializer = TodoSerializer(queryset, many=True)
#         return Response(serializer.data)
#
# def todos_list(request):
#     queryset = Todo.objects.for_user(request.user)
#     serializer = TodoSerializer(queryset, many=True)
#     return JsonResponse(data)



class ContactViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = ContactSerializer

    def get_queryset(self):
        return Contact.objects.for_user(self.request.user)

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return super().get_serializer(*args, **kwargs)


class TodoViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = TodoSerializer

    def get_queryset(self):
        return Todo.objects.for_user(self.request.user)


class ItemViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = ItemSerializer


    def create(self, request):
        todo_pk = request.query_params.get("todo_pk")
        if not todo_pk:
            todo_pk = request.data.get("todo_pk")
        else:
            raise serializers.ValidationError("Missing todo_pk")
        serializer =  self.get_serializer(data=request.data,
                                              context={"todo_pk": todo_pk})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    def retrieve(self, request, pk=None):
        item = get_object_or_404(Item, pk=pk)
        serializer = ItemSerializer(item)
        return Response(serializer.data)


    def get_queryset(self):
        todo_pk = self.request.query_params.get("todo_pk")
        if todo_pk:
            queryset = Item.objects.filter(todo=todo_pk)
            return queryset