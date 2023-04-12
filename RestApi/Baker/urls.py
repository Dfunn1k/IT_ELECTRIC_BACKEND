from django.urls import path
# from .views import UserView
from .views import UserList


app_name = 'app'
urlpatterns = [
    # path('api/usuarios', UserView.as_view(), name='Usuarios'),
    path('api/usuarios/', UserList.as_view(), name='user-list'),
]