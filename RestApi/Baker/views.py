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
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from rest_framework.parsers import JSONParser


class UserList(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer



class MotorCreateView(APIView):
    def post(self, request, format=None):
        # Utilizar el JSONParser para procesar los datos en formato JSON
        parser = JSONParser()
        data = parser.parse(request)

        serializer = MotorSerializer(data=data)
        if serializer.is_valid():
            # Obtener o crear el motor según su número nombre
            try:
                motor = Motor.objects.get(name=data['name'], usuario=request.user)
            except (Motor.DoesNotExist, KeyError):
                motor = serializer.save(usuario=request.user)

            # Crear una instancia del serializador para devolver los datos del motor
            response_serializer = MotorSerializer(motor)
            response_data = response_serializer.data

            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

