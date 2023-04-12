from rest_framework import serializers
from .models import Motor, Test, Medicion


class MotorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Motor
        fields = ('motor_key', 'model', 'user')


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ('test_key', 'motor_nro')

class MedicionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicion
        fields = ('medicion_key', 'test_key', 'time', 'mag_v1', 'mag_v2', 'mag_v3', 'ang_v1', 'ang_v2', 'ang_v3')