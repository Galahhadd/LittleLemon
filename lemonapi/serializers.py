from rest_framework import serializers

from django.contrib.auth.models import User, Group

from .models import Category, MenuItem

class UserSerializer(serializers.ModelField):

    class Meta:
        model = User
        fields = ['username']

class CategorySerializer(serializers.ModelField):

    class Meta:
        model = Category
        fields = ['id', 'slug', 'title']

class MenuItemSerializer(serializers.ModelSerializer):
    #category = CategorySerializer()

    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'featured', 'category']