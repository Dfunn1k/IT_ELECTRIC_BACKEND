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
        fields = ("test_electrical_result_pk",
                  "electrical_result_fk", "test_date_time")


class ElectricalResultSerializer(serializers.ModelSerializer):
    test_electrical_result = TestERSerializer(
        many=True, read_only=True, source='tester_set')

    class Meta:
        model = ElectricalResult
        fields = ("electrical_result_pk", "engine_fk",
                  "test_electrical_result")


class TestTBSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestTB
        fields = ("test_transient_boot_pk",
                  "transient_boot_fk", "test_date_time")


class TransientBootSerializer(serializers.ModelSerializer):
    test_transient_boot = TestTBSerializer(
        many=True, read_only=True, source='testtb_set')

    class Meta:
        model = TransientBoot
        fields = ("transient_boot_pk", "engine_fk", "test_transient_boot")


class EngineSerializer(serializers.ModelSerializer):
    electrical_result = ElectricalResultSerializer(read_only=True)
    transient_boot = TransientBootSerializer(read_only=True)

    class Meta:
        model = Engine
        fields = (
            "engine_pk",
            "name",
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
        electrical_result_data = ElectricalResultSerializer(
            engine.electricalresult).data
        transient_boot_data = TransientBootSerializer(
            engine.transientboot).data

        response_data = {
            "engine_pk": engine.engine_pk,
            "name": engine.name,
            "electrical_result_pk": electrical_result_data["electrical_result_pk"],
            "transient_boot_pk": transient_boot_data["transient_boot_pk"]
        }

        return response_data


class MeasurementERSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeasurementER
        fields = '__all__'


class MeasurementTBSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeasurementTB
        fields = '__all__'
