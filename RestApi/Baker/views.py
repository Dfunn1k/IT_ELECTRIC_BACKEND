from datetime import datetime

import pandas as pd
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.utils import timezone
from openpyxl import load_workbook
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.generics import CreateAPIView, ListAPIView
# excel
from rest_framework.parsers import (FileUploadParser, FormParser, JSONParser,
                                    MultiPartParser)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (MedicionRE, MedicionTA, Motor, ResultadoElectrico, TestRE,
                     TestTA, TransitorioArranque)
from .serializers import (MedicionRESerializer, MedicionTASerializer,
                          MotorSerializer, ResultadoElectricoSerializer,
                          TestRESerializer, TestTASerializer,
                          TransitorioArranqueSerializer, UserSerializer)


class UserList(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class LoginView(APIView):
    def post(self, request):
        # Verifica las credenciales del usuario
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        # Crea o recupera el token del usuario
        token, created = Token.objects.get_or_create(user=user)

        # Devuelve el token y el ID del usuario en la respuesta
        return Response({'token': token.key, 'user_id': user.id})

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        # Elimina el token del usuario
        Token.objects.filter(user=request.user).delete()
        return Response({'detail': 'El token fue eliminado'},status=204)


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
                response_data = MotorSerializer(motor).data
            except (Motor.DoesNotExist, KeyError):
                # motor = serializer.save(usuario=request.user)
                response_data = serializer.save(usuario=request.user)

            # Crear una instancia del serializador para devolver los datos del
            # motor
            # response_serializer = MotorSerializer(motor)
            # response_data = response_serializer.data

            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserMotorsView(APIView):
    def get(self, request, user_pk):
        motors = Motor.objects.filter(usuario__pk=user_pk)
        serializer = MotorSerializer(motors, many=True)
        return Response(serializer.data)

class TestREMedicionesView(APIView):
    def get(self, request, test_re_nro):
        mediciones = MedicionRE.objects.filter(test_re_nro=test_re_nro)
        data = {
            #'item': list(mediciones.values_list('item', flat=True)),
            'time': list(mediciones.values_list('time', flat=True)),
            'mag_v1': list(mediciones.values_list('mag_v1', flat=True)),
            'mag_v2': list(mediciones.values_list('mag_v2', flat=True)),
            'mag_v3': list(mediciones.values_list('mag_v3', flat=True)),
            'mag_i1': list(mediciones.values_list('mag_i1', flat=True)),
            'mag_i2': list(mediciones.values_list('mag_i2', flat=True)),
            'mag_i3': list(mediciones.values_list('mag_i3', flat=True))
        }
        return Response(data)
        #serializer = MedicionRESerializer(mediciones, many=True)
        #return Response(serializer.data)

class MedicionREUploadView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        if "file" not in request.data:
            return Response(
                {"error": "No file R.E. provided"},
                status=status.HTTP_400_BAD_REQUEST
            )

        file = request.data["file"]
        wb = load_workbook(file)
        res_elec_nro = request.data.get("res_elec_nro")
        resultado_electrico = ResultadoElectrico.objects.get(pk=res_elec_nro)

        # Leer el archivo de Excel y obtener las mediciones
        df = pd.read_excel(file)

        sheet_name = wb.sheetnames[0].rsplit("-", 2)
        sheet_name = ":".join(sheet_name)
        test_date_time = datetime.strptime(sheet_name, "%Y-%m-%dT%H:%M:%S")
        test_date_time = timezone.make_aware(test_date_time)
        
        try:
            test_re = TestRE.objects.create(
                res_elec_nro=resultado_electrico,
                test_date_time=test_date_time
            )
        except ValidationError as e:
            return Response({'error': e}, status=400)

        test_re_pk = test_re.pk

        # Iterar sobre las filas del DataFrame
        mediciones_data = []
        for index, row in df.iterrows():
            # Crear el objeto Reading y agregarlo a la lista de mediciones
            medicion_data = {
                "test_re_nro": test_re_pk,
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
        mediciones_serializer = MedicionRESerializer(data=mediciones_data,
                                                     many=True)
        mediciones_serializer.is_valid(raise_exception=True)
        mediciones_serializer.save()

        return Response(
            {"message": "Las mediciones R.E. han sido creadas exitosamente"},
            status=status.HTTP_201_CREATED,
        )


class MedicionTAUploadView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        if "file" not in request.data:
            return Response(
                {"error": "No file T.A. provided"},
                status=status.HTTP_400_BAD_REQUEST
            )

        file = request.data["file"]
        wb = load_workbook(file)
        trans_arran_nro = request.data.get("trans_arran_nro")
        transitorio_arranque = TransitorioArranque.objects.get(
            pk=trans_arran_nro)

        # Leer el archivo de Excel y obtener las mediciones
        df = pd.read_excel(file)

        sheet_name = wb.sheetnames[0].rsplit("-", 2)
        sheet_name = ":".join(sheet_name)
        test_date_time = datetime.strptime(sheet_name, "%Y-%m-%dT%H:%M:%S")
        test_date_time = timezone.make_aware(test_date_time)

        try:
            test_ta = TestTA.objects.create(
                trans_arran_nro=transitorio_arranque,
                test_date_time=test_date_time
            )
        except ValidationError as e:
            return Response({'error': e}, status=400)

        test_ta_pk = test_ta.pk

        # Iterar sobre las filas del DataFrame
        mediciones_data = []
        for index, row in df.iterrows():
            # Crear el objeto Reading y agregarlo a la lista de mediciones
            medicion_data = {
                "test_ta_nro": test_ta_pk,
                "item": row["item"],
                "time": row["time"],
                "v1": row["v1"],
                "v2": row["v2"],
                "v3": row["v3"],
                "i1": row["i1"],
                "i2": row["i2"],
                "i3": row["i3"],
            }
            mediciones_data.append(medicion_data)

        # Serializar y guardar las mediciones
        mediciones_serializer = MedicionTASerializer(data=mediciones_data,
                                                     many=True)
        mediciones_serializer.is_valid(raise_exception=True)
        mediciones_serializer.save()

        return Response(
            {"message": "Las mediciones T.A. han sido creadas exitosamente"},
            status=status.HTTP_201_CREATED,
        )


class MotorDeleteView(APIView):
    def delete(self, request, pk):
        try:
            motor = Motor.objects.get(pk=pk)
            motor.delete()
            return Response({"message": f"El motor con el id '{pk}' fue correctamente eliminado"}, status=status.HTTP_204_NO_CONTENT)
        except Motor.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
class TestREDeleteView(APIView):
    def delete(self, request, pk):
        try:
            test_re = TestRE.objects.get(pk=pk)
            test_re.delete()
            return Response({"message": f"Las mediciones del test '{pk}' fueron correctamente eliminadas"}, status=status.HTTP_204_NO_CONTENT)
        except TestRE.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

# class ResultadoElectricoCreateView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, format=None):
#         parser = JSONParser()
#         data = parser.parse(request)

#         serializer = ResultadoElectricoSerializer(data=data)

#         # Si el serializador es válido, se procesa la información
#         if serializer.is_valid():
#             # Se obtiene el objeto motor y su llave primaria
#             motor_obj = serializer.validated_data["motor_nro"]
#             motor_nro = motor_obj.motor_key

#             # Se obtiene el tipo de prueba o se establece por defecto
#             #test_type = serializer.validated_data.get("test_type")

#             try:
#                 # Se busca el motor y se verifica que pertenezca al usuario
#                 # actual
#                 motor = Motor.objects.get(motor_key=motor_nro,
#                                           usuario=request.user)
#             except Motor.DoesNotExist:
#                 # Si el motor no existe o no está registrado al usuario actual,
#                 # se retorna un error 404
#                 return Response(
#                     {
#                         "error": f"Motor with ID {motor_nro} does not exist \
#                             or is not registered to the current user"
#                     },
#                     status=status.HTTP_404_NOT_FOUND,
#                 )

#             # Se crea el objeto de prueba y se obtiene su llave primaria
#             test = ResultadoElectrico.objects.create(motor_nro=motor)
#             response_data = {"test_id": test.test_key}
#             return Response(response_data, status=status.HTTP_201_CREATED)

#         # Si el serializador no es válido, se retorna un error 400 con los
#         # errores de validación
# return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
