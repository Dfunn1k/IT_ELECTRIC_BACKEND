from django.shortcuts import render
from .models import Motor, Test, Medicion
from .serializers import MotorSerializer, TestSerializer, MedicionSerializer, UserSerializer 
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

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)
        print(f"self.request.user: {self.request.user}")