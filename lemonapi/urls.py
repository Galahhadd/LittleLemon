from django.urls import path

from .views import (MenuItemListCreateApiView,
                    MenuItemUpdateDeleteApiView, 
                    ManagerGroupApiView,
                    DeliveryGroupApiView,)

urlpatterns = [
    #path('groups/manager/users', GroupApiView.as_view()),
    path('menu-items/', MenuItemListCreateApiView.as_view()),
    path('menu-items/<int:pk>', MenuItemUpdateDeleteApiView.as_view()),
    path('groups/manager/users/', ManagerGroupApiView.as_view()),
    path('groups/manager/users/<int:pk>', ManagerGroupApiView.as_view()),
    path('groups/delivery-crew/users/', DeliveryGroupApiView.as_view()),
    path('groups/delivery-crew/users/<int:pk>', DeliveryGroupApiView.as_view()),
]