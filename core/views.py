from django.shortcuts import render
from .models import *
from .permissions import *
#from .exceptions import *
from .serializers import *
#from .services import *
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from django.views.decorators.csrf import csrf_exempt

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (UserPermission,)

    def list(self, request):
        return Response(UserSerializer(request.user).data)

    def get_queryset(self):
        return self.queryset.filter(pk=self.request.user.id)

    def retrieve(self, request, pk):
        user = User.objects.get(pk=pk)
        if request.user == user:
            return Response(UserSerializer(user, context={'request': request}).data)
        else:
            return Response(UserSerializer(user, context={'request': request}).data)