from django.shortcuts import render
from django.contrib.auth.models import User, Group

from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import permissions

from .serializers import UserSerializer, MenuItemSerializer
from .models import MenuItem
from .permissions import ManagerUser

'''
class GroupApiView(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request):
        managers = User.objects.filter(groups__name = 'Manager')
        serializer = UserSerializer(managers)
        print(dir(serializer))
        return Response(serializer, status=status.HTTP_200_OK)

'''

class MenuItemListCreateApiView(ListCreateAPIView):

    queryset = MenuItem.objects.select_related('category').all()
    serializer_class = MenuItemSerializer

    def get_permissions(self):
        
        if(self.request.method=='POST'):
            return [ManagerUser()]
        else:
            return[]
            
        
class MenuItemUpdateDeleteApiView(RetrieveUpdateDestroyAPIView):

    queryset = MenuItem.objects.select_related('category').all()
    serializer_class = MenuItemSerializer
