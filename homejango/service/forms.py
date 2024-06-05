from .models import Procedure, Clients, Pets
from django.forms import ModelForm, TextInput, NumberInput, DateInput


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