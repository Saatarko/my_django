from django.shortcuts import render, redirect
from .models import Clients, Vacations, Doctor, Procedure, Pets, Order
from .forms import PetForms, ClientsForms


# Create your views here.
def procedure(request):
    procedure_ = Procedure.objects.all
    return render(request, 'service/procedure.html', {'procedure_': procedure_})


def procedure_named(request, name):
    result = Procedure.objects.get(name_procedure=name)
    return render(request, 'service/procedure_name.html', {'result': result})


def order(request, name):
    error = ''
    if request.method == 'POST':
        form_client = ClientsForms(request.POST)
        form_pets = PetForms(request.POST)

        if form_client.is_valid() and form_pets.is_valid():   #проверка данных на валидность формы. но не занчения
            form_client.save()
            form_pets.save()

            return redirect('home')
        else:
            error = 'Форма заполнена неверно'

    result = Procedure.objects.get(name_procedure=name)
    form_client = ClientsForms()
    form_pets = PetForms()
    date = {
        'form_client': form_client,
        'form_pets': form_pets,
        'result': result,
        'error': error
    }
    return render(request, 'service/order.html', date)


def thanks(request, name):

    if request.POST:

        return render(request, 'service/thanks.html', {'date': date})