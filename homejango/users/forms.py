from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms import inlineformset_factory

from service.models import Clients, Pets


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин',
                               widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        # так делать правильнее чем через поля формы т.к страхует при изменения модели юзера
        model = get_user_model()
        fields = ['username', 'password']


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин',
                               widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль',
                                widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор Пароля',
                                widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    # firstname = forms.CharField(label='Имя',
    #                            widget=forms.TextInput(attrs={'class': 'form-input'}))
    # lastname = forms.CharField(label='Фамилия',
    #                            widget=forms.TextInput(attrs={'class': 'form-input'}))

    email = forms.EmailField(label='email',
                             widget=forms.TextInput(attrs={'class': 'form-input'}))

    class Meta:
        # так делать правильнее чем через поля формы т.к страхует при изменения модели юзера
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'phone']
        labels = {
            'email': 'E-mail',
            'firstname': 'Имя',
            'lastname': 'Фамилия',
            'phone': 'Телефон'

        }

    def сlean_password(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают')
        return cd['password']

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError('Такой email уже существует!!')
        return email


class ProfileUserForm(forms.ModelForm):
    username = forms.CharField(disabled=True, label='Логин',
                               widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(disabled=True, label='email',
                             widget=forms.TextInput(attrs={'class': 'form-input'}))

    class Meta:
        # так делать правильнее чем через поля формы т.к страхует при изменения модели юзера
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'phone']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'phone': 'Телефон'

        }


PetsFormSet = inlineformset_factory(
    Clients, Pets, fields=('nickname', 'birthdate', 'breed', 'color'), extra=1, can_delete=True
)
