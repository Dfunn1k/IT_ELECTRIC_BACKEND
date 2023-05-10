from django.urls import path
from .views import (LoginView, LogoutView, UploadMeasurementsERView,
                    UploadMeasurementsTBView, CreateEngineView, DeleteEngineView,
                    DeleteTestERView, DeleteTestTBView, GetMeasurementsERView, GetUserList,
                    GetEnginesUserView, EditEngineView, GetMeasurementsTBView)

app_name = 'app'
urlpatterns = [
    path('api/security/login/', LoginView.as_view(), name='login'),
    path('api/security/logout/', LogoutView.as_view(), name='logout'),
    path('api/upload/measurements/electrical_result/<int:pk>/', UploadMeasurementsERView.as_view(), name='create_measurement_er'),
    path('api/upload/measurements/transient_boot/<int:pk>/', UploadMeasurementsTBView.as_view(), name='create_measurement_tb'),
    path('api/delete/engine/<int:pk>/', DeleteEngineView.as_view(), name="delete_engine"),
    path('api/delete/test/electrical_result/<int:pk>/', DeleteTestERView.as_view(), name="delete_test_er"),
    path('api/delete/test/transient_boot/<int:pk>/', DeleteTestTBView.as_view(), name="delete_test_tb"),
    path('api/get/engines/data/<int:user_pk>/', GetEnginesUserView.as_view(), name='user_motors'),
    path('api/get/users/', GetUserList.as_view(), name='user_list'),
    path('api/get/measurements/electrical_result/<int:test_er>/', GetMeasurementsERView.as_view(), name='get_measurement_er'),
    path('api/get/measurements/transient_boot/<int:test_tb>/', GetMeasurementsTBView.as_view(), name='get_measurement_tb'),
    path('api/create/engine/', CreateEngineView.as_view(), name='create_engine'),
    path('api/edit/engine/<int:pk>/', EditEngineView.as_view(), name='edit_engine')
]
