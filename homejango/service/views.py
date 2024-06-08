from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect

from users.forms import ProfileUserForm
from .models import Clients, Vacations, Doctor, Procedure, Pets, Order
from .forms import PetForms, ClientsForms, OrderForms
from django.views.generic import DetailView, ListView  #DetailView - одна запиь, ListView - все записи
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# Create your views here.
# def procedure(request):                 #вараинт вызвоа через функцию а  не через класс
#     procedure_ = Procedure.objects.all
#     return render(request, 'service/procedure.html', {'procedure_': procedure_})


class ProcedureDetailView(ListView):
    model = Procedure
    template_name = 'service/procedure.html'
    context_object_name = 'procedure'


@login_required  # можно в скобках указать url для перехода и он будет иметь больший приоритет
def schedule(request):
    return render(request, 'service/schedule.html')


# def procedure_named(request, name):
#     result = Procedure.objects.get(name_procedure=name)
#     return render(request, 'service/procedure_name.html', {'result': result})

class ProcedureNameDetailView(DetailView):
    model = Procedure
    template_name = 'service/procedure_name.html'
    context_object_name = 'result'
    slug_field = 'name_procedure'  # Указываем поле, которое будет использоваться как слаг
    slug_url_kwarg = 'name'  # Указываем имя аргумента из URL

    def get_queryset(self):
        # Фильтрация по условию name_procedure=name
        name = self.kwargs.get('name')
        return Procedure.objects.filter(name_procedure=name)


def order(request, name, additional_param):
    error = ''
    step = False
    result = Procedure.objects.get(name_procedure=name)
    procedure_id = result.id
    min_day_value = datetime.today().strftime("%Y-%m-%d")
    max_day_value = (datetime.today() + timedelta(days=30)).strftime("%Y-%m-%d")

    form_order = OrderForms()

    if additional_param == 'base':
        day_value = datetime.today().strftime("%Y-%m-%d")

        if request.POST:
            if 'date' in request.POST and 'time' not in request.POST:
                date_order_str = request.POST['date']
                day_value = date_order_str
                all_time = date_time_check(date_order_str)

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

            elif 'date' in request.POST and 'time' in request.POST:

                date_temp = request.POST['date']
                time_temp = request.POST['time']
                current_user = request.user

                client = Clients.objects.get(first_name=current_user.first_name, last_name=current_user.last_name)
                client_id = client.id
                client, created = Clients.objects.get_or_create(user=current_user)
                form = ProfileUserForm(request.POST or None, instance=user)
                pets_formset = PetsFormSet(request.POST or None, instance=client)

                date = {
                    'date_temp': date_temp,
                    'time_temp': time_temp,
                    'procedure_id': procedure_id,
                    'client_id': client_id,
                     }

                return render(request, 'service/order_confirm.html', date)
        else:

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
