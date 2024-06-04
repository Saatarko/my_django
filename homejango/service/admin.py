from django.contrib import admin

from .models import Clients, Vacations, Doctor, Procedure, Pets, Order
# Register your models here.

admin.site.register(Clients)   #регистрируем таблицы для вывода в админке
admin.site.register(Vacations)
admin.site.register(Doctor)
admin.site.register(Procedure)
admin.site.register(Pets)
admin.site.register(Order)