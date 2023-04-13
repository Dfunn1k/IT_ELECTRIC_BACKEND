from django.shortcuts import render
from .models import Motor, Test, Medicion
from .serializers import MotorSerializer, TestSerializer, MedicionSerializer, UserSerializer 
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.views import APIView

from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework import generics
from rest_framework.response import Response

#excel
from rest_framework.parsers import FileUploadParser


class UserList(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class MotorCreateView(CreateAPIView):
    queryset = Motor.objects.all()
    serializer_class = MotorSerializer

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)
        print(f"self.request.user: {self.request.user}")

# class FileUploadView(APIView):
#     parser_classes = (FileUploadParser,)

#     def post(self, request, *args, **kwargs):
#         if 'file' not in request.data
#         return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)

#         file = request.data['file']
#         read_and_store_data(file)
#         return Response({'status': 'success'}, status=status.HTTP_200_OK)


