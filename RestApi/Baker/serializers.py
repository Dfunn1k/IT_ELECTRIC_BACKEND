from rest_framework import serializers
from .models import Motor, Test, Medicion, Usuario
from django.contrib.auth.models import User


class MotorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Motor
        fields = ('motor_key', 'model', 'usuario')


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ('test_key', 'motor_nro')

class MedicionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicion
        fields = ('medicion_key', 'test_key', 'time', 'mag_v1', 'mag_v2', 'mag_v3', 'ang_v1', 'ang_v2', 'ang_v3')

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('user')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']