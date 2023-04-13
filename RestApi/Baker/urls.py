from django.urls import path
from .views import UserList, MotorCreateView
from rest_framework.authtoken import views


app_name = 'app'
urlpatterns = [
    path('api/usuarios/', UserList.as_view(), name='user-list'),
    path('api/create_motor/', MotorCreateView.as_view(), name='create-motor'),
    path('api/token/', views.obtain_auth_token),
]