from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible

from .models import Procedure, Clients, Pets, Order
from django.forms import ModelForm, TextInput, NumberInput, DateInput, TimeInput, formset_factory

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms import inlineformset_factory


@deconstructible
class DataValidatorPet_Client:
    ALLOWED_CHARS = 'abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя-'
    code = 'letters'

    def __init__(self, message=None):
        self.message = message if message else 'Должны присутствовать только буквы или дефис'

    def __call__(self, value, *args, **kwargs):
        if not (set(value) <= set(self.ALLOWED_CHARS)):
            raise ValidationError(self.message, code=self.code)


@deconstructible
class DataValidatorClientPhone:
    ALLOWED_CHARS = '+123456789'
    code = 'numbers'

    def __init__(self, message=None):
        self.message = message if message else 'Должны присутствовать цифры или +'

    def __call__(self, value, *args, **kwargs):
        if not (set(value) <= set(self.ALLOWED_CHARS)):
            raise ValidationError(self.message, code=self.code)


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
        def clean_first_name(self):
            first_name = self.cleaned_data['first_name']
            if not DataValidatorPet_Client(first_name):
                raise forms.ValidationError
            return first_name

        def clean_last_name(self):
            last_name = self.cleaned_data['last_name']
            if not DataValidatorPet_Client(last_name):
                raise forms.ValidationError
            return last_name

        def clean_first_namephone(self):
            phone = self.cleaned_data['phone']
            if not DataValidatorClientPhone(phone):
                raise forms.ValidationError
            return phone

PetForm = forms.ModelForm


class PetForms(ModelForm):
    class Meta:
        model = Pets
        fields = ['nickname', 'birthdate', 'breed', 'color', 'id']

        widgets = {
            'nickname': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Укажите кличку питомца',
            }),
            'birthdate': forms.DateInput(attrs={'type': 'date'}),
            'breed': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Укажите породу питомца',
            }),
            'color': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Укажите окрас питомца',
            }),
            'client': forms.HiddenInput(),
        }

        def clean_nickname(self):
            nickname = self.cleaned_data['nickname']
            if not DataValidatorPet_Client(nickname):
                raise forms.ValidationError
            return nickname

        def clean_breed(self):
            breed = self.cleaned_data['breed']
            if not DataValidatorPet_Client(breed):
                raise forms.ValidationError
            return breed

        def clean_color(self):
            color = self.cleaned_data['color']
            if not DataValidatorPet_Client(color):
                raise forms.ValidationError
            return color

        def __init__(self, *args, **kwargs):
            super(PetForm, self).__init__(*args, **kwargs)
            instance = kwargs.get('instance')
            if instance:
                self.fields['birthdate'].initial = instance.birthdate.strftime('%Y-%m-%d')


PetsFormSet = formset_factory(PetForm, extra=1, can_delete=True)


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
