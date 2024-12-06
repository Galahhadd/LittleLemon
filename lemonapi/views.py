from django.shortcuts import render
from django.contrib.auth.models import User, Group
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, DestroyAPIView
from rest_framework import permissions

from .serializers import UserSerializer, MenuItemSerializer, CartSerializer, OrderSerializer
from .models import MenuItem, Cart, Order, OrderItem
from .permissions import ManagerUser

import datetime




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

    def get_permissions(self):
        if(self.request.method=='GET'):
            return []
        else:
            return[ManagerUser()]
        
class ManagerGroupApiView(APIView):

    permission_classes = [ManagerUser]

    def get(self, request):
        users = User.objects.filter(groups__name = 'Manager')
        serializer = UserSerializer(users, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        try:
            username = request.data['username']
        except KeyError:
            return Response({"message" : "You didn't provide proper data"}, status=status.HTTP_400_BAD_REQUEST)
        
        user = get_object_or_404(User, username=username)

        if user.groups.filter(name = 'Manager').exists():
            return Response({"message":"This user is already manager"}, status=status.HTTP_400_BAD_REQUEST)
        
        managers = Group.objects.get(name="Manager")
        managers.user_set.add(user)
        return Response({"message":"New manager was assigned"}, status=status.HTTP_200_OK)
    
    def delete(self, request, pk):
        user = get_object_or_404(User, id = pk)
        role = Group.objects.get(name = 'Manager')
        user.groups.remove(role)
        return Response ({"message" : "Manager role was removed successfully"}, status=status.HTTP_200_OK)
        
        
class DeliveryGroupApiView(APIView):

    permission_classes = [ManagerUser]

    def get(self, request):
        users = User.objects.filter(groups__name = 'Delivery')
        serializer = UserSerializer(users, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        try:
            username = request.data['username']
        except KeyError:
            return Response({"message" : "You didn't provide proper data"}, status=status.HTTP_400_BAD_REQUEST)
        
        user = get_object_or_404(User, username=username)

        if user.groups.filter(name = 'Delivery').exists():
            return Response({"message":"This user is already in delivery-crew"}, status=status.HTTP_400_BAD_REQUEST)
        
        managers = Group.objects.get(name="Delivery")
        managers.user_set.add(user)
        return Response({"message":"New delivery-crew member was assigned"}, status=status.HTTP_200_OK)
    
    def delete(self, request, pk = None):
        if pk:
            user = get_object_or_404(User, id = pk)
            role = Group.objects.get(name = 'Delivery')
            user.groups.remove(role)
            return Response ({"message" : "Delivery-crew role was removed successfully"}, status=status.HTTP_200_OK)


class CartApiView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        cart = user.cart_set.all()
        serializer = CartSerializer(cart, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):

        serializer = CartSerializer(data = request.data, context = {'request':request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()

        return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
    
    def delete(self, request):
        user = request.user
        cart = user.cart_set.all().delete()
        return Response({"message":"All items from cart were successfully deleted"}, status=status.HTTP_200_OK)
    

class OrderApiView(APIView):
    
    permission_classes = [IsAuthenticated]

    def get(self, request, pk = None):

        if request.user.groups.filter(name = 'Manager').exists() or request.user.is_superuser:
            orders = Order.objects.all()
            serializer = OrderSerializer(orders, many = True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        elif request.user.groups.filter(name = 'Delivery').exists():
            orders = Order.objects.filter(delivery_crew = request.user)
            serializer = OrderSerializer(orders, many = True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        else:
            if pk:
                order = get_object_or_404(Order, id = pk)
                if request.user != order.user:
                    return Response({"message":"You are not able to view this data"}, status=status.HTTP_403_FORBIDDEN)
                else:
                    serializer = OrderSerializer(order)
                    return Response(serializer.data, status=status.HTTP_200_OK)

            else:
                orders = Order.objects.filter(user = request.user)
                serializer = OrderSerializer(orders, many = True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            
    def post(self, request):
        cart = Cart.objects.filter(user = request.user)

        if not cart:
            return Response({"message":"Cart is empty, can't create order"}, status=status.HTTP_404_NOT_FOUND)
        
        total = 0
        for item in cart:
            total += item.price
        order = Order(user=request.user, total = total, date = datetime.timedelta(hours=2))
        order.save()
        orderitems = [OrderItem(order = order, 
                                menuitem = item.menuitem, 
                                quantity = item.quantity, 
                                price = item.price, 
                                unit_price = item.unit_price) for item in cart]
        
        OrderItem.objects.bulk_create(orderitems)
        serializer = OrderSerializer(order)
        cart.delete()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
            

        

    def delete(self, request, pk = None):
        if pk:
            order = get_object_or_404(Order, id = pk)
            if request.user.groups.filter(name = 'Manager').exists() or request.user.is_superuser:
                order.delete()
                return Response ({"message" : "Order was deleted"}, status=status.HTTP_200_OK)
            else:
                return Response({"message":"You are not able to delete this order"}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({"message":"You didn't provide proper id"}, status=status.HTTP_404_NOT_FOUND)









