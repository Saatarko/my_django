from django.shortcuts import render, redirect
from .models import Clients, Vacations, Doctor, Procedure, Pets, Order
from .forms import PetForms, ClientsForms
from django.views.generic import DetailView, ListView  #DetailView - одна запиь, ListView - все записи
from datetime import datetime, timedelta




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


def order(request, name):
    error = ''
    if request.method == 'POST':
        form_client = ClientsForms(request.POST)
        form_pets = PetForms(request.POST)

        if form_client.is_valid() and form_pets.is_valid():  #проверка данных на валидность формы. но не занчения
            form_client.save()
            form_pets.save()

            return redirect('home')
        else:
            error = 'Форма заполнена неверно'

    all_time = ['08:00', '08:30', '09:00', '09:30', '10:00', '10:30', '11:00', '11:30', '12:00', '12:30', '13:00',
                '13:30', '14:00', '14:30', '15:00', '15:30', '16:00', '16:30', '17:00', '17:30', '18:00', '18:30',
                '19:00', '19:30', '20:00', '20:30', '21:00', '21:30', '22:00', '22:30']

    day_value = datetime.today()
    min_day_value = day_value.strftime("%Y-%m-%d")
    max_day_value = min_day_value + timedelta(days=30)

    result = Procedure.objects.get(name_procedure=name)
    form_client = ClientsForms()
    form_pets = PetForms()
    date = {
        'form_client': form_client,
        'form_pets': form_pets,
        'result': result,
        'error': error,
        'min_day_value': min_day_value,
        'all_time': all_time,
        'max_day_value': max_day_value
    }
    return render(request, 'service/order.html', date)


def thanks(request, name):
    if request.POST:
        return render(request, 'service/thanks.html', {'date': date})


def zapis(request):

    # man_day_value =

    date = {
        'min_day_value': min_day_value,

    }

    return render(request, 'service/thanks.html', {'date': date})