from django.contrib.auth.models import User
from rest_framework import serializers

from .models import (MeasurementER, MeasurementTB, Engine, ElectricalResult, TestER,
                     TestTB, TransientBoot, AverageMeasurement)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]


class TestERSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestER
        fields = ("test_electrical_result_pk", "electrical_result_fk", "test_date_time")


class ElectricalResultSerializer(serializers.ModelSerializer):
    test_electrical_result = TestERSerializer(many=True, read_only=True, source='tester_set')
    class Meta:
        model = ElectricalResult
        fields = ("electrical_result_pk", "engine_fk", "test_electrical_result")


class TestTBSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestTB
        fields = ("test_transient_boot_pk", "transient_boot_fk", "test_date_time")


class TransientBootSerializer(serializers.ModelSerializer):
    test_transient_boot = TestTBSerializer(many=True, read_only=True, source='testtb_set')
    class Meta:
        model = TransientBoot
        fields = ("transient_boot_pk", "engine_fk", "test_transient_boot")


class EngineSerializer(serializers.ModelSerializer):
    electrical_result = ElectricalResultSerializer(many=True, read_only=True, source='electricalresult_set')
    transient_boot = TransientBootSerializer(many=True, read_only=True, source='transientboot_set')
    class Meta:
        model = Engine
        fields = ("engine_pk",
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
                  "electrical_result",
                  "transient_boot",
                  )

    def create(self, validated_data):
        engine = Engine.objects.create(**validated_data)
        electrical_result = engine.electricalresult_set.first()
        transient_boot = engine.transientboot_set.first()
        response_data = {
            "engine_pk": engine.engine_pk,
            "name": engine.name,
            "electrical_result_pk": electrical_result.electrical_result_pk,
            "boot_transient_pk": transient_boot.transient_boot_pk
        }
        return response_data
        


class MeasurementERSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeasurementER
        fields = (
            "measurement_electrical_result_pk",
            "test_electrical_result_fk",
            #"item",
            "time",
            "mag_v1",
            "mag_v2",
            "mag_v3",
            "ang_v1",
            "ang_v2",
            "ang_v3",
            "mag_i1",
            "mag_i2",
            "mag_i3",
            "ang_i1",
            "ang_i2",
            "ang_i3",
            "v1_freq",
            "v2_freq",
            "v3_freq",
            "i1_freq",
            "i2_freq",
            "i3_freq",
        )


class MeasurementTBSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeasurementTB
        fields = ("measurement_transient_boot_pk",
                  "test_transient_boot_fk",
                  #"item",
                  "time",
                  "ia",
                  "ib",
                  "ic",
                  "va",
                  "vb",
                  "vc",
                  )
