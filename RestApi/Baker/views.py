from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.utils import timezone

import pandas as pd
from openpyxl import load_workbook

from concurrent.futures import ThreadPoolExecutor

from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.parsers import FileUploadParser, FormParser, JSONParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import MeasurementER, MeasurementTB, Engine, ElectricalResult, TestER, TestTB, TransientBoot
from .serializers import MeasurementERSerializer, MeasurementTBSerializer, EngineSerializer, ElectricalResultSerializer, TestERSerializer, TestTBSerializer, TransientBootSerializer, UserSerializer

from datetime import datetime


from .utils import create_objects, read_excel_chunk

class GetUserList(ListAPIView):
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


class CreateEngineView(APIView):
    def post(self, request, format=None):
        # Utilizar el JSONParser para procesar los datos en formato JSON
        parser = JSONParser()
        data = parser.parse(request)

        serializer = EngineSerializer(data=data)
        if serializer.is_valid():
            # Obtener o crear el motor según su número nombre
            try:
                engine = Engine.objects.get(name=data["name"],
                                          user=request.user)
                response_data = EngineSerializer(engine).data
            except (Engine.DoesNotExist, KeyError):
                # motor = serializer.save(usuario=request.user)
                response_data = serializer.save(user=request.user)

            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class GetEnginesUserView(APIView):
    def get(self, request, user_pk):
        engines = Engine.objects.filter(user__pk=user_pk)
        serializer = EngineSerializer(engines, many=True)
        return Response(serializer.data)

class GetMeasurementsERView(APIView):
    def get(self, request, test_er):
        """Esta función obtiene los datos de las columnas mostradas, re"""
        measurements = MeasurementER.objects.filter(test_electrical_result_fk=test_er)
        data = {
            #'item': list(mediciones.values_list('item', flat=True)),
            'time': list(measurements.values_list('time', flat=True)),
            'mag_v1': list(measurements.values_list('mag_v1', flat=True)),
            'mag_v2': list(measurements.values_list('mag_v2', flat=True)),
            'mag_v3': list(measurements.values_list('mag_v3', flat=True)),
            'mag_i1': list(measurements.values_list('mag_i1', flat=True)),
            'mag_i2': list(measurements.values_list('mag_i2', flat=True)),
            'mag_i3': list(measurements.values_list('mag_i3', flat=True))
        }
        return Response(data)
    
class GetMeasurementsTBView(APIView):
    def get(self, request, test_tb):
        measurements = MeasurementTB.objects.filter(test_transient_boot_fk=test_tb)
        data = {
            'time': list(measurements.values_list('time', flat=True)),
            'ia': list(measurements.values_list('ia', flat=True)),
            'ib': list(measurements.values_list('ib', flat=True)),
            'ic': list(measurements.values_list('ic', flat=True)),
            'va': list(measurements.values_list('va', flat=True)),
            'vb': list(measurements.values_list('vb', flat=True)),
            'vc': list(measurements.values_list('vc', flat=True))
        }
        return Response(data)

class UploadMeasurementsERView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]

    def post(self, request, pk):
        # Verificamos que se este enviando un archivo en la petición
        if "file" not in request.data:
            return Response(
                {"error": "No file R.E. provided"},
                status=status.HTTP_400_BAD_REQUEST
            )

        file = request.data["file"]

        # Verificamos que el archivo tenga una extensión xlsx
        if not file.name.endswith('.xlsx'):
            return Response(
                {"error": "El archivo debe ser un archivo de Excel (.xlsx)"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Verificar si se puede leer el archivo
        # try:
        #     df = pd.read_excel(file)
        # except Exception as e:
        #     return Response(
        #         {"error": "No se puede leer el archivo Excel"},
        #         status=status.HTTP_400_BAD_REQUEST
        #     )
        # Verificar que las columnas esten presentes
        # required_columns = [
        #     "item", "time", "mag_v1", "mag_v2", "mag_v3", "ang_v1",
        #     "ang_v2", "ang_v3", "v1_freq", "v2_freq", "v3_freq",
        #     "mag_i1", "mag_i2", "mag_i3", "ang_i1", "ang_i2",
        #     "ang_i3", "i1_freq", "i2_freq", "i3_freq"
        # ]
        # missing_columns = set(required_columns) - set(df.columns)
        # if missing_columns:
        #     return Response(
        #         {"error": f"El archivo debe contener las columnas {', '.join(required_columns)}"},
        #         status=status.HTTP_400_BAD_REQUEST
        #     )
        
        # Obtener la data necesaria para crear el objeto testRE
        electrical_result_fk = pk
        obj_electrical_result = ElectricalResult.objects.get(pk=electrical_result_fk)
        # Leer el archivo de Excel y obtener las mediciones
        wb = load_workbook(file, read_only=True)

        sheet_name = wb.sheetnames[0].rsplit("-", 2)
        sheet_name = ":".join(sheet_name)
        test_date_time = datetime.strptime(sheet_name, "%Y-%m-%dT%H:%M:%S")
        test_date_time = timezone.make_aware(test_date_time)
        
        try:
            test_electrical_result = TestER.objects.create(
                electrical_result_fk=obj_electrical_result,
                test_date_time=test_date_time
            )
        except ValidationError as e:
            test_electrical_result = TestER.objects.get(electrical_result_fk=obj_electrical_result, test_date_time=test_date_time)
            test_electrical_result.delete()
            return Response({'error': f"{e}, tambien se elimino el testER",}, status=400)
        
        
        with ThreadPoolExecutor() as executor:
            futures = []
            for chunk in read_excel_chunk(wb, 625, test_electrical_result):
                futures.append(executor.submit(create_objects, chunk))
            for future in futures:
                future.result()

        return Response(
            {"message": "Las mediciones E.R han sido creadas exitosamente"},
            status=status.HTTP_201_CREATED,
        )


class UploadMeasurementsTBView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]

    def post(self, request, pk):
        if "file" not in request.data:
            return Response(
                {"error": "No file T.A. provided"},
                status=status.HTTP_400_BAD_REQUEST
            )

        file = request.data["file"]

        #verificamos que el archivo tenga una extensión xlsx
        if not file.name.endswith('.xlsx'):
            return Response(
                {"error": "El archivo debe ser un archivo de Excel (.xlsx)"},
                status=status.HTTP_400_BAD_REQUEST
            )

        transient_boot_fk = pk
        obj_transient_boot = TransientBoot.objects.get(
            pk=transient_boot_fk)
        wb = load_workbook(file, read_only=True)
        print(wb.sheetnames)
        sheet_name = wb.sheetnames[0].rsplit("-", 2)

        sheet_name = ":".join(sheet_name)
        test_date_time = datetime.strptime(sheet_name, "%Y-%m-%dT%H:%M:%S")
        test_date_time = timezone.make_aware(test_date_time)

        try:
            test_transient_boot = TestTB.objects.create(
                transient_boot_fk=obj_transient_boot,
                test_date_time=test_date_time
            )
        except ValidationError as e:
            test_transient_boot = TestTB.objects.get(transient_boot_fk=obj_transient_boot, test_date_time=test_date_time)
            test_transient_boot.delete()
            return Response({'error': f"{e}, tambien se elimino el testTB"}, status=400)
 
        with ThreadPoolExecutor() as executor:
            futures = []
            for chunk in read_excel_chunk(wb, 625, test_transient_boot):
                futures.append(executor.submit(create_objects, chunk))
            for future in futures:
                future.result()

        return Response(
            {"message": "Las mediciones T.B. han sido creadas exitosamente"},
            status=status.HTTP_201_CREATED,
        )


class DeleteEngineView(APIView):
    def delete(self, request, pk):
        try:
            engine = Engine.objects.get(pk=pk)
            engine.delete()
            return Response({"message": f"El motor con el id '{pk}' fue correctamente eliminado"}, status=status.HTTP_204_NO_CONTENT)
        except Engine.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
class EditEngineView(APIView):
    def put(self, request, pk):
        engine = Engine.objects.get(pk=pk)
        serializer = EngineSerializer(engine, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        engine = Engine.objects.get(pk=pk)
        serializer = EngineSerializer(engine, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
        
class DeleteTestERView(APIView):
    def delete(self, request, pk):
        try:
            test_electrical_result = TestER.objects.get(pk=pk)
            test_electrical_result.delete()
            return Response({"message": f"Las mediciones del test '{pk}' fueron correctamente eliminadas"}, status=status.HTTP_204_NO_CONTENT)
        except TestER.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class DeleteTestTBView(APIView):
    def delete(self, request, pk):
        try:
            test_transient_boot = TestTB.objects.get(pk=pk)
            test_transient_boot.delete()
            return Response({"message": f"Las mediciones del test '{pk}' fueron correctamente eliminadas"}, status=status.HTTP_204_NO_CONTENT)
        except TestTB.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
