from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.utils import timezone
import time
import pandas as pd
from openpyxl import load_workbook
import numpy as np

from concurrent.futures import ThreadPoolExecutor

from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.parsers import FileUploadParser, FormParser, JSONParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import MeasurementER, MeasurementTB, Engine, ElectricalResult, TestER, TestTB, TransientBoot, AverageMeasurement
from .serializers import MeasurementERSerializer, MeasurementTBSerializer, EngineSerializer, ElectricalResultSerializer, TestERSerializer, TestTBSerializer, TransientBootSerializer, UserSerializer

from datetime import datetime

import multiprocessing
import concurrent.futures
from .utils import create_objects, process_array, read_excel_chunk, data_avarage


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
        return Response({'detail': 'El token fue eliminado'}, status=204)


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
        measurements = MeasurementER.objects.filter(
            test_electrical_result_fk=test_er)
        data = {
            # 'item': list(mediciones.values_list('item', flat=True)),
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
        measurements = MeasurementTB.objects.filter(
            test_transient_boot_fk=test_tb)
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

        # Obtener la data necesaria para crear el objeto testRE
        electrical_result_fk = pk
        obj_electrical_result = ElectricalResult.objects.get(
            pk=electrical_result_fk)
        # Leer el archivo de Excel y obtener las mediciones
        wb = load_workbook(file, read_only=True)
        # columnas_deseadas = [2,3,4]

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
            test_electrical_result = TestER.objects.get(
                electrical_result_fk=obj_electrical_result, test_date_time=test_date_time)
            test_electrical_result.delete()
            return Response({'error': f"{e}, tambien se elimino el testER", }, status=400)
        df = pd.read_excel(file)

        number_cores = multiprocessing.cpu_count()

        array = df.to_numpy()
        promedio = data_avarage(array, electrical_result_fk)
        obj_average = AverageMeasurement(test_electrical_result_fk=test_electrical_result,
                                         ab=promedio["voltage"]["ab"],
                                         bc=promedio["voltage"]["bc"],
                                         ca=promedio["voltage"]["ca"],
                                         avg=promedio["voltage"]["avg"],
                                         value=promedio["voltage"]["value"],
                                         unbalance=promedio["unbalance"],
                                         thdv_a=promedio["distorsion"]["thdv_a"],
                                         thdv_b=promedio["distorsion"]["thdv_b"],
                                         thdv_c=promedio["distorsion"]["thdv_c"],
                                         thdv_avg=promedio["distorsion"]["thdv_avg"],
                                         thdi_a=promedio["distorsion"]["thdi_a"],
                                         thdi_b=promedio["distorsion"]["thdi_b"],
                                         thdi_c=promedio["distorsion"]["thdi_c"],
                                         thdi_avg=promedio["distorsion"]["thdi_avg"],
                                         tdv_a=promedio["full_distorsion"]["tdv_a"],
                                         tdv_b=promedio["full_distorsion"]["tdv_b"],
                                         tdv_c=promedio["full_distorsion"]["tdv_c"],
                                         tdv_avg=promedio["full_distorsion"]["tdv_avg"],
                                         tdi_a=promedio["full_distorsion"]["tdi_a"],
                                         tdi_b=promedio["full_distorsion"]["tdi_b"],
                                         tdi_c=promedio["full_distorsion"]["tdi_c"],
                                         tdi_avg=promedio["full_distorsion"]["tdi_avg"],
                                         current_a=promedio["current_level"]["current_a"],
                                         current_b=promedio["current_level"]["current_b"],
                                         current_c=promedio["current_level"]["current_c"],
                                         current_avg=promedio["current_level"]["current_avg"],
                                         current_nominal=promedio["current_level"]["current_nominal"],
                                         current_unbalance=promedio["current_unbalance"],
                                         load_percen_avg=promedio["efficiency"]["load_percen_avg"],
                                         lsskw_avg=promedio["efficiency"]["lsskw_avg"],
                                         eff_avg=promedio["efficiency"]["eff_avg"],
                                         sideband_amplitud_db=promedio["spectrum"]["sideband_amplitud_db"],
                                         sideband_freq_hz=promedio["spectrum"]["sideband_freq_hz"],
                                         vab_fase=promedio["symetrical_components"]["vab_fase"],
                                         vbc_fase=promedio["symetrical_components"]["vbc_fase"],
                                         vca_fase=promedio["symetrical_components"]["vca_fase"],
                                         unbalance_voltage=promedio["symetrical_components"]["unbalance_voltage"],
                                         va1_amplitud=promedio["symetrical_components"]["va1_amplitud"],
                                         va2_amplitud=promedio["symetrical_components"]["va2_amplitud"],
                                         va1_fase=promedio["symetrical_components"]["va1_fase"],
                                         va2_fase=promedio["symetrical_components"]["va2_fase"],
                                         ia_fase=promedio["symetrical_components"]["ia_fase"],
                                         ib_fase=promedio["symetrical_components"]["ib_fase"],
                                         ic_fase=promedio["symetrical_components"]["ic_fase"],
                                         unbalance_current=promedio["symetrical_components"]["unbalance_current"],
                                         ia1_amplitud=promedio["symetrical_components"]["ia1_amplitud"],
                                         ia2_amplitud=promedio["symetrical_components"]["ia2_amplitud"],
                                         ia1_fase=promedio["symetrical_components"]["ia1_fase"],
                                         ia2_fase=promedio["symetrical_components"]["ia2_fase"],
                                         )
        obj_average.save()

        split_array = np.array_split(array, number_cores)
        data_with_test = [(split_array[i], test_electrical_result)
                          for i in range(number_cores)]

        with concurrent.futures.ThreadPoolExecutor(max_workers=number_cores) as executor:
            executor.map(process_array, data_with_test)

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

        # verificamos que el archivo tenga una extensión xlsx
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
            print("llegue a entrar al try")
        except ValidationError as e:
            test_transient_boot = TestTB.objects.get(
                transient_boot_fk=obj_transient_boot, test_date_time=test_date_time)
            test_transient_boot.delete()
            print("entre al except")
            return Response({'error': f"{e}, tambien se elimino el testTB"}, status=400)
        print("Sali del except")
        with ThreadPoolExecutor() as executor:
            futures = []
            for chunk in read_excel_chunk(wb, 1000, test_transient_boot):
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


class AverageView(APIView):
    def get(self, request, test_er):
        test_er_obj = TestER.objects.get(pk=test_er)
        electrical_result_obj = test_er_obj.electrical_result_fk
        engine_pk = electrical_result_obj.engine_fk.pk
        promedio = AverageMeasurement.objects.get(
            test_electrical_result_fk=test_er)
        tests = TestER.objects.filter(
            electrical_result_fk__engine_fk=engine_pk)
        history = {}
        for index, test in enumerate(tests, start=1):
            value = AverageMeasurement.objects.get(
                test_electrical_result_fk=test.pk)
            history[index] = {
                'value': value.value,
                'fecha': test.test_date_time.strftime("%d/%m/%Y"),
                'hora': test.test_date_time.strftime("%H:%M:%S"),
            }
        gauge = {
            "minValue": 0,
            "maxValue": 120,
            "value": promedio.value
        }

        data = {
            "popupVoltage": {
                "values": {
                    "ab": promedio.ab,
                    "bc": promedio.bc,
                    "ca": promedio.ca,
                    "avg": promedio.avg,
                    "rated": electrical_result_obj.engine_fk.voltage_rating,
                    "value": promedio.value
                },
                "gauge": gauge,
                "history": history
            },
            "popupUnbalance": {
                "values": {
                    "ab": promedio.ab,
                    "bc": promedio.bc,
                    "ca": promedio.ca,
                    "avg": promedio.avg,
                    "unbalance": promedio.unbalance,
                    "nemaDerating": electrical_result_obj.engine_fk.amps_rating,
                },
                "gauge": gauge,
                "history": history
            },
            "popupDistorsion": {
                "tdhv": {
                    "a": promedio.thdv_a,
                    "b": promedio.thdv_b,
                    "c": promedio.thdv_c,
                    "avg": promedio.thdv_avg,
                },
                "tdhi": {
                    "a": promedio.thdi_a,
                    "b": promedio.thdi_b,
                    "c": promedio.thdi_c,
                    "avg": promedio.thdi_avg
                },
                "history": history
            },
            "popupFullDistorsion": {
                "tdv": {
                    "a": promedio.tdv_a,
                    "b": promedio.tdv_b,
                    "c": promedio.tdv_c,
                    "avg": promedio.tdv_avg
                },
                "tdi": {
                    "a": promedio.tdi_a,
                    "b": promedio.tdi_b,
                    "c": promedio.tdi_c,
                    "avg": promedio.tdi_avg
                },
                "gauge": gauge,
                "history": history
            },
            "popupCurrentLevel": {
                "values": {
                    "a": promedio.current_a,
                    "b": promedio.current_b,
                    "c": promedio.current_c,
                    "avg": promedio.current_avg,
                    "nominalCurrent": promedio.current_nominal,
                    "rated": electrical_result_obj.engine_fk.voltage_rating
                },
                "gauge": gauge,
                "history": history
            },
            "popupCurrentUnbalance": {
                "values": {
                    "a": promedio.current_a,
                    "b": promedio.current_b,
                    "c": promedio.current_c,
                    "avg": promedio.current_avg,
                    "currentUnbalance": promedio.current_unbalance,
                    "rated": electrical_result_obj.engine_fk.voltage_rating
                },
                "gauge": gauge,
                "history": history
            },
            "popupEfficiency": {
                "values": {
                    "load": promedio.load_percen_avg,
                    "losses": promedio.lsskw_avg,
                    "efficiency": promedio.eff_avg
                },
                "gauge": gauge,
                "history": history
            },
            "popupLoad": {
                "values": {
                    "efficiency": promedio.eff_avg,
                    "speed": electrical_result_obj.engine_fk.speed_rpm,
                    "nemaDerating": electrical_result_obj.engine_fk.amps_rating,
                    "load": promedio.load_percen_avg
                },
                "gauge": gauge,
                "history": history
            },
            "popupSpectrum": {
                "values": {
                    "sideAmplitude": promedio.sideband_amplitud_db,
                    "sidebandFreq": promedio.sideband_freq_hz,
                    "fundFreq": electrical_result_obj.engine_fk.freq_hz,
                },
                "history": history
            },
            "SymmetricalComponents": [
                {
                    "section_left": [
                        {
                            "title": 'Vab',
                            "values": {
                                "amplitud": f"{promedio.ab} [V]",
                                "fase": f"{promedio.vab_fase}°"
                            }
                        },
                        {
                            "title": 'Vbc',
                            "values": {
                                "amplitud": f"{promedio.bc} [V]",
                                "fase": f"{promedio.vbc_fase}°"
                            }
                        },
                        {
                            "title": "Vca",
                            "values": {
                                "amplitud": f"{promedio.ca} [V]",
                                "fase": f"{promedio.vca_fase}°"
                            }
                        }],
                    "section_mid": "35%",
                    "section_right": [
                        {
                            "title": "VA1",
                            "values": {
                                "amplitud": promedio.va1_amplitud,
                                "fase": promedio.va1_fase
                            }
                        },
                        {
                            "title": "VA2",
                            "values": {
                                "amplitud": promedio.va2_amplitud,
                                "fase": promedio.va2_fase
                            }
                        }
                    ]
                },
                {
                    "section_left": [
                        {
                            "title": "IA",
                            "values": {
                                "amplitud": f"{promedio.current_a} [I]",
                                "fase": f"{promedio.ia_fase}°"
                            }
                        },
                        {
                            "title": "IB",
                            "values": {
                                "amplitud": f"{promedio.current_b} [I]",
                                "fase": f"{promedio.ib_fase}°"
                            }
                        },
                        {
                            "title": "IC",
                            "values": {
                                "amplitud": f"{promedio.current_c} [I]",
                                "fase": f"{promedio.ic_fase}°"
                            }
                        }
                    ],
                    "section_mid": "35%",
                }

            ]

        }

        return Response(data)
