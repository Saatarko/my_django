from .models import Procedure, Clients, Pets, Order
from django.forms import ModelForm, TextInput, NumberInput, DateInput, TimeInput


class ClientsForms(ModelForm):
    class Meta:
        model = Clients
        fields = ['name','phone']

        widgets = {
            'name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Укажите ваше ФИО',
            }),
            'phone': NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Укажите ваш телефон',
            })

        }


class PetForms(ModelForm):
    class Meta:
        model = Pets
        fields = ['nickname','birthdate','breed','color']

        widgets = {
            'nickname': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'кажите кличку питомца',
            }),
            'birthdate': DateInput(attrs={
                'class': 'form-control',
                'placeholder': 'Укажите дату рождения питомца',
            }),
            'breed': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Укажите породу питомца',
            }),
            'color': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Укажите окрас питомца',
            })

        }

class Order(ModelForm):
    class Meta:
        model = Order
        fields = ['date_order','time_order']

        widgets = {
            'date_order': DateInput(attrs={
                'class': 'form-control',
                'placeholder': 'Укажите дату заявки',
                'type': 'date',
            }),
            'time_order': TimeInput(attrs={
                'class': 'form-control',
                'placeholder': 'Укажите время заявки',
                'type': 'time',
            })

        }