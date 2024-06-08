from django.conf import settings
from django.db import models


# Create your models here.
class Clients(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField('Имя', max_length=30)
    last_name = models.CharField('Фамилия', max_length=30)
    phone = models.CharField('Телефон', max_length=15)

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.phone}"

    class Meta:  # даем название таблицы в админке
        verbose_name = 'Клиенты/Clients'
        verbose_name_plural = 'Клиенты/Clients'


class Pets(models.Model):
    nickname = models.CharField('Кличка', max_length=30)
    birthdate = models.DateField('Дата рождения')
    breed = models.CharField('Порода', max_length=20)
    color = models.CharField('Окрас', max_length=20)

    clients = models.ForeignKey(Clients, on_delete=models.CASCADE)

    def __str__(self):
        return self.nickname

    class Meta:
        verbose_name = 'Питомцы/Pets'
        verbose_name_plural = 'Питомцы/Pets'


class Procedure(models.Model):
    name_procedure = models.CharField('Название процедуры', max_length=30)
    eng_name_procedure = models.CharField('Название процедуры на англ', max_length=30)
    description = models.TextField('Описание')
    price = models.IntegerField('Цена')

    def __str__(self):
        return self.name_procedure

    class Meta:
        verbose_name = 'Процедуры/Procedure'
        verbose_name_plural = 'Процедуры/Procedure'


class Doctor(models.Model):
    name = models.CharField('ФИО врача', max_length=30)
    profession = models.CharField('Профессия', max_length=30)
    salary = models.IntegerField('ЗП')



    def __str__(self):
        return self.name

    class Meta:  # даем название таблицы в админке
        verbose_name = 'Врачи/Doctor'
        verbose_name_plural = 'Врачи/Doctor'


class Order(models.Model):
    date_order = models.DateField('Дата бронирования')
    time_order = models.TimeField('Время бронирования')

    procedure = models.ForeignKey(Procedure, on_delete=models.CASCADE)
    clients = models.ForeignKey(Pets, on_delete=models.CASCADE)
    doctor = models.OneToOneField(Doctor, on_delete=models.CASCADE)

    def __str__(self):
        return self.date_order

    class Meta:  # даем название таблицы в админке
        verbose_name = 'Заказ/Order'
        verbose_name_plural = 'Заказ/Order'


class Vacations(models.Model):
    date_vacations = models.DateField('Дата отпуска')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)

    def __str__(self):
        return self.date_vacations

    class Meta:  # даем название таблицы в админке
        verbose_name = 'Отпуска/Vacations'
        verbose_name_plural = 'Отпуска/Vacations'
