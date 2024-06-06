from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Clients, Vacations, Doctor, Procedure, Pets, Order
from .forms import PetForms, ClientsForms
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

    min_day_value = datetime.today().strftime("%Y-%m-%d")
    max_day_value = (datetime.today() + timedelta(days=30)).strftime("%Y-%m-%d")
    result = Procedure.objects.get(name_procedure=name)
    form_client = ClientsForms()
    form_pets = PetForms()


    if additional_param == 'Base':

        day_value = datetime.today()



        date = {
            'form_client': form_client,
            'form_pets': form_pets,
            'result': result,
            'error': error,
            'day_value': day_value,
            'min_day_value': min_day_value,
            'max_day_value': max_day_value,
            'step': 1,
        }
        return render(request, 'service/order.html', date)

    elif additional_param == 'secondbase':

        day_value = request.GET.get('date')
        all_time = date_time_check(day_value)

        date = {
            'form_client': form_client,
            'form_pets': form_pets,
            'result': result,
            'error': error,
            'day_value': day_value,
            'min_day_value': min_day_value,
            'max_day_value': max_day_value,
            'all_time': all_time,
            'step': 2,
        }

        return render(request, 'service/order.html', date)


    elif additional_param == 'thirdbase':

        day_value = request.GET.get('date')
        time = request.GET.get('time')

        date = {
            'form_client': form_client,
            'form_pets': form_pets,
            'result': result,
            'error': error,
            'day_value': day_value,
            'min_day_value': min_day_value,
            'max_day_value': max_day_value,
            'time': time,
            'step': 3,
        }

        return render(request, 'service/order.html', date)
    # else:

        # if request.method == 'POST':
        #     form_client = ClientsForms(request.POST)
        #     form_pets = PetForms(request.POST)
        #     order = Order(date_order= ,time_order= )
        #
        #     if form_client.is_valid() and form_pets.is_valid():  #проверка данных на валидность формы. но не занчения
        #         form_client.save()
        #         form_pets.save()
        #
        #
        #         return redirect('home')
        #
        #     else:
        #         error = 'Форма заполнена неверно'
        #         day_value = request.GET.get('date')
        #         all_time = date_time_check(day_value)
        #         date = {
        #             'form_client': form_client,
        #             'form_pets': form_pets,
        #             'result': result,
        #             'error': error,
        #             'day_value': day_value,
        #             'min_day_value': min_day_value,
        #             'max_day_value': max_day_value,
        #             'all_time': all_time,
        #             'step': 2,
        #         }
        #         return render(request, 'service/order.html', date)




def date_time_check(day_value):
    date_str = day_value
    print(f'Получена дата из запроса: {date_str}')

    # Преобразуем строку в объект datetime.date
    date_to_check = datetime.strptime(date_str, '%Y-%m-%d').date()
    print(f'Дата преобразована в объект datetime.date: {date_to_check}')

    start_time = datetime.strptime('09:00', '%H:%M').time()
    end_time = datetime.strptime('23:00', '%H:%M').time()

    # Создайте список времён с интервалом в 30 минут используя генератор списка и цикл for
    time_slots = [(datetime.combine(date_to_check, start_time) + timedelta(minutes=30 * i)).time() for i in range(
        (datetime.combine(date_to_check, end_time) - datetime.combine(date_to_check, start_time)).seconds // 1800)]
    print(f'time_slots: {time_slots}')
    # Получите список времён, которые уже заняты в этот день
    occupied_slots = Order.objects.filter(date_order=date_to_check).values_list('time_order', flat=True)
    print(f'occupied_slots: {occupied_slots}')

    # Отфильтруйте занятые времена из списка доступных времён
    available_slots = [time for time in time_slots if time not in occupied_slots]

    logging.info(f'Доступные временные слоты: {available_slots}')

    return available_slots