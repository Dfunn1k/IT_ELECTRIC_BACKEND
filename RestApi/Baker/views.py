from django.shortcuts import render
from .models import Motor, Test, Medicion
from .serializers import (
    MotorSerializer,
    TestSerializer,
    MedicionSerializer,
    UserSerializer,
)
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.views import APIView

from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework import generics
from rest_framework.response import Response

# excel
from rest_framework.parsers import FileUploadParser
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
import pandas as pd


class UserList(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class MedicionUploadView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        if "file" not in request.data:
            return Response(
                {"error": "No file provided"},
                status=status.HTTP_400_BAD_REQUEST
            )

        file = request.data["file"]
        print("request.data: ", request.data)
        test_key = request.data.get("test_key")
        print("test_key: ", test_key)

        # Leer el archivo de Excel y obtener las mediciones
        df = pd.read_excel(file, engine="odf", sheet_name="data")

        # Iterar sobre las filas del DataFrame
        mediciones_data = []
        for index, row in df.iterrows():
            # Buscar o crear el objeto Engine
            # test_object, _ = Test.objects.get_or_create(test_key=2)

            # Crear el objeto Reading y agregarlo a la lista de mediciones
            medicion_data = {
                "test_key": test_key,
                "item": row["item"],
                "time": row["time"],
                "mag_v1": row["MagV1"],
                "mag_v2": row["MagV2"],
                "mag_v3": row["MagV3"],
                "ang_v1": row["AngV1"],
                "ang_v2": row["AngV2"],
                "ang_v3": row["AngV3"],
                "v1_freq": row["V1_Freq"],
                "v2_freq": row["V2_Freq"],
                "v3_freq": row["V3_Freq"],
                "mag_i1": row["MagI1"],
                "mag_i2": row["MagI2"],
                "mag_i3": row["MagI3"],
                "ang_i1": row["AngI1"],
                "ang_i2": row["AngI2"],
                "ang_i3": row["AngI3"],
                "i1_freq": row["I1_Freq"],
                "i2_freq": row["I2_Freq"],
                "i3_freq": row["I3_Freq"],
            }
            mediciones_data.append(medicion_data)

        # Serializar y guardar las mediciones
        mediciones_serializer = MedicionSerializer(data=mediciones_data,
                                                   many=True)
        mediciones_serializer.is_valid(raise_exception=True)
        mediciones_serializer.save()

        return Response(
            {"message": "Las mediciones han sido creadas exitosamente"},
            status=status.HTTP_201_CREATED,
        )


class TestCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        parser = JSONParser()
        data = parser.parse(request)

        serializer = TestSerializer(data=data)

        # Si el serializador es válido, se procesa la información
        if serializer.is_valid():
            # Se obtiene el objeto motor y su llave primaria
            motor_obj = serializer.validated_data["motor_nro"]
            motor_nro = motor_obj.motor_key

            # Se obtiene el tipo de prueba o se establece por defecto
            test_type = serializer.validated_data.get("test_type")

            try:
                # Se busca el motor y se verifica que pertenezca al usuario
                # actual
                motor = Motor.objects.get(motor_key=motor_nro,
                                          usuario=request.user)
            except Motor.DoesNotExist:
                # Si el motor no existe o no está registrado al usuario actual,
                # se retorna un error 404
                return Response(
                    {
                        "error": f"Motor with ID {motor_nro} does not exist \
                            or is not registered to the current user"
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )

            # Se crea el objeto de prueba y se obtiene su llave primaria
            test = Test.objects.create(motor_nro=motor, test_type=test_type)
            response_data = {"test_id": test.test_key}
            return Response(response_data, status=status.HTTP_201_CREATED)

        # Si el serializador no es válido, se retorna un error 400 con los
        # errores de validación
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
                motor = Motor.objects.get(name=data["name"],
                                          usuario=request.user)
            except (Motor.DoesNotExist, KeyError):
                motor = serializer.save(usuario=request.user)

            # Crear una instancia del serializador para devolver los datos del
            # motor
            response_serializer = MotorSerializer(motor)
            response_data = response_serializer.data

            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
