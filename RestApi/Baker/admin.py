from django.contrib import admin
from .models import Motor, Test, Medicion

# Register your models here.
admin.site.register(Motor)
admin.site.register(Test)
admin.site.register(Medicion)