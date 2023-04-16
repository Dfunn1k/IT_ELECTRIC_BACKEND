from rest_framework import serializers
from .models import Motor, Test, Medicion
from django.contrib.auth.models import User


class MotorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Motor
        fields = ("motor_key", "modelo", "name")


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ("test_key", "motor_nro", "test_type")


class MedicionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicion
        fields = (
            "medicion_key",
            "test_key",
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


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]
