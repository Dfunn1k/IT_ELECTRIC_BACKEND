# Generated by Django 4.2 on 2023-04-13 17:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Motor',
            fields=[
                ('motor_key', models.AutoField(primary_key=True, serialize=False)),
                ('model', models.CharField(max_length=100)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('test_key', models.AutoField(primary_key=True, serialize=False)),
                ('motor_nro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Baker.motor')),
            ],
        ),
        migrations.CreateModel(
            name='Medicion',
            fields=[
                ('medicion_key', models.AutoField(primary_key=True, serialize=False)),
                ('time', models.DateTimeField()),
                ('mag_v1', models.FloatField()),
                ('mag_v2', models.FloatField()),
                ('mag_v3', models.FloatField()),
                ('ang_v1', models.FloatField()),
                ('ang_v2', models.FloatField()),
                ('ang_v3', models.FloatField()),
                ('v2_freq', models.FloatField()),
                ('v3_freq', models.FloatField()),
                ('mag_i1', models.FloatField()),
                ('mag_i2', models.FloatField()),
                ('mag_i3', models.FloatField()),
                ('ang_i1', models.FloatField()),
                ('ang_i2', models.FloatField()),
                ('ang_i3', models.FloatField()),
                ('i1_freq', models.FloatField()),
                ('i2_freq', models.FloatField()),
                ('i3_freq', models.FloatField()),
                ('test_key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Baker.test')),
            ],
        ),
    ]
