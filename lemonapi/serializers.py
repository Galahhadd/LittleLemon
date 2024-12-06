from rest_framework import serializers

from django.contrib.auth.models import User, Group

from .models import Category, MenuItem, Cart, Order, OrderItem

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'slug', 'title']

class MenuItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField()

    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'featured', 'category', 'category_id']


class CartSerializer(serializers.ModelSerializer):
    menuitem = MenuItemSerializer(read_only = True)
    menuitem_id = serializers.IntegerField(write_only = True)

    class Meta:
        model = Cart
        fields = ['user', 'quantity', 'price', 'unit_price', 'menuitem', 'menuitem_id']
        read_only_fields = ['user', 'price', 'unit_price']

    def validate(self, data):

        menuitem_id = data.get('menuitem_id')
        quantity = data.get('quantity')

        if menuitem_id and quantity:
            unit_price = MenuItem.objects.get(id = menuitem_id).price
            data['unit_price'] = unit_price
            data['price'] = unit_price * quantity
        return data
    
    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)
    
class OrderItemSerializer(serializers.ModelSerializer):
    menuitem = MenuItemSerializer()

    class Meta:
        model = OrderItem
        fields = ['menuitem','quantity', 'price', 'unit_price']


class OrderSerializer(serializers.ModelSerializer):
    orderitem_set = OrderItemSerializer(many = True, read_only = True)

    class Meta:
        model = Order
        fields = ['id','user','delivery_crew', 'status', 'total', 'date', 'orderitem_set']
