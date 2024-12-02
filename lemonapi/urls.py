from django.urls import path

from .views import MenuItemApiView

urlpatterns = [
    #path('groups/manager/users', GroupApiView.as_view()),
    path('menu-items/', MenuItemApiView.as_view())
]