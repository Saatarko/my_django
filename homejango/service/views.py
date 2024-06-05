from django.shortcuts import render
from .models import Clients, Vacations, Doctor, Procedure, Pets, Order


# Create your views here.
def procedure(request):
    procedure_ = Procedure.objects.all
    return render(request, 'service/procedure.html', {'procedure_': procedure_})


def procedure_named(request, name):
    result = Procedure.objects.filter(f'{name}')
    return render(request, 'service/procedure_name.html', {'result': result})
