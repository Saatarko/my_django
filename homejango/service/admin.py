from django.contrib import admin

from .models import Clients, Vacations, Doctor, Procedure, Pets, Order


# admin.site.register(Clients)   #регистрируем таблицы для вывода в админке
admin.site.register(Vacations)
admin.site.register(Doctor)
admin.site.register(Procedure)
# admin.site.register(Pets)
# admin.site.register(Order)
#

#
@admin.register(Clients)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'phone')
    list_display_links = ('id', 'first_name', 'last_name')      # поля по которым можно переходить в админке


@admin.register(Pets)
class PetsAdmin(admin.ModelAdmin):
    list_display = ('id', 'nickname', 'birthdate', 'breed', 'color', 'clients')
    list_display_links = ('id', 'nickname')
    list_editable = ('birthdate', 'breed', 'color',)      # редактируемые поля
    # редактируемое поле не может быть кликабельным т.е в list_display_links и list_editable не должны пересекаться


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_order', 'time_order', 'procedure', 'clients', 'doctor')
    list_display_links = ('id', 'date_order', 'time_order', 'procedure', 'clients', 'doctor')
    ordering = ['date_order', 'time_order']   # сортировка записей только для админки
    # list_per_page = 5  # Указывает какое кол-во данных будет на одной странице
#
#
# # admin.site.register(Clients, ClientAdmin)  #регистрируем таблицы для вывода в админке но лучше через декоратор
# # admin.site.register(Clients)
# admin.site.register(Vacations)
# admin.site.register(Doctor)
# admin.site.register(Procedure)
# # admin.site.register(Pets)
# # admin.site.register(Order)
# # admin.site.register(Pets, PetsAdmin)
# # admin.site.register(Order,OrderAdmin)
