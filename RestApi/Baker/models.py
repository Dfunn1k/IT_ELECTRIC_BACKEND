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
    test_re_nro = models.ForeignKey(TestRE, on_delete=models.CASCADE, null=True)
    item = models.IntegerField()
    time = models.DateTimeField()
    
    mag_v1 = models.FloatField()
    mag_v2 = models.FloatField()
    mag_v3 = models.FloatField()
    
    ang_v1 = models.FloatField()
    ang_v2 = models.FloatField()
    ang_v3 = models.FloatField()

    mag_i1 = models.FloatField()
    mag_i2 = models.FloatField()
    mag_i3 = models.FloatField()

    ang_i1 = models.FloatField()
    ang_i2 = models.FloatField()
    ang_i3 = models.FloatField()

    v1_freq = models.FloatField()
    v2_freq = models.FloatField()
    v3_freq = models.FloatField()

    pf1_1 = models.FloatField()
    pf2_2 = models.FloatField()
    pf3_3 = models.FloatField()

    kw_1 = models.FloatField()
    kw_2 = models.FloatField()
    kw_3 = models.FloatField()

    kvar_1 = models.FloatField()
    kvar_2 = models.FloatField()
    kvar_3 = models.FloatField()

    ks_1 = models.FloatField()
    ks_2 = models.FloatField()
    ks_3 = models.FloatField()

    ckwh_1 = models.FloatField()
    ckwh_2 = models.FloatField()
    ckwh_3 = models.FloatField()

    lsskw_1 = models.FloatField()
    lsskw_2 = models.FloatField()
    lsskw_3 = models.FloatField()
# ---------------------------------------------

    dv_u2 = models.FloatField()
    dv_u0 = models.FloatField()
    dvf_u2 = models.FloatField()
    dvf_u0 = models.FloatField()

    di_u2 = models.FloatField()
    di_u0 = models.FloatField()
    dif_u2 = models.FloatField()
    dif_u0 = models.FloatField()

    u0_mag = models.FloatField()
    u1_mag = models.FloatField()
    u2_mag = models.FloatField()

    u0_ang = models.FloatField()
    u1_ang = models.FloatField()
    u2_ang = models.FloatField()

    i0_mag = models.FloatField()
    i1_mag = models.FloatField()
    i2_mag = models.FloatField()

    i0_ang = models.FloatField()
    i1_ang = models.FloatField()
    i2_ang = models.FloatField()

    eff1 = models.FloatField()
    eff2 = models.FloatField()
    eff3 = models.FloatField()

    torque1 = models.FloatField()
    torque2 = models.FloatField()
    torque3 = models.FloatField()

    load1_percen = models.FloatField()
    load2_percen = models.FloatField()
    load3_percen = models.FloatField()

    load1_hp = models.FloatField()
    load2_hp = models.FloatField()
    load3_hp = models.FloatField()

    rpm = models.FloatField()
    db1 = models.FloatField()
    db2 = models.FloatField()
    db3 = models.FloatField()

    thd_v1 = models.FloatField()
    thd_v2 = models.FloatField()
    thd_v3 = models.FloatField()

    thdg_v1 = models.FloatField()
    thdg_v2 = models.FloatField()
    thdg_v3 = models.FloatField()

    thd_i1 = models.FloatField()
    thd_i2 = models.FloatField()
    thd_i3 = models.FloatField()

    thds_v1 = models.FloatField()
    thds_v2 = models.FloatField()
    thds_v3 = models.FloatField()

    vh1_v1 = models.FloatField()
    vh1_v2 = models.FloatField()
    vh1_v3 = models.FloatField()
    vh1_v4 = models.FloatField()
    vh1_v5 = models.FloatField()
    vh1_v6 = models.FloatField()
    vh1_v7 = models.FloatField()
    vh1_v8 = models.FloatField()
    vh1_v9 = models.FloatField()
    vh1_v10 = models.FloatField()
    vh1_v11 = models.FloatField()
    vh1_v12 = models.FloatField()
    vh1_v13 = models.FloatField()
    vh1_v14 = models.FloatField()
    vh1_v15 = models.FloatField()
    vh1_v16 = models.FloatField()
    vh1_v17 = models.FloatField()
    vh1_v18 = models.FloatField()
    vh1_v19 = models.FloatField()
    vh1_v20 = models.FloatField()
    vh1_v21 = models.FloatField()
    vh1_v22 = models.FloatField()
    vh1_v23 = models.FloatField()
    vh1_v24 = models.FloatField()
    vh1_v25 = models.FloatField()

    vh2_v1 = models.FloatField()
    vh2_v2 = models.FloatField()
    vh2_v3 = models.FloatField()
    vh2_v4 = models.FloatField()
    vh2_v5 = models.FloatField()
    vh2_v6 = models.FloatField()
    vh2_v7 = models.FloatField()
    vh2_v8 = models.FloatField()
    vh2_v9 = models.FloatField()
    vh2_v10 = models.FloatField()
    vh2_v11 = models.FloatField()
    vh2_v12 = models.FloatField()
    vh2_v13 = models.FloatField()
    vh2_v14 = models.FloatField()
    vh2_v15 = models.FloatField()
    vh2_v16 = models.FloatField()
    vh2_v17 = models.FloatField()
    vh2_v18 = models.FloatField()
    vh2_v19 = models.FloatField()
    vh2_v20 = models.FloatField()
    vh2_v21 = models.FloatField()
    vh2_v22 = models.FloatField()
    vh2_v23 = models.FloatField()
    vh2_v24 = models.FloatField()
    vh2_v25 = models.FloatField()

    vh3_v1 = models.FloatField()
    vh3_v2 = models.FloatField()
    vh3_v3 = models.FloatField()
    vh3_v4 = models.FloatField()
    vh3_v5 = models.FloatField()
    vh3_v6 = models.FloatField()
    vh3_v7 = models.FloatField()
    vh3_v8 = models.FloatField()
    vh3_v9 = models.FloatField()
    vh3_v10 = models.FloatField()
    vh3_v11 = models.FloatField()
    vh3_v12 = models.FloatField()
    vh3_v13 = models.FloatField()
    vh3_v14 = models.FloatField()
    vh3_v15 = models.FloatField()
    vh3_v16 = models.FloatField()
    vh3_v17 = models.FloatField()
    vh3_v18 = models.FloatField()
    vh3_v19 = models.FloatField()
    vh3_v20 = models.FloatField()
    vh3_v21 = models.FloatField()
    vh3_v22 = models.FloatField()
    vh3_v23 = models.FloatField()
    vh3_v24 = models.FloatField()
    vh3_v25 = models.FloatField()

    ih1_v1 = models.FloatField()
    ih1_v2 = models.FloatField()
    ih1_v3 = models.FloatField()
    ih1_v4 = models.FloatField()
    ih1_v5 = models.FloatField()
    ih1_v6 = models.FloatField()
    ih1_v7 = models.FloatField()
    ih1_v8 = models.FloatField()
    ih1_v9 = models.FloatField()
    ih1_v10 = models.FloatField()
    ih1_v11 = models.FloatField()
    ih1_v12 = models.FloatField()
    ih1_v13 = models.FloatField()
    ih1_v14 = models.FloatField()
    ih1_v15 = models.FloatField()
    ih1_v16 = models.FloatField()
    ih1_v17 = models.FloatField()
    ih1_v18 = models.FloatField()
    ih1_v19 = models.FloatField()
    ih1_v20 = models.FloatField()
    ih1_v21 = models.FloatField()
    ih1_v22 = models.FloatField()
    ih1_v23 = models.FloatField()
    ih1_v24 = models.FloatField()
    ih1_v25 = models.FloatField()

    ih2_v1 = models.FloatField()
    ih2_v2 = models.FloatField()
    ih2_v3 = models.FloatField()
    ih2_v4 = models.FloatField()
    ih2_v5 = models.FloatField()
    ih2_v6 = models.FloatField()
    ih2_v7 = models.FloatField()
    ih2_v8 = models.FloatField()
    ih2_v9 = models.FloatField()
    ih2_v10 = models.FloatField()
    ih2_v11 = models.FloatField()
    ih2_v12 = models.FloatField()
    ih2_v13 = models.FloatField()
    ih2_v14 = models.FloatField()
    ih2_v15 = models.FloatField()
    ih2_v16 = models.FloatField()
    ih2_v17 = models.FloatField()
    ih2_v18 = models.FloatField()
    ih2_v19 = models.FloatField()
    ih2_v20 = models.FloatField()
    ih2_v21 = models.FloatField()
    ih2_v22 = models.FloatField()
    ih2_v23 = models.FloatField()
    ih2_v24 = models.FloatField()
    ih2_v25 = models.FloatField()

    ih3_v1 = models.FloatField()
    ih3_v2 = models.FloatField()
    ih3_v3 = models.FloatField()
    ih3_v4 = models.FloatField()
    ih3_v5 = models.FloatField()
    ih3_v6 = models.FloatField()
    ih3_v7 = models.FloatField()
    ih3_v8 = models.FloatField()
    ih3_v9 = models.FloatField()
    ih3_v10 = models.FloatField()
    ih3_v11 = models.FloatField()
    ih3_v12 = models.FloatField()
    ih3_v13 = models.FloatField()
    ih3_v14 = models.FloatField()
    ih3_v15 = models.FloatField()
    ih3_v16 = models.FloatField()
    ih3_v17 = models.FloatField()
    ih3_v18 = models.FloatField()
    ih3_v19 = models.FloatField()
    ih3_v20 = models.FloatField()
    ih3_v21 = models.FloatField()
    ih3_v22 = models.FloatField()
    ih3_v23 = models.FloatField()
    ih3_v24 = models.FloatField()
    ih3_v25 = models.FloatField()
    class Meta:
        unique_together = ('test_re_nro', 'item')

    def __str__(self):
        return f"Medicion RE pk:{self.medicion_re_key} y test.pk:{self.test_re_nro}"


class MedicionTA(models.Model):
    medicion_ta_key = models.AutoField(primary_key=True)
    test_ta_nro = models.ForeignKey(TestTA, on_delete=models.CASCADE)
    item = models.IntegerField()
    time = models.FloatField()
    v1 = models.FloatField()
    v2 = models.FloatField()
    v3 = models.FloatField()
    i1 = models.FloatField()
    i2 = models.FloatField()
    i3 = models.FloatField()

    class Meta:
        unique_together = ('test_ta_nro', 'item')

