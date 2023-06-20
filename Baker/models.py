from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import F


class Engine(models.Model):
    engine_pk = models.AutoField(primary_key=True)
    # no deber ser unique -> 2 usuarios pueden crear un motod llamado "motor A", to do✅
    name = models.CharField(max_length=100)
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
    engine_fk = models.OneToOneField(Engine, on_delete=models.CASCADE)


class TransientBoot(models.Model):
    transient_boot_pk = models.AutoField(primary_key=True)
    engine_fk = models.OneToOneField(Engine, on_delete=models.CASCADE)


class TestER(models.Model):
    test_electrical_result_pk = models.AutoField(primary_key=True)
    electrical_result_fk = models.ForeignKey(
        ElectricalResult, on_delete=models.CASCADE)
    test_date_time = models.DateTimeField()

    def save(self, *args, **kwargs):
        if TestER.objects.filter(electrical_result_fk=self.electrical_result_fk, test_date_time=self.test_date_time).exists():
            raise ValidationError(
                "Ya existe un archivo con la misma fecha para este TestRE")
        else:
            super().save(*args, **kwargs)


class TestTB(models.Model):
    test_transient_boot_pk = models.AutoField(primary_key=True)
    transient_boot_fk = models.ForeignKey(
        TransientBoot, on_delete=models.CASCADE)
    test_date_time = models.DateTimeField()

    def save(self, *args, **kwargs):
        if TestTB.objects.filter(transient_boot_fk=self.transient_boot_fk, test_date_time=self.test_date_time).exists():
            raise ValidationError(
                "Ya existe un archivo con la misma fecha para este TestTA")
        else:
            super().save(*args, **kwargs)


class MeasurementER(models.Model):
    measurement_electrical_result_pk = models.AutoField(primary_key=True)
    test_electrical_result_fk = models.ForeignKey(
        TestER, on_delete=models.CASCADE)
    # item = models.IntegerField()
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
    # class Meta:
    #     unique_together = ('test_electrical_result_fk', 'item')

    def __str__(self):
        attrs = ', '.join(f'{attr}={value}' for attr,
                          value in vars(self).items())
        return f"MeasurementER({attrs})"


class MeasurementTB(models.Model):
    measurement_transient_boot_pk = models.AutoField(primary_key=True)
    test_transient_boot_fk = models.ForeignKey(
        TestTB, on_delete=models.CASCADE)
    # item = models.IntegerField()
    time = models.FloatField()
    ia = models.FloatField()
    ib = models.FloatField()
    ic = models.FloatField()
    va = models.FloatField()
    vb = models.FloatField()
    vc = models.FloatField()
    # class Meta:
    #    unique_together = ('test_transient_boot_fk', 'item')


class AverageMeasurement(models.Model):
    average_measurement_pk = models.AutoField(primary_key=True)
    test_electrical_result_fk = models.OneToOneField(
        TestER, on_delete=models.CASCADE)
    # voltage
    ab = models.FloatField()
    bc = models.FloatField()
    ca = models.FloatField()
    avg = models.FloatField()
    value = models.FloatField()
    # unbalance
    unbalance = models.FloatField()
    # distorsion
    thdv_a = models.FloatField()
    thdv_b = models.FloatField()
    thdv_c = models.FloatField()
    thdv_avg = models.FloatField()
    thdi_a = models.FloatField()
    thdi_b = models.FloatField()
    thdi_c = models.FloatField()
    thdi_avg = models.FloatField()
    # full_distorsion
    tdv_a = models.FloatField()
    tdv_b = models.FloatField()
    tdv_c = models.FloatField()
    tdv_avg = models.FloatField()
    tdi_a = models.FloatField()
    tdi_b = models.FloatField()
    tdi_c = models.FloatField()
    tdi_avg = models.FloatField()
    # CurrentLevel
    current_a = models.FloatField()
    current_b = models.FloatField()
    current_c = models.FloatField()
    current_avg = models.FloatField()
    current_nominal = models.FloatField()
    # currentUnbalance
    current_unbalance = models.FloatField()
    # efficiency
    load_percen_avg = models.FloatField()
    lsskw_avg = models.FloatField()
    eff_avg = models.FloatField()
    # spectrum
    sideband_amplitud_db = models.FloatField()
    sideband_freq_hz = models.FloatField()
    # symetrical components
    vab_fase = models.FloatField()
    vbc_fase = models.FloatField()
    vca_fase = models.FloatField()
    unbalance_voltage = models.FloatField()
    va1_amplitud = models.FloatField()
    va2_amplitud = models.FloatField()
    va1_fase = models.FloatField()
    va2_fase = models.FloatField()
    ia_fase = models.FloatField()
    ib_fase = models.FloatField()
    ic_fase = models.FloatField()
    unbalance_current = models.FloatField()
    ia1_amplitud = models.FloatField()
    ia2_amplitud = models.FloatField()
    ia1_fase = models.FloatField()
    ia2_fase = models.FloatField()
    # energia
    kw_a = models.FloatField()
    kw_b = models.FloatField()
    kw_c = models.FloatField()
    kw_avg = models.FloatField()
    kvar_a = models.FloatField()
    kvar_b = models.FloatField()
    kvar_c = models.FloatField()
    kvar_avg = models.FloatField()
    kva_a = models.FloatField()
    kva_b = models.FloatField()
    kva_c = models.FloatField()
    kva_avg = models.FloatField()
    pf_a = models.FloatField()
    pf_b = models.FloatField()
    pf_c = models.FloatField()
    pf_avg = models.FloatField()
    #
    torque = models.FloatField()
