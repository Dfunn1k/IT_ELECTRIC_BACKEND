import uuid
from django.contrib.auth.models import User
from django.db import models


class Motor(models.Model):
    motor_key = models.AutoField(primary_key=True)
    modelo = models.CharField(max_length=100)
    name = models.CharField(max_length=100, unique=True, default=uuid.uuid4)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)


class Test(models.Model):
    test_key = models.AutoField(primary_key=True)
    test_type = models.CharField(max_length=100, default="notest")
    motor_nro = models.ForeignKey(Motor, on_delete=models.CASCADE)


class Medicion(models.Model):
    medicion_key = models.AutoField(primary_key=True)
    test_key = models.ForeignKey(Test, on_delete=models.CASCADE)
    item = models.IntegerField()
    time = models.DateTimeField()
    # Tension.magnitud
    mag_v1 = models.FloatField()
    mag_v2 = models.FloatField()
    mag_v3 = models.FloatField()
    # --
    ang_v1 = models.FloatField()
    ang_v2 = models.FloatField()
    ang_v3 = models.FloatField()
    # --
    v1_freq = models.FloatField()
    v2_freq = models.FloatField()
    v3_freq = models.FloatField()

    # Current.magnitud
    mag_i1 = models.FloatField()
    mag_i2 = models.FloatField()
    mag_i3 = models.FloatField()
    # --
    ang_i1 = models.FloatField()
    ang_i2 = models.FloatField()
    ang_i3 = models.FloatField()
    # --
    i1_freq = models.FloatField()
    i2_freq = models.FloatField()
    i3_freq = models.FloatField()

    class Meta:
        unique_together = ('test_key', 'item')
