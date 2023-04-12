from django.urls import path
# from .views import UserView
from .views import UserList, MotorCreateView


app_name = 'app'
urlpatterns = [
    # path('api/usuarios', UserView.as_view(), name='Usuarios'),
    path('api/usuarios/', UserList.as_view(), name='user-list'),
    path('api/create_motor/', MotorCreateView.as_view(), name='create-motor'),
]