from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import F


class Engine(models.Model):
    engine_pk = models.AutoField(primary_key=True)
    #no deber ser unique -> 2 usuarios pueden crear un motod llamado "motor A", to do✅
    name = models.CharField(max_length=100, unique=True)
    power_out_hp = models.FloatField(decimal_places=2)
    power_out_kw = models.FloatField(decimal_places=2)
    voltage_rating = models.FloatField(decimal_places=2)
    speed_rpm = models.FloatField(decimal_places=2)
    amps_rating = models.FloatField(decimal_places=2)
    off_level = models.FloatField(decimal_places=2)
    frame = models.FloatField(decimal_places=2)
    insulation_class = models.FloatField(decimal_places=2)
    locked_rotor_current = models.FloatField(decimal_places=2)
    locked_rotor_code = models.FloatField(decimal_places=2)
    freq_hz = models.FloatField(decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # Si el objeto no tiene un id, entonces es nuevo y se está creando
        if not self.pk:
            super().save(*args, **kwargs)
            # Crear una instancia de R.E y T.A asociada a este Motor
            ElectricalResult.objects.create(engine_fk=self)
            TransientBoot.objects.create(engine_fk=self)
        else:
            super().save(*args, **kwargs)


class ElectricalResult(models.Model):
    electrical_result_pk = models.AutoField(primary_key=True)
    engine_fk = models.ForeignKey(Engine, on_delete=models.CASCADE)

class TransientBoot(models.Model):
    transient_boot_pk = models.AutoField(primary_key=True)
    engine_fk = models.ForeignKey(Engine, on_delete=models.CASCADE)

class TestER(models.Model):
    test_electrical_result_pk = models.AutoField(primary_key=True)
    electrical_result_fk = models.ForeignKey(
        ElectricalResult, on_delete=models.CASCADE)
    test_date_time = models.DateTimeField()

    def save(self, *args, **kwargs):
        if TestER.objects.filter(electrical_result_fk=self.electrical_result_fk,test_date_time=self.test_date_time).exists():
            raise ValidationError("Ya existe un archivo con la misma fecha para este TestRE")
        else:
            super().save(*args, **kwargs)

class TestTB(models.Model):
    test_transient_boot_pk = models.AutoField(primary_key=True)
    transient_boot_fk = models.ForeignKey(
        TransientBoot, on_delete=models.CASCADE)
    test_date_time = models.DateTimeField()

    def save(self, *args, **kwargs):
        if TestTB.objects.filter(transient_boot_fk=self.transient_boot_fk,test_date_time=self.test_date_time).exists():
            raise ValidationError("Ya existe un archivo con la misma fecha para este TestTA")
        else:
            super().save(*args, **kwargs)

class MeasurementER(models.Model):
    measurement_electrical_result_pk = models.AutoField(primary_key=True)
    test_electrical_result_fk = models.ForeignKey(TestER, on_delete=models.CASCADE)
    #item = models.IntegerField()
    time = models.DateTimeField()
    
    mag_v1 = models.FloatField(decimal_places=2)
    mag_v2 = models.FloatField(decimal_places=2)
    mag_v3 = models.FloatField(decimal_places=2)
    
    ang_v1 = models.FloatField(decimal_places=2)
    ang_v2 = models.FloatField(decimal_places=2)
    ang_v3 = models.FloatField(decimal_places=2)

    mag_i1 = models.FloatField(decimal_places=2)
    mag_i2 = models.FloatField(decimal_places=2)
    mag_i3 = models.FloatField(decimal_places=2)

    ang_i1 = models.FloatField(decimal_places=2)
    ang_i2 = models.FloatField(decimal_places=2)
    ang_i3 = models.FloatField(decimal_places=2)

    v1_freq = models.FloatField(decimal_places=2)
    v2_freq = models.FloatField(decimal_places=2)
    v3_freq = models.FloatField(decimal_places=2)

    pf1_1 = models.FloatField(decimal_places=2)
    pf2_2 = models.FloatField(decimal_places=2)
    pf3_3 = models.FloatField(decimal_places=2)

    kw_1 = models.FloatField(decimal_places=2)
    kw_2 = models.FloatField(decimal_places=2)
    kw_3 = models.FloatField(decimal_places=2)

    kvar_1 = models.FloatField(decimal_places=2)
    kvar_2 = models.FloatField(decimal_places=2)
    kvar_3 = models.FloatField(decimal_places=2)

    ks_1 = models.FloatField(decimal_places=2)
    ks_2 = models.FloatField(decimal_places=2)
    ks_3 = models.FloatField(decimal_places=2)

    ckwh_1 = models.FloatField(decimal_places=2)
    ckwh_2 = models.FloatField(decimal_places=2)
    ckwh_3 = models.FloatField(decimal_places=2)

    lsskw_1 = models.FloatField(decimal_places=2)
    lsskw_2 = models.FloatField(decimal_places=2)
    lsskw_3 = models.FloatField(decimal_places=2)

    dv_u2 = models.FloatField(decimal_places=2)
    dv_u0 = models.FloatField(decimal_places=2)
    dvf_u2 = models.FloatField(decimal_places=2)
    dvf_u0 = models.FloatField(decimal_places=2)

    di_u2 = models.FloatField(decimal_places=2)
    di_u0 = models.FloatField(decimal_places=2)
    dif_u2 = models.FloatField(decimal_places=2)
    dif_u0 = models.FloatField(decimal_places=2)

    u0_mag = models.FloatField(decimal_places=2)
    u1_mag = models.FloatField(decimal_places=2)
    u2_mag = models.FloatField(decimal_places=2)

    u0_ang = models.FloatField(decimal_places=2)
    u1_ang = models.FloatField(decimal_places=2)
    u2_ang = models.FloatField(decimal_places=2)

    i0_mag = models.FloatField(decimal_places=2)
    i1_mag = models.FloatField(decimal_places=2)
    i2_mag = models.FloatField(decimal_places=2)

    i0_ang = models.FloatField(decimal_places=2)
    i1_ang = models.FloatField(decimal_places=2)
    i2_ang = models.FloatField(decimal_places=2)

    eff1 = models.FloatField(decimal_places=2)
    eff2 = models.FloatField(decimal_places=2)
    eff3 = models.FloatField(decimal_places=2)

    torque1 = models.FloatField(decimal_places=2)
    torque2 = models.FloatField(decimal_places=2)
    torque3 = models.FloatField(decimal_places=2)

    load1_percen = models.FloatField(decimal_places=2)
    load2_percen = models.FloatField(decimal_places=2)
    load3_percen = models.FloatField(decimal_places=2)

    load1_hp = models.FloatField(decimal_places=2)
    load2_hp = models.FloatField(decimal_places=2)
    load3_hp = models.FloatField(decimal_places=2)

    rpm = models.FloatField(decimal_places=2)
    db1 = models.FloatField(decimal_places=2)
    db2 = models.FloatField(decimal_places=2)
    db3 = models.FloatField(decimal_places=2)

    thd_v1 = models.FloatField(decimal_places=2)
    thd_v2 = models.FloatField(decimal_places=2)
    thd_v3 = models.FloatField(decimal_places=2)

    thdg_v1 = models.FloatField(decimal_places=2)
    thdg_v2 = models.FloatField(decimal_places=2)
    thdg_v3 = models.FloatField(decimal_places=2)

    thd_i1 = models.FloatField(decimal_places=2)
    thd_i2 = models.FloatField(decimal_places=2)
    thd_i3 = models.FloatField(decimal_places=2)

    thds_v1 = models.FloatField(decimal_places=2)
    thds_v2 = models.FloatField(decimal_places=2)
    thds_v3 = models.FloatField(decimal_places=2)

    vh1_v1 = models.FloatField(decimal_places=2)
    vh1_v2 = models.FloatField(decimal_places=2)
    vh1_v3 = models.FloatField(decimal_places=2)
    vh1_v4 = models.FloatField(decimal_places=2)
    vh1_v5 = models.FloatField(decimal_places=2)
    vh1_v6 = models.FloatField(decimal_places=2)
    vh1_v7 = models.FloatField(decimal_places=2)
    vh1_v8 = models.FloatField(decimal_places=2)
    vh1_v9 = models.FloatField(decimal_places=2)
    vh1_v10 = models.FloatField(decimal_places=2)
    vh1_v11 = models.FloatField(decimal_places=2)
    vh1_v12 = models.FloatField(decimal_places=2)
    vh1_v13 = models.FloatField(decimal_places=2)
    vh1_v14 = models.FloatField(decimal_places=2)
    vh1_v15 = models.FloatField(decimal_places=2)
    vh1_v16 = models.FloatField(decimal_places=2)
    vh1_v17 = models.FloatField(decimal_places=2)
    vh1_v18 = models.FloatField(decimal_places=2)
    vh1_v19 = models.FloatField(decimal_places=2)
    vh1_v20 = models.FloatField(decimal_places=2)
    vh1_v21 = models.FloatField(decimal_places=2)
    vh1_v22 = models.FloatField(decimal_places=2)
    vh1_v23 = models.FloatField(decimal_places=2)
    vh1_v24 = models.FloatField(decimal_places=2)
    vh1_v25 = models.FloatField(decimal_places=2)

    vh2_v1 = models.FloatField(decimal_places=2)
    vh2_v2 = models.FloatField(decimal_places=2)
    vh2_v3 = models.FloatField(decimal_places=2)
    vh2_v4 = models.FloatField(decimal_places=2)
    vh2_v5 = models.FloatField(decimal_places=2)
    vh2_v6 = models.FloatField(decimal_places=2)
    vh2_v7 = models.FloatField(decimal_places=2)
    vh2_v8 = models.FloatField(decimal_places=2)
    vh2_v9 = models.FloatField(decimal_places=2)
    vh2_v10 = models.FloatField(decimal_places=2)
    vh2_v11 = models.FloatField(decimal_places=2)
    vh2_v12 = models.FloatField(decimal_places=2)
    vh2_v13 = models.FloatField(decimal_places=2)
    vh2_v14 = models.FloatField(decimal_places=2)
    vh2_v15 = models.FloatField(decimal_places=2)
    vh2_v16 = models.FloatField(decimal_places=2)
    vh2_v17 = models.FloatField(decimal_places=2)
    vh2_v18 = models.FloatField(decimal_places=2)
    vh2_v19 = models.FloatField(decimal_places=2)
    vh2_v20 = models.FloatField(decimal_places=2)
    vh2_v21 = models.FloatField(decimal_places=2)
    vh2_v22 = models.FloatField(decimal_places=2)
    vh2_v23 = models.FloatField(decimal_places=2)
    vh2_v24 = models.FloatField(decimal_places=2)
    vh2_v25 = models.FloatField(decimal_places=2)

    vh3_v1 = models.FloatField(decimal_places=2)
    vh3_v2 = models.FloatField(decimal_places=2)
    vh3_v3 = models.FloatField(decimal_places=2)
    vh3_v4 = models.FloatField(decimal_places=2)
    vh3_v5 = models.FloatField(decimal_places=2)
    vh3_v6 = models.FloatField(decimal_places=2)
    vh3_v7 = models.FloatField(decimal_places=2)
    vh3_v8 = models.FloatField(decimal_places=2)
    vh3_v9 = models.FloatField(decimal_places=2)
    vh3_v10 = models.FloatField(decimal_places=2)
    vh3_v11 = models.FloatField(decimal_places=2)
    vh3_v12 = models.FloatField(decimal_places=2)
    vh3_v13 = models.FloatField(decimal_places=2)
    vh3_v14 = models.FloatField(decimal_places=2)
    vh3_v15 = models.FloatField(decimal_places=2)
    vh3_v16 = models.FloatField(decimal_places=2)
    vh3_v17 = models.FloatField(decimal_places=2)
    vh3_v18 = models.FloatField(decimal_places=2)
    vh3_v19 = models.FloatField(decimal_places=2)
    vh3_v20 = models.FloatField(decimal_places=2)
    vh3_v21 = models.FloatField(decimal_places=2)
    vh3_v22 = models.FloatField(decimal_places=2)
    vh3_v23 = models.FloatField(decimal_places=2)
    vh3_v24 = models.FloatField(decimal_places=2)
    vh3_v25 = models.FloatField(decimal_places=2)

    ih1_v1 = models.FloatField(decimal_places=2)
    ih1_v2 = models.FloatField(decimal_places=2)
    ih1_v3 = models.FloatField(decimal_places=2)
    ih1_v4 = models.FloatField(decimal_places=2)
    ih1_v5 = models.FloatField(decimal_places=2)
    ih1_v6 = models.FloatField(decimal_places=2)
    ih1_v7 = models.FloatField(decimal_places=2)
    ih1_v8 = models.FloatField(decimal_places=2)
    ih1_v9 = models.FloatField(decimal_places=2)
    ih1_v10 = models.FloatField(decimal_places=2)
    ih1_v11 = models.FloatField(decimal_places=2)
    ih1_v12 = models.FloatField(decimal_places=2)
    ih1_v13 = models.FloatField(decimal_places=2)
    ih1_v14 = models.FloatField(decimal_places=2)
    ih1_v15 = models.FloatField(decimal_places=2)
    ih1_v16 = models.FloatField(decimal_places=2)
    ih1_v17 = models.FloatField(decimal_places=2)
    ih1_v18 = models.FloatField(decimal_places=2)
    ih1_v19 = models.FloatField(decimal_places=2)
    ih1_v20 = models.FloatField(decimal_places=2)
    ih1_v21 = models.FloatField(decimal_places=2)
    ih1_v22 = models.FloatField(decimal_places=2)
    ih1_v23 = models.FloatField(decimal_places=2)
    ih1_v24 = models.FloatField(decimal_places=2)
    ih1_v25 = models.FloatField(decimal_places=2)

    ih2_v1 = models.FloatField(decimal_places=2)
    ih2_v2 = models.FloatField(decimal_places=2)
    ih2_v3 = models.FloatField(decimal_places=2)
    ih2_v4 = models.FloatField(decimal_places=2)
    ih2_v5 = models.FloatField(decimal_places=2)
    ih2_v6 = models.FloatField(decimal_places=2)
    ih2_v7 = models.FloatField(decimal_places=2)
    ih2_v8 = models.FloatField(decimal_places=2)
    ih2_v9 = models.FloatField(decimal_places=2)
    ih2_v10 = models.FloatField(decimal_places=2)
    ih2_v11 = models.FloatField(decimal_places=2)
    ih2_v12 = models.FloatField(decimal_places=2)
    ih2_v13 = models.FloatField(decimal_places=2)
    ih2_v14 = models.FloatField(decimal_places=2)
    ih2_v15 = models.FloatField(decimal_places=2)
    ih2_v16 = models.FloatField(decimal_places=2)
    ih2_v17 = models.FloatField(decimal_places=2)
    ih2_v18 = models.FloatField(decimal_places=2)
    ih2_v19 = models.FloatField(decimal_places=2)
    ih2_v20 = models.FloatField(decimal_places=2)
    ih2_v21 = models.FloatField(decimal_places=2)
    ih2_v22 = models.FloatField(decimal_places=2)
    ih2_v23 = models.FloatField(decimal_places=2)
    ih2_v24 = models.FloatField(decimal_places=2)
    ih2_v25 = models.FloatField(decimal_places=2)

    ih3_v1 = models.FloatField(decimal_places=2)
    ih3_v2 = models.FloatField(decimal_places=2)
    ih3_v3 = models.FloatField(decimal_places=2)
    ih3_v4 = models.FloatField(decimal_places=2)
    ih3_v5 = models.FloatField(decimal_places=2)
    ih3_v6 = models.FloatField(decimal_places=2)
    ih3_v7 = models.FloatField(decimal_places=2)
    ih3_v8 = models.FloatField(decimal_places=2)
    ih3_v9 = models.FloatField(decimal_places=2)
    ih3_v10 = models.FloatField(decimal_places=2)
    ih3_v11 = models.FloatField(decimal_places=2)
    ih3_v12 = models.FloatField(decimal_places=2)
    ih3_v13 = models.FloatField(decimal_places=2)
    ih3_v14 = models.FloatField(decimal_places=2)
    ih3_v15 = models.FloatField(decimal_places=2)
    ih3_v16 = models.FloatField(decimal_places=2)
    ih3_v17 = models.FloatField(decimal_places=2)
    ih3_v18 = models.FloatField(decimal_places=2)
    ih3_v19 = models.FloatField(decimal_places=2)
    ih3_v20 = models.FloatField(decimal_places=2)
    ih3_v21 = models.FloatField(decimal_places=2)
    ih3_v22 = models.FloatField(decimal_places=2)
    ih3_v23 = models.FloatField(decimal_places=2)
    ih3_v24 = models.FloatField(decimal_places=2)
    ih3_v25 = models.FloatField(decimal_places=2)
    # class Meta:
    #     unique_together = ('test_electrical_result_fk', 'item')

    def __str__(self):
        return {self.measurement_electrical_result_pk,self.ang_i1, self.ckwh_1}


class MeasurementTB(models.Model):
    measurement_transient_boot_pk = models.AutoField(primary_key=True)
    test_transient_boot_fk = models.ForeignKey(TestTB, on_delete=models.CASCADE)
    #item = models.IntegerField()
    time = models.FloatField(decimal_places=2)
    ia = models.FloatField(decimal_places=2)
    ib = models.FloatField(decimal_places=2)
    ic = models.FloatField(decimal_places=2)
    va = models.FloatField(decimal_places=2)
    vb = models.FloatField(decimal_places=2)
    vc = models.FloatField(decimal_places=2)
    #class Meta:
    #    unique_together = ('test_transient_boot_fk', 'item')

class AverageMeasurement(models.Model):
    average_measurement_pk = models.AutoField(primary_key=True)
    test_electrical_result_fk = models.OneToOneField(TestER, on_delete=models.CASCADE)
    #voltage
    ab = models.FloatField(decimal_places=2)
    bc = models.FloatField(decimal_places=2)
    ca = models.FloatField(decimal_places=2)
    avg = models.FloatField(decimal_places=2)
    value = models.FloatField(decimal_places=2)
    #unbalance
    unbalance = models.FloatField(decimal_places=2)
    #distorsion
    thdv_a = models.FloatField(decimal_places=2)
    thdv_b = models.FloatField(decimal_places=2)
    thdv_c = models.FloatField(decimal_places=2)
    thdv_avg = models.FloatField(decimal_places=2)
    thdi_a = models.FloatField(decimal_places=2)
    thdi_b = models.FloatField(decimal_places=2)
    thdi_c = models.FloatField(decimal_places=2)
    thdi_avg = models.FloatField(decimal_places=2)
    #full_distorsion
    tdv_a = models.FloatField(decimal_places=2)
    tdv_b = models.FloatField(decimal_places=2)
    tdv_c = models.FloatField(decimal_places=2)
    tdv_avg = models.FloatField(decimal_places=2)
    tdi_a = models.FloatField(decimal_places=2)
    tdi_b = models.FloatField(decimal_places=2)
    tdi_c = models.FloatField(decimal_places=2)
    tdi_avg = models.FloatField(decimal_places=2)
    #CurrentLevel
    current_a = models.FloatField(decimal_places=2)
    current_b = models.FloatField(decimal_places=2)
    current_c = models.FloatField(decimal_places=2)
    current_avg = models.FloatField(decimal_places=2)
    current_nominal = models.FloatField(decimal_places=2)
    #currentUnbalance
    current_unbalance = models.FloatField(decimal_places=2)
    #efficiency
    load_percen_avg = models.FloatField(decimal_places=2)
    lsskw_avg = models.FloatField(decimal_places=2)
    eff_avg = models.FloatField(decimal_places=2)
    #spectrum
    sideband_amplitud_db = models.FloatField(decimal_places=2)
    sideband_freq_hz = models.FloatField(decimal_places=2)
    #symetrical components
    vab_fase = models.FloatField(decimal_places=2)
    vbc_fase = models.FloatField(decimal_places=2)
    vca_fase = models.FloatField(decimal_places=2)
    unbalance_voltage = models.FloatField(decimal_places=2)
    va1_amplitud = models.FloatField(decimal_places=2)
    va2_amplitud = models.FloatField(decimal_places=2)
    va1_fase = models.FloatField(decimal_places=2)
    va2_fase = models.FloatField(decimal_places=2)
    ia_fase = models.FloatField(decimal_places=2)
    ib_fase = models.FloatField(decimal_places=2)
    ic_fase = models.FloatField(decimal_places=2)
    unbalance_current = models.FloatField(decimal_places=2)
    ia1_amplitud = models.FloatField(decimal_places=2)
    ia2_amplitud = models.FloatField(decimal_places=2)
    ia1_fase = models.FloatField(decimal_places=2)
    ia2_fase = models.FloatField(decimal_places=2)