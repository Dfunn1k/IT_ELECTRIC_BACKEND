from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models


class Motor(models.Model):
    motor_key = models.AutoField(primary_key=True)
    #no deber ser unique -> 2 usuarios pueden crear un motod llamado "motor A", to do✅
    name = models.CharField(max_length=100, unique=True)
    #model = models.CharField(max_length=100)
    power_out_hp = models.FloatField()
    power_out_kw = models.FloatField()
    voltage_rating = models.FloatField()
    speed_rpm = models.FloatField()
    amps_rating = models.FloatField()
    off_level = models.FloatField()
    frame = models.FloatField()
    insulation_class = models.FloatField()
    locked_rotor_current = models.FloatField()
    locked_rotor_code = models.FloatField()
    freq_hz = models.FloatField()



    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # Si el objeto no tiene un id, entonces es nuevo y se está creando
        if not self.pk:
            super().save(*args, **kwargs)
            # Crear una instancia de R.E y T.A asociada a este Motor
            ResultadoElectrico.objects.create(motor_nro=self)
            TransitorioArranque.objects.create(motor_nro=self)
        else:
            super().save(*args, **kwargs)


class ResultadoElectrico(models.Model):
    res_elec_key = models.AutoField(primary_key=True)
    motor_nro = models.ForeignKey(Motor, on_delete=models.CASCADE)
    # test_type = models.CharField(max_length=100
    # , default="notest")
    # test_date_time = models.DateTimeField()


class TransitorioArranque(models.Model):
    t_arranque_key = models.AutoField(primary_key=True)
    motor_nro = models.ForeignKey(Motor, on_delete=models.CASCADE)


class TestRE(models.Model):
    test_re_key = models.AutoField(primary_key=True)
    res_elec_nro = models.ForeignKey(
        ResultadoElectrico, on_delete=models.CASCADE)
    test_date_time = models.DateTimeField()

    def save(self, *args, **kwargs):
        if TestRE.objects.filter(res_elec_nro=self.res_elec_nro,test_date_time=self.test_date_time).exists():
            raise ValidationError("Ya existe un archivo con la misma fecha para este TestRE")
        else:
            super().save(*args, **kwargs)

class TestTA(models.Model):
    test_ta_key = models.AutoField(primary_key=True)
    trans_arran_nro = models.ForeignKey(
        TransitorioArranque, on_delete=models.CASCADE)
    test_date_time = models.DateTimeField()

    def save(self, *args, **kwargs):
        if TestTA.objects.filter(trans_arran_nro=self.trans_arran_nro,test_date_time=self.test_date_time).exists():
            raise ValidationError("Ya existe un archivo con la misma fecha para este TestTA")
        else:
            super().save(*args, **kwargs)


class MedicionRE(models.Model):
    medicion_re_key = models.AutoField(primary_key=True)
    test_re_nro = models.ForeignKey(TestRE, on_delete=models.CASCADE)
    # item = models.IntegerField()
    # time = models.DateTimeField()
    # mag_v1 = models.FloatField()
    # mag_v2 = models.FloatField()
    # mag_v3 = models.FloatField()
    # ang_v1 = models.FloatField()
    # ang_v2 = models.FloatField()
    # ang_v3 = models.FloatField()
    # v1_freq = models.FloatField()
    # v2_freq = models.FloatField()
    # v3_freq = models.FloatField()
    # mag_i1 = models.FloatField()
    # mag_i2 = models.FloatField()
    # mag_i3 = models.FloatField()
    # ang_i1 = models.FloatField()
    # ang_i2 = models.FloatField()
    # ang_i3 = models.FloatField()
    # i1_freq = models.FloatField()
    # i2_freq = models.FloatField()
    # i3_freq = models.FloatField()

    class Meta:
        unique_together = ('test_re_nro', 'item')


class MedicionTA(models.Model):
    medicion_ta_key = models.AutoField(primary_key=True)
    test_ta_nro = models.ForeignKey(TestTA, on_delete=models.CASCADE)
    item = models.IntegerField()
    time = models.DateTimeField()
    v1 = models.FloatField()
    v2 = models.FloatField()
    v3 = models.FloatField()
    i1 = models.FloatField()
    i2 = models.FloatField()
    i3 = models.FloatField()

    class Meta:
        unique_together = ('test_ta_nro', 'item')

