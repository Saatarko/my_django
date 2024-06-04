from django.shortcuts import render
from .models import Clients, Vacations, Doctor, Procedure, Pets, Order

# Create your views here.
def procedure(request):
    procedure_ = Procedure.objects.all
    return render(request, 'service/procedure.html', {'procedure_':procedure_})


