from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views


app_name = 'users'
urlpatterns = [
   # для вывода нужной страницы после входа/выхода нужно прописать или
   # функции get-succes_url или в settings  LOGOUT/LOGIN_REDIRECT_URL
   path('login', views.LoginUser.as_view(), name='login'),     # для
   path('logout', LogoutView.as_view(), name='logout'),

]