from django.core.exceptions import ObjectDoesNotExist
from django.forms import model_to_dict

import datetime

from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import TodoSerializer, TodoCreateSerializer, TodoListSerializer

from .models import Todo


@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'List': '/task-list/',
        'Detail View': '/task-detail/<str:pk>/',
        'Create': '/task-create/',
        'Update': '/task-update/<str:pk>/',
        'Delete': '/task-delete/<str:pk>/',
    }
    return Response(api_urls)


class TodoCreate(CreateAPIView):
    serializer_class = TodoCreateSerializer
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication


class TodoView(ListAPIView):
    serializer_class = TodoListSerializer
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def get(self, request):
        user_todos = Todo.objects.filter(user=request.user).values().order_by('date_created')

        return Response(user_todos)


class TodoDetail(RetrieveAPIView):
    serializer_class = TodoSerializer
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def get(self, *args, **kwargs):
        user_todo = Todo.objects. \
            filter(user=self.request._user, pk=kwargs['pk']). \
            values(). \
            order_by('date_created')

        if user_todo:
            return Response(user_todo)
        else:
            return Response("Todo not founded!", status=404)


class TodoUpdate(UpdateAPIView):
    serializer_class = TodoSerializer
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def put(self, request, *args, **kwargs):
        try:
            user_todo = Todo.objects. \
                get(user=request._user, pk=kwargs['pk'])

            if request.data.get('title'):
                user_todo.title = request.data['title']
            if request.data.get('body'):
                user_todo.body = request.data['body']
            if request.data.get('completed') is not None:
                user_todo.completed = request.data['completed']
                user_todo.date_completed = datetime.datetime.now() if request.data['completed'] else None

            user_todo.save()

        except ObjectDoesNotExist:
            return Response([], status=404)

        return Response(model_to_dict(user_todo))


class TodoDelete(DestroyAPIView):
    serializer_class = TodoSerializer
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def delete(self, request, *args, **kwargs):
        try:
            user_todo = Todo.objects.filter(user=request._user, pk=kwargs['pk'])

            if user_todo:
                user_todo.delete()
            else:
                return Response("Todo not founded!", status=404)

        except ObjectDoesNotExist:
            return Response("Todo not founded!", status=404)

        return Response("Deleted!")