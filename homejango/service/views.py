import random
from functools import wraps

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import render, redirect

from .models import Clients, Vacations, Doctor, Procedure, Pets, Order
from .forms import PetForms, ClientsForms, OrderForms
from django.views.generic import DetailView, ListView  #DetailView - одна запиь, ListView - все записи
from datetime import datetime, timedelta
import telegram
from django.conf import settings


# Create your views here.
# def procedure(request):                 #вараинт вызвоа через функцию а  не через класс
#     procedure_ = Procedure.objects.all
#     return render(request, 'service/procedure.html', {'procedure_': procedure_})

def check_specific_user(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Проверяем, что пользователь - это Modetaror или Saatarko
        if not (request.user.username == "Modetaror" or request.user.username == "Saatarko"):
            return HttpResponseForbidden("Доступ запрещен")
        return view_func(request, *args, **kwargs)

    return _wrapped_view


class ProcedureDetailView(ListView):
    model = Procedure
    template_name = 'service/procedure.html'
    context_object_name = 'procedure'


# @login_required  # можно в скобках указать url для перехода и он будет иметь больший приоритет
@check_specific_user
def schedule(request):
    doctor_list = Doctor.objects.all()
    appointments = Order.objects.filter(
        date_order__gt=(datetime.today() - timedelta(days=7)).strftime("%Y-%m-%d")).select_related('procedure',
                                                                                                   'clients', 'doctor')

    if request.method == 'POST':
        date_temp = request.POST.get('date_order')
        selected_doctor_name = request.POST.get('doctor')

        if date_temp:
            appointments = appointments.filter(date_order__gt=date_temp)

        if selected_doctor_name:
            selected_doctor = Doctor.objects.filter(name=selected_doctor_name).first()
            if selected_doctor:
                appointments = appointments.filter(doctor__id=selected_doctor.id)

    context = {
        'appointments': appointments,
        'doctor_list': doctor_list,
    }

    return render(request, 'service/schedule.html', context)


def procedure_named(request, name):
    result = Procedure.objects.get(name_procedure=name)
    current_user = request.user
    client = Clients.objects.get(first_name=current_user.first_name, last_name=current_user.last_name)
    client_id = client.id
    pets_formset = Pets.objects.filter(clients=client_id)
    context = {
        'result': result,
        'pets_formset': pets_formset,
    }
    return render(request, 'service/procedure_name.html', context)


# class ProcedureNameDetailView(DetailView):
#     model = Procedure
#     template_name = 'service/procedure_name.html'
#     context_object_name = 'result'
#     slug_field = 'name_procedure'  # Указываем поле, которое будет использоваться как слаг
#     slug_url_kwarg = 'name'  # Указываем имя аргумента из URL
#
#     def get_queryset(self):
#         # Фильтрация по условию name_procedure=name
#         name = self.kwargs.get('name')
#         return Procedure.objects.filter(name_procedure=name)


def order(request, name, additional_param):
    error = ''
    step = False
    result = Procedure.objects.get(name_procedure=name)
    procedure_id = result.id
    min_day_value = datetime.today().strftime("%Y-%m-%d")
    max_day_value = (datetime.today() + timedelta(days=30)).strftime("%Y-%m-%d")

    if additional_param == 'base':
        day_value = datetime.today().strftime("%Y-%m-%d")

        if request.POST:
            if 'date_order' in request.POST and 'time_order' not in request.POST:
                date_order_str = request.POST['date_order']
                day_value = date_order_str
                all_time = date_time_check(date_order_str)

                form_order = OrderForms(initial={
                    'day_value': day_value,
                    'min_day_value': day_value,
                    'max_day_value': max_day_value
                })

                date = {
                    'error': error,
                    'day_value': day_value,
                    'min_day_value': min_day_value,
                    'max_day_value': max_day_value,
                    'form_order': form_order,
                    'procedure_id': procedure_id,
                    'result': result,
                    'all_time': all_time,
                    'step1': True
                }

                return render(request, 'service/order.html', date)

            elif 'date_order' in request.POST and 'time_order' in request.POST:

                date_temp = request.POST['date_order']
                time_temp = request.POST['time_order']
                current_user = request.user

                client = Clients.objects.get(first_name=current_user.first_name, last_name=current_user.last_name)
                client_id = client.id
                # pets_formset = PetsFormSet(request.POST or None, instance=client)
                # pets_formset = Pets.objects.filter(clients=client_id)
                #
                # doctor = Doctor.objects.filter(profession=result.name_procedure)
                # random_doctor = random.choice(doctor)
                # # Получаем id выбранного доктора
                # random_doctor_id = random_doctor.id
                # procedure = Procedure.objects.get(id=procedure_id)

                date = {
                    'date_temp': date_temp,
                    'time_temp': time_temp,
                    'procedure_id': procedure_id,
                    'client_id': client_id,

                }

                return redirect('order_confirm', procedure_id=procedure_id, client_id=client_id, date_temp=date_temp,
                                time_temp=time_temp)
        else:
            form_order = OrderForms(initial={
                'day_value': day_value,
                'min_day_value': min_day_value,
                'max_day_value': max_day_value
            })

            date = {
                'error': error,
                'day_value': day_value,
                'min_day_value': min_day_value,
                'max_day_value': max_day_value,
                'form_order': form_order,
                'procedure_id': procedure_id,
                'step': True,
            }

            return render(request, 'service/order.html', date)

    return render(request, 'service/order.html')


def date_time_check(day_value):
    date_str = day_value

    # Преобразуем строку в объект datetime.date
    date_to_check = datetime.strptime(date_str, '%Y-%m-%d').date()

    start_time = datetime.strptime('09:00', '%H:%M').time()
    end_time = datetime.strptime('23:00', '%H:%M').time()

    # Создайте список времён с интервалом в 30 минут используя генератор списка и цикл for
    time_slots = [(datetime.combine(date_to_check, start_time) + timedelta(minutes=30 * i)).time() for i in range(
        (datetime.combine(date_to_check, end_time) - datetime.combine(date_to_check, start_time)).seconds // 1800)]

    # Получите список времён, которые уже заняты в этот день
    occupied_slots = Order.objects.filter(date_order=date_to_check).values_list('time_order', flat=True)

    # Отфильтруйте занятые времена из списка доступных времён
    available_slots = [time for time in time_slots if time not in occupied_slots]

    return available_slots


def order_confirm(request, procedure_id, client_id, date_temp, time_temp):
    procedure = Procedure.objects.get(id=procedure_id)

    client = Clients.objects.get(id=client_id)
    pets_formset = Pets.objects.filter(clients=client_id)

    doctor = Doctor.objects.filter(profession=procedure.name_procedure)
    random_doctor = random.choice(doctor)
    # Получаем id выбранного доктора
    random_doctor_id = random_doctor.id

    if request.POST:
        procedure_instance = Procedure.objects.get(id=procedure_id)
        client_instance = Clients.objects.get(id=client_id)
        doctor_instance = Doctor.objects.get(id=random_doctor_id)

        pet_id = request.POST.get('submit_button')
        # Теперь мы можем использовать pet_id для получения экземпляра питомца или других операций
        pet_instance = Pets.objects.get(id=pet_id)

        order = Order(date_order=date_temp, time_order=time_temp,
                      procedure=procedure_instance, clients=pet_instance,
                      doctor=doctor_instance)
        order.save()
        messages.success(request, "Вы успешно записались на прием")
        return redirect('home')
    else:

        date = {
            'date_temp': date_temp,
            'time_temp': time_temp,
            'procedure_id': procedure_id,
            'client': client,
            'client_id': client_id,
            'pets_formset': pets_formset,
            'procedure': procedure,
            'random_doctor_id': random_doctor_id,
        }
    return render(request, 'service/order_confirm.html', date)


# def send_telegram_message(order):
#     bot = telegram.Bot(token=settings.TELEGRAM_BOT_TOKEN)
#     chat_id = settings.TELEGRAM_CHANNEL_ID
#     message = f"Новый заказ:\nДата: {order.date_order}\nВремя: {order.time_order}\nПроцедура: {order.procedure.name_procedure}\nКлиент: {order.clients.name}\nДоктор: {order.doctor.name}"
#     bot.send_message(chat_id=chat_id, text=message)
#
