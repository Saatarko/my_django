from .models import Procedure, Clients, Pets, Order
from django.forms import ModelForm, TextInput, NumberInput, DateInput, TimeInput

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms import inlineformset_factory



class ClientsForms(ModelForm):
    class Meta:
        model = Clients
        fields = ['first_name', 'last_name', 'phone']

        widgets = {
            'first_name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Укажите ваше Имя',
            }),
            'last_name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Укажите вашу Фамилию',
            }),
            'phone': NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Укажите ваш телефон',
            })

        }


class PetForms(ModelForm):
    class Meta:
        model = Pets
        fields = ['nickname', 'birthdate', 'breed', 'color']

        widgets = {
            'nickname': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Укажите кличку питомца',
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


class OrderForms(ModelForm):
    class Meta:
        model = Order
        fields = ['date_order', 'time_order']

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

    def __init__(self, *args, **kwargs):
        super(OrderForms, self).__init__(*args, **kwargs)
        self.fields['date_order'].widget.attrs.update({
            'value': kwargs.get('initial', {}).get('day_value', ''),
            'min': kwargs.get('initial', {}).get('min_day_value', ''),
            'max': kwargs.get('initial', {}).get('max_day_value', '')
        })
