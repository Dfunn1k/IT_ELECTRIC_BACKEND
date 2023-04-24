from django.urls import path
from rest_framework.authtoken import views

from .views import (MedicionREUploadView, MedicionTAUploadView,
                    MotorCreateView, TestREMedicionesView, UserList,
                    UserMotorsView)

app_name = 'app'
urlpatterns = [
    path('api/usuarios/', UserList.as_view(), name='user-list'),
    path('api/token/', views.obtain_auth_token),
    path('api/create_motor/', MotorCreateView.as_view(), name='create_motor'),
    path('api/user/<int:user_pk>/motors/', UserMotorsView.as_view(), name='user_motors'),
    path('api/medicionesRE/upload/', MedicionREUploadView.as_view(), name='create_medicion_re'),
    path('api/medicionesTA/upload/', MedicionTAUploadView.as_view(), name='create_medicion_ta'),
    path('api/testmedicionesRE/<int:test_re_key>/', TestREMedicionesView.as_view(), name='get_medicion_re'),
]