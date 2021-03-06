from django.http import HttpResponse
from django.shortcuts import render

import os
import logging
from django.conf import settings

from app.serializer import UserSerializer, UserSerializerWithToken
from rest_framework import viewsets, mixins, permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User

# Create your views here.


@api_view(['GET'])
def current_user(request):
    """
    Determine the current user by their token, and return their data
    """

    serializer = UserSerializer(request.user)
    print(serializer.data)
    return Response(serializer.data)


class CreateUser(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = UserSerializerWithToken(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserList(APIView):
    permission_classes = (permissions.AllowAny,)


def get(self, request, format=None):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


def post(self, request, format=None):
    serializer = UserSerializerWithToken(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED)
    return Response(serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get', 'put', ]


class UserViewSetForCreatingUser(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserSerializerWithToken
    http_method_names = ['post']


index_file_path = os.path.join(settings.REACT_APP_DIR, 'out',
                               'index.html')


def index(request):
    try:
        with open(index_file_path) as f:
            return HttpResponse(f.read())
    except FileNotFoundError:
        logging.exception('Production build of app not found')
        return HttpResponse(
            status=501,
        )
