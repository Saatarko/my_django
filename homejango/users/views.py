from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView

from service.forms import PetForms
from service.models import Clients, Pets
from .forms import LoginUserForm, RegisterUserForm

from .forms import ProfileUserForm, PetsFormSet


# Create your views here.


# def login_user(request):       # логин через функцию
#     if request.method == 'POST':
#         form = LoginUserForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data  # коллекция для аутентификации пользователя
#             user = authenticate(request, username=cd['username'], password=cd['password'])
#             if user and user.is_active:
#                 login(request, user)
#                 return HttpResponseRedirect(reverse('home'))
#     else:
#         form = LoginUserForm()
#     return render(request, 'users/login.html', {'form': form})

#
# def logout_user(request):    # логаут через функцию (аздан напрямую в urls.py)
#     logout(request)
#     return HttpResponseRedirect(reverse('users:login'))


class LoginUser(LoginView):  # логин через класс - проверка на валидность сразу встроена
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Авторизация'}

    # меняет страницу на которую переходится после успешной авторизаии
    # У нас убрано т.к прописан LOGIN_REDIRECT_URL  в settings - что аналогично
    # def get_success_url(self):
    #     return reverse_lazy('home')


# class RegisterUser(CreateView):
#     form_class = RegisterUserForm
#     template_name = 'users/register.html'
#     extra_context = {'title': 'Регистрация'}

def register(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            error = check_client_value_valid(request.POST['first_name'], request.POST['last_name'],
                                             request.POST['phone'])
            if error == '':
                user = form.save(commit=False)
                user.set_password(form.cleaned_data['password1'])
                user.save()

                Clients.objects.create(
                    user=user,
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    phone=form.cleaned_data['phone']
                )
                messages.success(request, "Регистрация успешно завершена")
                return redirect('home')
            else:
                messages.error(request, f'{error}')
                return render(request, 'users/register.html', {'form': form})
    else:
        form = RegisterUserForm()
    return render(request, 'users/register.html', {'form': form})


# class ProfileUser(LoginRequiredMixin, UpdateView):
#     model = get_user_model()
#     form_class = ProfileUserForm
#     template_name = 'users/profile.html'
#     extra_context = {'title': 'Профайл'}
#
#     def get_success_url(self):
#         return reverse_lazy('users:profile')
#
#     def get_object(self, queryset=None):
#         return self.request.user
#

def profile_update(request):
    user = request.user
    client, created = Clients.objects.get_or_create(user=user)
    client_id = client.id
    form = ProfileUserForm(request.POST or None, instance=user)
    pets = Pets.objects.filter(clients=client_id)

    if request.method == 'POST':
        if form.is_valid():
            # Обновление данных клиента
            error = check_client_value_valid(request.POST['first_name'], request.POST['last_name'],request.POST['phone'])
            if error == '':
                client.first_name = form.cleaned_data['first_name']
                client.last_name = form.cleaned_data['last_name']
                client.phone = form.cleaned_data['phone']
                client.save()

                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                user.phone = form.cleaned_data['phone']
                user.save()
                messages.success(request, "Ваши данные успешно обновлены")
            else:
                messages.error(request, f'{error}')
                return render(request, 'users/profile.html', {
                    'form': form,
                    'pets': pets,
                    'title': 'Профайл'
                })

    return render(request, 'users/profile.html', {
        'form': form,
        'pets': pets,
        'title': 'Профайл'
    })


def register_done(request):
    return render(request, 'users/register_done.html')


def profile_delete(request, temp_id):
    pets = Pets.objects.filter(id=temp_id)
    pets.delete()
    messages.success(request, "Питомец успешно удален из профиля")
    return redirect('users:profile')


def profile_add_pet(request):
    if request.method == 'POST':
        pets = PetForms(request.POST)
        if pets.is_valid():
            error = check_pets_value_valid(request.POST['nickname'], request.POST['breed'], request.POST['color'])
            if error == '':
                user = request.user
                client, created = Clients.objects.get_or_create(user=user)
                pet = pets.save(commit=False)
                pet.clients = client  # Присваиваем объект client к полю clients
                pet.save()
                messages.success(request, "Питомец успешно добавлен в профиль")
                return redirect('users:profile')
            else:
                messages.error(request, f"{error}")
                return render(request, 'users/add_pet.html', {
                    'pets': pets,
                })
    else:
        pets = PetForms()

    return render(request, 'users/add_pet.html', {
        'pets': pets,
    })


def profile_edit_pet(request, temp_id):
    if request.method == 'POST':
        pets = PetForms(request.POST)
        if pets.is_valid():
            error = check_pets_value_valid(request.POST['nickname'], request.POST['breed'], request.POST['color'])
            if error == '':
                user = request.user
                client, created = Clients.objects.get_or_create(user=user)
                pet = pets.save(commit=False)
                pet.clients = client
                pet.save()
                messages.success(request, "Данные питомца успешно обновлены.")
                return redirect('users:profile')
            else:
                temp_pet = get_object_or_404(Pets, id=temp_id)
                value = temp_pet.birthdate.isoformat()
                pets = PetForms(instance=temp_pet)

                messages.error(request, f"{error}")
                return render(request, 'users/edit_pet.html', {
                    'pets': pets,
                    'value': value,
                })
    else:
        temp_pet = get_object_or_404(Pets, id=temp_id)
        value = temp_pet.birthdate.isoformat()

        pets = PetForms(instance=temp_pet)

    return render(request, 'users/edit_pet.html', {
        'pets': pets,
        'value': value,
    })


def check_pets_value_valid(nickname, breed, color):
    letters = 'abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя-'
    error = ''
    temp_name = nickname.lower()
    temp_name_split = temp_name.split()

    temp_breed = breed.lower()
    temp_breed_split = temp_breed.split()

    temp_color = color.lower()
    temp_color_split = temp_color.split()

    if len(temp_name_split) > 4:
        error = 'Слишком много слов для клички'
        return error
    if len(temp_breed_split) > 1:
        error = 'Слишком много слов для породы '
        return error
    if len(temp_color_split) > 1:
        error = 'Слишком много слов для цвета'
        return error

    for i in temp_name:
        if len(i.strip(letters)) != 0:
            error = 'В кличке допустимы только буквы!'
            return error
    for j in temp_breed:
        if len(j.strip(letters)) != 0:
            error = 'В названии породы допустимы только буквы!'
            return error
    for k in temp_color:
        if len(k.strip(letters)) != 0:
            error = 'В названии цвета допустимы только буквы!'
            return error
    return error


def check_client_value_valid(first_name, last_name, phone):
    letters = 'abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя-'
    numbers = '1234567890+'
    error = ''

    temp_first_name = first_name.lower()
    temp_first_name_split = temp_first_name.split()

    temp_last_name = last_name.lower()
    temp_last_name_split = temp_last_name.split()

    if len(temp_first_name_split) > 1 or len(temp_last_name_split) > 1:
        error = 'Слишком много слов для имени/фамилии'
        return error

    for i in temp_first_name:
        if len(i.strip(letters)) != 0:
            error = 'В имени допустимы только буквы!'
            return error
    for j in temp_last_name:
        if len(j.strip(letters)) != 0:
            error = 'В фамилии допустимы только буквы!'
            return error
    for s in phone:
        if len(s.strip(numbers)) != 0:
            error = 'У вас в номере телефона некорректные символы!'
            return error
    return error
