from django.contrib.auth.models import User
from rest_framework import serializers

from .models import (MedicionRE, MedicionTA, Motor, ResultadoElectrico, TestRE,
                     TestTA, TransitorioArranque)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]


class TestRESerializer(serializers.ModelSerializer):
    class Meta:
        model = TestRE
        fields = ("test_re_key", "res_elec_nro", "test_date_time")


class ResultadoElectricoSerializer(serializers.ModelSerializer):
    test_re = TestRESerializer(many=True, read_only=True, source='testre_set')
    class Meta:
        model = ResultadoElectrico
        fields = ("res_elec_key", "motor_nro", "test_re")


class TestTASerializer(serializers.ModelSerializer):
    class Meta:
        model = TestTA
        fields = ("test_ta_key", "trans_arran_nro", "test_date_time")


class TransitorioArranqueSerializer(serializers.ModelSerializer):
    test_ta = TestTASerializer(many=True, read_only=True, source='testta_set')
    class Meta:
        model = TransitorioArranque
        fields = ("t_arranque_key", "motor_nro", "test_ta")


class MotorSerializer(serializers.ModelSerializer):
    resultado_electrico = ResultadoElectricoSerializer(many=True, read_only=True, source='resultadoelectrico_set')
    transitorio_arranque = TransitorioArranqueSerializer(many=True, read_only=True, source='transitorioarranque_set')
    class Meta:
        model = Motor
        fields = ("motor_key",
                  "name" ,
                  "power_out_hp",
                  "power_out_kw",
                  "voltage_rating",
                  "speed_rpm",
                  "amps_rating",
                  "off_level",
                  "frame",
                  "insulation_class",
                  "locked_rotor_current",
                  "locked_rotor_code",
                  "freq_hz",
                  "resultado_electrico",
                  "transitorio_arranque",
                  )

    def create(self, validated_data):
        # print("Hola")
        motor = Motor.objects.create(**validated_data)
        resultado_electrico = motor.resultadoelectrico_set.first()
        # print(resultado_electrico.res_elec_key)
        transitorio_arranque = motor.transitorioarranque_set.first()
        response_data = {
            "motor_key": motor.motor_key,
            "name": motor.name,
            "resultado_electrico_key": resultado_electrico.res_elec_key,
            "transitorio_arranque_key": transitorio_arranque.t_arranque_key
        }
        return response_data
        


class MedicionRESerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicionRE
        fields = (
            "medicion_re_key",
            "test_re_nro",
            "item",
            "time",
            "mag_v1",
            "mag_v2",
            "mag_v3",
            "ang_v1",
            "ang_v2",
            "ang_v3",
            "v1_freq",
            "v2_freq",
            "v3_freq",
            "mag_i1",
            "mag_i2",
            "mag_i3",
            "ang_i1",
            "ang_i2",
            "ang_i3",
            "i1_freq",
            "i2_freq",
            "i3_freq",
        )


class MedicionTASerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicionTA
        fields = ("medicion_ta_key",
                  "test_ta_nro",
                  "item",
                  "time",
                  "v1",
                  "v2",
                  "v3",
                  "i1",
                  "i2",
                  "i3",
                  )
