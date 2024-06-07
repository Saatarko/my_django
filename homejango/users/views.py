from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy

from .forms import LoginUserForm
# Create your views here.


class LoginUser(LoginView):      # логин через класс - проверка на валидность сразу встроена
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Авторизация'}

    # меняет страницу на которую переходится после успешной авторизаии
    # У нас убрано т.к прописан LOGIN_REDIRECT_URL  в settings - что аналогично
    # def get_success_url(self):
    #     return reverse_lazy('home')



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
