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
from rest_framework.permissions import IsAuthenticated



class UserList(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class TestCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        parser = JSONParser()
        data = parser.parse(request)

        serializer = TestSerializer(data=data)

        # Si el serializador es válido, se procesa la información
        if serializer.is_valid():
            # Se obtiene el objeto motor y su llave primaria
            motor_obj = serializer.validated_data['motor_nro']
            motor_nro = motor_obj.motor_key
            
            # Se obtiene el tipo de prueba o se establece por defecto
            test_type = serializer.validated_data.get('test_type')

            try:
                # Se busca el motor y se verifica que pertenezca al usuario actual
                motor = Motor.objects.get(motor_key=motor_nro, usuario=request.user)
            except Motor.DoesNotExist:
                # Si el motor no existe o no está registrado al usuario actual, se retorna un error 404
                return Response({'error': f'Motor with ID {motor_nro} does not exist or is not registered to the current user'}, status=status.HTTP_404_NOT_FOUND)

            # Se crea el objeto de prueba y se obtiene su llave primaria
            test = Test.objects.create(motor_nro=motor, test_type=test_type)
            response_data = {'test_id': test.test_key}
            return Response(response_data, status=status.HTTP_201_CREATED)
        
        # Si el serializador no es válido, se retorna un error 400 con los errores de validación
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



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

