from django.db import transaction
from .models import MeasurementER, MeasurementTB, TestER, TestTB, AverageMeasurement, Engine, ElectricalResult
from .serializers import MeasurementERSerializer, MeasurementTBSerializer
from django.core.exceptions import ValidationError
import numpy as np
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from math import pi
# ----------------------------------------------- método con hilos ----------------------------------------------


def create_objects(data, size):
    obj = data[0]
    if isinstance(obj, MeasurementER):
        MeasurementER.objects.bulk_create(data, batch_size=size)
    if isinstance(obj, MeasurementTB):
        MeasurementTB.objects.bulk_create(data, batch_size=size)


def data_vectorized(fila, test):
    if isinstance(test, TestER):
        try:
            objeto = MeasurementER(test_electrical_result_fk=test,
                                   # item=fila[0],
                                   time=fila[1],
                                   mag_v1=fila[2],
                                   mag_v2=fila[3],
                                   mag_v3=fila[4],
                                   ang_v1=fila[5],
                                   ang_v2=fila[6],
                                   ang_v3=fila[7],
                                   mag_i1=fila[8],
                                   mag_i2=fila[9],
                                   mag_i3=fila[10],
                                   ang_i1=fila[11],
                                   ang_i2=fila[12],
                                   ang_i3=fila[13],
                                   v1_freq=fila[14],
                                   v2_freq=fila[15],
                                   v3_freq=fila[16],
                                   pf1_1=fila[17],
                                   pf2_2=fila[18],
                                   pf3_3=fila[19],
                                   kw_1=fila[20],
                                   kw_2=fila[21],
                                   kw_3=fila[22],
                                   kvar_1=fila[23],
                                   kvar_2=fila[24],
                                   kvar_3=fila[25],
                                   ks_1=fila[26],
                                   ks_2=fila[27],
                                   ks_3=fila[28],
                                   ckwh_1=fila[29],
                                   ckwh_2=fila[30],
                                   ckwh_3=fila[31],
                                   lsskw_1=fila[32],
                                   lsskw_2=fila[33],
                                   lsskw_3=fila[34],
                                   dv_u2=fila[35],
                                   dv_u0=fila[36],
                                   dvf_u2=fila[37],
                                   dvf_u0=fila[38],
                                   di_u2=fila[39],
                                   di_u0=fila[40],
                                   dif_u2=fila[41],
                                   dif_u0=fila[42],
                                   u0_mag=fila[43],
                                   u1_mag=fila[44],
                                   u2_mag=fila[45],
                                   u0_ang=fila[46],
                                   u1_ang=fila[47],
                                   u2_ang=fila[48],
                                   i0_mag=fila[49],
                                   i1_mag=fila[50],
                                   i2_mag=fila[51],
                                   i0_ang=fila[52],
                                   i1_ang=fila[53],
                                   i2_ang=fila[54],
                                   eff1=fila[55],
                                   eff2=fila[56],
                                   eff3=fila[57],
                                   torque1=fila[58],
                                   torque2=fila[59],
                                   torque3=fila[60],
                                   load1_percen=fila[61],
                                   load2_percen=fila[62],
                                   load3_percen=fila[63],
                                   load1_hp=fila[64],
                                   load2_hp=fila[65],
                                   load3_hp=fila[66],
                                   rpm=fila[67],
                                   db1=fila[68],
                                   db2=fila[69],
                                   db3=fila[70],
                                   thd_v1=fila[71],
                                   thd_v2=fila[72],
                                   thd_v3=fila[73],
                                   thdg_v1=fila[74],
                                   thdg_v2=fila[75],
                                   thdg_v3=fila[76],
                                   thd_i1=fila[77],
                                   thd_i2=fila[78],
                                   thd_i3=fila[79],
                                   thds_v1=fila[80],
                                   thds_v2=fila[81],
                                   thds_v3=fila[82],
                                   vh1_v1=fila[83],
                                   vh1_v2=fila[84],
                                   vh1_v3=fila[85],
                                   vh1_v4=fila[86],
                                   vh1_v5=fila[87],
                                   vh1_v6=fila[88],
                                   vh1_v7=fila[89],
                                   vh1_v8=fila[90],
                                   vh1_v9=fila[91],
                                   vh1_v10=fila[92],
                                   vh1_v11=fila[93],
                                   vh1_v12=fila[94],
                                   vh1_v13=fila[95],
                                   vh1_v14=fila[96],
                                   vh1_v15=fila[97],
                                   vh1_v16=fila[98],
                                   vh1_v17=fila[99],
                                   vh1_v18=fila[100],
                                   vh1_v19=fila[101],
                                   vh1_v20=fila[102],
                                   vh1_v21=fila[103],
                                   vh1_v22=fila[104],
                                   vh1_v23=fila[105],
                                   vh1_v24=fila[106],
                                   vh1_v25=fila[107],
                                   vh2_v1=fila[108],
                                   vh2_v2=fila[109],
                                   vh2_v3=fila[110],
                                   vh2_v4=fila[111],
                                   vh2_v5=fila[112],
                                   vh2_v6=fila[113],
                                   vh2_v7=fila[114],
                                   vh2_v8=fila[115],
                                   vh2_v9=fila[116],
                                   vh2_v10=fila[117],
                                   vh2_v11=fila[118],
                                   vh2_v12=fila[119],
                                   vh2_v13=fila[120],
                                   vh2_v14=fila[121],
                                   vh2_v15=fila[122],
                                   vh2_v16=fila[123],
                                   vh2_v17=fila[124],
                                   vh2_v18=fila[125],
                                   vh2_v19=fila[126],
                                   vh2_v20=fila[127],
                                   vh2_v21=fila[128],
                                   vh2_v22=fila[129],
                                   vh2_v23=fila[130],
                                   vh2_v24=fila[131],
                                   vh2_v25=fila[132],
                                   vh3_v1=fila[133],
                                   vh3_v2=fila[134],
                                   vh3_v3=fila[135],
                                   vh3_v4=fila[136],
                                   vh3_v5=fila[137],
                                   vh3_v6=fila[138],
                                   vh3_v7=fila[139],
                                   vh3_v8=fila[140],
                                   vh3_v9=fila[141],
                                   vh3_v10=fila[142],
                                   vh3_v11=fila[143],
                                   vh3_v12=fila[144],
                                   vh3_v13=fila[145],
                                   vh3_v14=fila[146],
                                   vh3_v15=fila[147],
                                   vh3_v16=fila[148],
                                   vh3_v17=fila[149],
                                   vh3_v18=fila[150],
                                   vh3_v19=fila[151],
                                   vh3_v20=fila[152],
                                   vh3_v21=fila[153],
                                   vh3_v22=fila[154],
                                   vh3_v23=fila[155],
                                   vh3_v24=fila[156],
                                   vh3_v25=fila[157],
                                   ih1_v1=fila[158],
                                   ih1_v2=fila[159],
                                   ih1_v3=fila[160],
                                   ih1_v4=fila[161],
                                   ih1_v5=fila[162],
                                   ih1_v6=fila[163],
                                   ih1_v7=fila[164],
                                   ih1_v8=fila[165],
                                   ih1_v9=fila[166],
                                   ih1_v10=fila[167],
                                   ih1_v11=fila[168],
                                   ih1_v12=fila[169],
                                   ih1_v13=fila[170],
                                   ih1_v14=fila[171],
                                   ih1_v15=fila[172],
                                   ih1_v16=fila[173],
                                   ih1_v17=fila[174],
                                   ih1_v18=fila[175],
                                   ih1_v19=fila[176],
                                   ih1_v20=fila[177],
                                   ih1_v21=fila[178],
                                   ih1_v22=fila[179],
                                   ih1_v23=fila[180],
                                   ih1_v24=fila[181],
                                   ih1_v25=fila[182],
                                   ih2_v1=fila[183],
                                   ih2_v2=fila[184],
                                   ih2_v3=fila[185],
                                   ih2_v4=fila[186],
                                   ih2_v5=fila[187],
                                   ih2_v6=fila[188],
                                   ih2_v7=fila[189],
                                   ih2_v8=fila[190],
                                   ih2_v9=fila[191],
                                   ih2_v10=fila[192],
                                   ih2_v11=fila[193],
                                   ih2_v12=fila[194],
                                   ih2_v13=fila[195],
                                   ih2_v14=fila[196],
                                   ih2_v15=fila[197],
                                   ih2_v16=fila[198],
                                   ih2_v17=fila[199],
                                   ih2_v18=fila[200],
                                   ih2_v19=fila[201],
                                   ih2_v20=fila[202],
                                   ih2_v21=fila[203],
                                   ih2_v22=fila[204],
                                   ih2_v23=fila[205],
                                   ih2_v24=fila[206],
                                   ih2_v25=fila[207],
                                   ih3_v1=fila[208],
                                   ih3_v2=fila[209],
                                   ih3_v3=fila[210],
                                   ih3_v4=fila[211],
                                   ih3_v5=fila[212],
                                   ih3_v6=fila[213],
                                   ih3_v7=fila[214],
                                   ih3_v8=fila[215],
                                   ih3_v9=fila[216],
                                   ih3_v10=fila[217],
                                   ih3_v11=fila[218],
                                   ih3_v12=fila[219],
                                   ih3_v13=fila[220],
                                   ih3_v14=fila[221],
                                   ih3_v15=fila[222],
                                   ih3_v16=fila[223],
                                   ih3_v17=fila[224],
                                   ih3_v18=fila[225],
                                   ih3_v19=fila[226],
                                   ih3_v20=fila[227],
                                   ih3_v21=fila[228],
                                   ih3_v22=fila[229],
                                   ih3_v23=fila[230],
                                   ih3_v24=fila[231],
                                   ih3_v25=fila[232])
            objeto.full_clean()  # Valida la instancia sin excluir ningún campo
            return objeto
        except:
            return

    if isinstance(test, TestTB):
        try:
            objeto = MeasurementTB(test_transient_boot_fk=test,
                                   time=fila[0],
                                   ia=fila[1],
                                   ib=fila[2],
                                   ic=fila[3],
                                   va=fila[4],
                                   vb=fila[5],
                                   vc=fila[6])
            # objeto.full_clean()
            return objeto
        except:
            return


def process_array(args):
    data, test_m = args
    string = "Measurmente TB"
    if isinstance(test_m, TestER):
        string = "Measurement ER"

    resultado = np.apply_along_axis(
        data_vectorized, axis=1, arr=data, test=test_m)
    if None in resultado:
        raise ValidationError(
            f"Something went wrong when creating an instance of {string}")
    resultado_list = resultado.tolist()
    size = (len(resultado_list)//2)
    create_objects(resultado_list, size)


def data_avarage(array, electrical_result_fk):
    electrical_result = ElectricalResult.objects.get(pk=electrical_result_fk)
    rated = electrical_result.engine_fk.voltage_rating
    rpm = electrical_result.engine_fk.speed_rpm
    # voltage
    ab = np.mean(array[:, 2])
    bc = np.mean(array[:, 3])
    ca = np.mean(array[:, 4])
    avg = (ab+bc+ca)/3
    value = (avg/rated)*100
    # distorsion
    thdv_a = np.mean(array[:, 71])
    thdv_b = np.mean(array[:, 72])
    thdv_c = np.mean(array[:, 73])
    thdv_avg = (thdv_a+thdv_b+thdv_c)/3
    thdi_a = np.mean(array[:, 77])
    thdi_b = np.mean(array[:, 78])
    thdi_c = np.mean(array[:, 79])
    thdi_avg = (thdi_a+thdi_b+thdi_c)/3
    # diu unbalance
    di_u2 = array[:, 39]
    di_u0 = array[:, 40]
    division_array = di_u2/di_u0
    unbalance = np.mean(division_array)
    # fulldistorsion
    tdv_a = np.mean(array[:, 74])
    tdv_b = np.mean(array[:, 75])
    tdv_c = np.mean(array[:, 76])
    tdv_avg = (tdv_a+tdv_b+tdv_c)/3
    tdi_a = np.mean(array[:, 80])
    tdi_b = np.mean(array[:, 81])
    tdi_c = np.mean(array[:, 82])
    tdi_avg = (tdi_a+tdi_b+tdi_c)/3
    # curentLevel
    current_a = np.mean(array[:, 8])
    current_b = np.mean(array[:, 9])
    current_c = np.mean(array[:, 10])
    current_avg = (current_a+current_b+current_c)/3
    current_nominal = (current_avg/rated)
    # currentUnbalance
    di_u2 = array[:, 39]
    di_u0 = array[:, 40]
    current_unbalance = np.mean(di_u0/di_u2)
    # efficiency
    load1_percen = np.mean(array[:, 61])
    load2_percen = np.mean(array[:, 62])
    load3_percen = np.mean(array[:, 63])
    load_percen_avg = (load1_percen+load2_percen+load3_percen)/3
    lsskw_1 = np.mean(array[:, 32])
    lsskw_2 = np.mean(array[:, 33])
    lsskw_3 = np.mean(array[:, 34])
    lsskw_avg = (lsskw_1+lsskw_2+lsskw_3)/3
    eff1 = np.mean(array[:, 55])
    eff2 = np.mean(array[:, 56])
    eff3 = np.mean(array[:, 57])
    eff_avg = (eff1+eff2+eff3)/3
    # load
    # spectrum
    db1 = np.mean(array[:, 68])
    db2 = np.mean(array[:, 69])
    db3 = np.mean(array[:, 70])
    sideband_amplitud_db = (db1 + db2 + db3)/3
    v1_freq = np.mean(array[:, 14])
    v2_freq = np.mean(array[:, 15])
    v3_freq = np.mean(array[:, 16])
    sideband_freq_hz = (v1_freq + v2_freq + v3_freq)/3
    # symetrical components
    vab_fase = np.mean(array[:, 5])
    vbc_fase = np.mean(array[:, 6])
    vca_fase = np.mean(array[:, 7])
    u0_mag = np.mean(array[:, 43])
    u2_mag = np.mean(array[:, 45])
    unbalance_voltage = np.mean(u0_mag/u2_mag)
    va1_amplitud = np.mean(array[:, 44])
    va2_amplitud = np.mean(array[:, 45])
    va1_fase = np.mean(array[:, 47])
    va2_fase = np.mean(array[:, 48])
    ia_fase = np.mean(array[:, 11])
    ib_fase = np.mean(array[:, 12])
    ic_fase = np.mean(array[:, 13])
    i0_mag = np.mean(array[:, 49])
    i2_mag = np.mean(array[:, 51])
    unbalance_current = np.mean(i0_mag/i2_mag)
    ia1_amplitud = np.mean(array[:, 50])
    ia2_amplitud = np.mean(array[:, 51])
    ia1_fase = np.mean(array[:, 53])
    ia2_fase = np.mean(array[:, 54])
    # energia
    kw_a = np.mean(array[:, 20])
    kw_b = np.mean(array[:, 21])
    kw_c = np.mean(array[:, 22])
    kw_avg = (kw_a + kw_b + kw_c) / 3
    kvar_a = np.mean(array[:, 23])
    kvar_b = np.mean(array[:, 24])
    kvar_c = np.mean(array[:, 25])
    kvar_avg = (kvar_a + kvar_b + kvar_c) / 3
    kva_a = np.mean(array[:, 26])
    kva_b = np.mean(array[:, 27])
    kva_c = np.mean(array[:, 28])
    kva_avg = (kva_a + kva_b + kva_c) / 3
    pf_a = np.mean(array[:, 17])
    pf_b = np.mean(array[:, 18])
    pf_c = np.mean(array[:, 19])
    pf_avg = (pf_a + pf_b + pf_c) / 3

    # mag_i1=fila[8],
    rps = (2*pi*(rpm/60))
    torque = kw_avg/rps
    # mag_i2=fila[9],
    # mag_i3=fila[10],

    data = {
        "voltage": {
            "ab": ab,
            "bc": bc,
            "ca": ca,
            "avg": avg,
            "value": value,
        },
        "unbalance": unbalance,
        "distorsion": {
            "thdv_a": thdv_a,
            "thdv_b": thdv_b,
            "thdv_c": thdv_c,
            "thdv_avg": thdv_avg,
            "thdi_a": thdi_a,
            "thdi_b": thdi_b,
            "thdi_c": thdv_c,
            "thdi_avg": thdi_avg
        },
        "full_distorsion": {
            "tdv_a": tdv_a,
            "tdv_b": tdv_b,
            "tdv_c": tdv_c,
            "tdv_avg": tdv_avg,
            "tdi_a": tdi_a,
            "tdi_b": tdi_b,
            "tdi_c": tdi_c,
            "tdi_avg": tdi_avg
        },
        "current_level": {
            "current_a": current_a,
            "current_b": current_b,
            "current_c": current_c,
            "current_avg": current_avg,
            "current_nominal": current_nominal,
        },
        "current_unbalance": current_unbalance,
        "efficiency": {
            "load_percen_avg": load_percen_avg,
            "lsskw_avg": lsskw_avg,
            "eff_avg": eff_avg,
        },
        "spectrum": {
            "sideband_amplitud_db": sideband_amplitud_db,
            "sideband_freq_hz": sideband_freq_hz,
        },
        "energia": {
            "kw_a": kw_a,
            "kw_b": kw_b,
            "kw_c": kw_c,
            "kw_avg": kw_avg,
            "kvar_a": kvar_a,
            "kvar_b": kvar_b,
            "kvar_c": kvar_c,
            "kvar_avg": kvar_avg,
            "kva_a": kva_a,
            "kva_b": kva_b,
            "kva_c": kva_c,
            "kva_avg": kva_avg,
            "pf_a": pf_a,
            "pf_b": pf_b,
            "pf_c": pf_c,
            "pf_avg": pf_avg,
            # "v_a": ab,
            # "v_b": bc,
            # "v_c": ca,
            # "v_avg": avg,
            # "i_a": current_a,
            # "i_b": current_b,
            # "i_c": current_c,
            # "i_avg": current_avg,
            # "thdv_a": thdv_a,
            # "thdv_b": thdv_b,
            # "thdv_c": thdv_c,
            # "thdv_avg": thdv_avg,
            # "thdi_a": thdi_a,
            # "thdi_b": thdi_b,
            # "thdi_c": thdv_c,
            # "thdi_avg": thdi_avg,
        },
        "torque": torque,
        "symetrical_components": {
            "vab_fase": vab_fase,
            "vbc_fase": vbc_fase,
            "vca_fase": vca_fase,
            "unbalance_voltage": unbalance_voltage,
            "va1_amplitud": va1_amplitud,
            "va2_amplitud": va2_amplitud,
            "va1_fase": va1_fase,
            "va2_fase": va2_fase,
            "ia_fase": ia_fase,
            "ib_fase": ib_fase,
            "ic_fase": ic_fase,
            "unbalance_current": unbalance_current,
            "ia1_amplitud": ia1_amplitud,
            "ia2_amplitud": ia2_amplitud,
            "ia1_fase": ia1_fase,
            "ia2_fase": ia2_fase
        }
    }
    print(data)
    return data


def create_average(promedio, test_electrical_result):
    try:
        print(test_electrical_result)
        obj_average = AverageMeasurement(test_electrical_result_fk=test_electrical_result,
                                         ab=promedio["voltage"]["ab"],
                                         bc=promedio["voltage"]["bc"],
                                         ca=promedio["voltage"]["ca"],
                                         avg=promedio["voltage"]["avg"],
                                         value=promedio["voltage"]["value"],
                                         unbalance=promedio["unbalance"],
                                         thdv_a=promedio["distorsion"]["thdv_a"],
                                         thdv_b=promedio["distorsion"]["thdv_b"],
                                         thdv_c=promedio["distorsion"]["thdv_c"],
                                         thdv_avg=promedio["distorsion"]["thdv_avg"],
                                         thdi_a=promedio["distorsion"]["thdi_a"],
                                         thdi_b=promedio["distorsion"]["thdi_b"],
                                         thdi_c=promedio["distorsion"]["thdi_c"],
                                         thdi_avg=promedio["distorsion"]["thdi_avg"],
                                         tdv_a=promedio["full_distorsion"]["tdv_a"],
                                         tdv_b=promedio["full_distorsion"]["tdv_b"],
                                         tdv_c=promedio["full_distorsion"]["tdv_c"],
                                         tdv_avg=promedio["full_distorsion"]["tdv_avg"],
                                         tdi_a=promedio["full_distorsion"]["tdi_a"],
                                         tdi_b=promedio["full_distorsion"]["tdi_b"],
                                         tdi_c=promedio["full_distorsion"]["tdi_c"],
                                         tdi_avg=promedio["full_distorsion"]["tdi_avg"],
                                         current_a=promedio["current_level"]["current_a"],
                                         current_b=promedio["current_level"]["current_b"],
                                         current_c=promedio["current_level"]["current_c"],
                                         current_avg=promedio["current_level"]["current_avg"],
                                         current_nominal=promedio["current_level"]["current_nominal"],
                                         current_unbalance=promedio["current_unbalance"],
                                         load_percen_avg=promedio["efficiency"]["load_percen_avg"],
                                         lsskw_avg=promedio["efficiency"]["lsskw_avg"],
                                         eff_avg=promedio["efficiency"]["eff_avg"],
                                         sideband_amplitud_db=promedio["spectrum"]["sideband_amplitud_db"],
                                         sideband_freq_hz=promedio["spectrum"]["sideband_freq_hz"],
                                         vab_fase=promedio["symetrical_components"]["vab_fase"],
                                         vbc_fase=promedio["symetrical_components"]["vbc_fase"],
                                         vca_fase=promedio["symetrical_components"]["vca_fase"],
                                         unbalance_voltage=promedio["symetrical_components"]["unbalance_voltage"],
                                         va1_amplitud=promedio["symetrical_components"]["va1_amplitud"],
                                         va2_amplitud=promedio["symetrical_components"]["va2_amplitud"],
                                         va1_fase=promedio["symetrical_components"]["va1_fase"],
                                         va2_fase=promedio["symetrical_components"]["va2_fase"],
                                         ia_fase=promedio["symetrical_components"]["ia_fase"],
                                         ib_fase=promedio["symetrical_components"]["ib_fase"],
                                         ic_fase=promedio["symetrical_components"]["ic_fase"],
                                         unbalance_current=promedio["symetrical_components"]["unbalance_current"],
                                         ia1_amplitud=promedio["symetrical_components"]["ia1_amplitud"],
                                         ia2_amplitud=promedio["symetrical_components"]["ia2_amplitud"],
                                         ia1_fase=promedio["symetrical_components"]["ia1_fase"],
                                         ia2_fase=promedio["symetrical_components"]["ia2_fase"],
                                         kw_a=promedio["energia"]["kw_a"],
                                         kw_b=promedio["energia"]["kw_b"],
                                         kw_c=promedio["energia"]["kw_c"],
                                         kw_avg=promedio["energia"]["kw_avg"],
                                         kvar_a=promedio["energia"]["kvar_a"],
                                         kvar_b=promedio["energia"]["kvar_b"],
                                         kvar_c=promedio["energia"]["kvar_c"],
                                         kvar_avg=promedio["energia"]["kvar_avg"],
                                         kva_a=promedio["energia"]["kva_a"],
                                         kva_b=promedio["energia"]["kva_b"],
                                         kva_c=promedio["energia"]["kva_c"],
                                         kva_avg=promedio["energia"]["kva_avg"],
                                         pf_a=promedio["energia"]["pf_a"],
                                         pf_b=promedio["energia"]["pf_b"],
                                         pf_c=promedio["energia"]["pf_c"],
                                         pf_avg=promedio["energia"]["pf_avg"],
                                         torque=promedio["torque"])
        print(f"objeto average : {obj_average}")
        print("aqui llego")
        obj_average.save()
    except TestER.DoesNotExist:
        return Response({'error': f'Test electrical result instance does not exist'},
                        status=status.HTTP_404_NOT_FOUND)


def validate_date_format(date_string):
    expected_format = "%Y-%m-%dT%H:%M:%S"
    try:
        date_obj = datetime.strptime(date_string, expected_format)
        return date_obj
    except ValueError:
        raise ValueError(
            f"Invalid date format. The expected format is {expected_format}.")
