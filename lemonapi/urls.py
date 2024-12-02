from django.urls import path

from .views import MenuItemListCreateApiView, MenuItemUpdateDeleteApiView

urlpatterns = [
    #path('groups/manager/users', GroupApiView.as_view()),
    path('menu-items/', MenuItemListCreateApiView.as_view()),
    path('menu-items/<int:pk>', MenuItemUpdateDeleteApiView.as_view()),
]