from django.contrib import admin

# Register your models here.


from django.contrib import admin
from MainApp.models import Svs_z, Svs_k

admin.site.register(Svs_k)
admin.site.register(Svs_z)
