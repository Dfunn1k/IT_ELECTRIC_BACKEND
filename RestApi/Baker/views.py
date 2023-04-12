from django.shortcuts import render
from .models import Usuario, Motor, Test, Medicion
from .serializers import MotorSerializer, TestSerializer, MedicionSerializer, UsuarioSerializer
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.views import APIView

from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework import generics


class UserList(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class MotorCreateView(CreateAPIView):
    queryset = Motor.objects.all()
    serializer_class = MotorSerializer