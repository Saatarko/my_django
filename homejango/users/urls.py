from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views


app_name = 'users'
urlpatterns = [
   # для вывода нужной страницы после входа/выхода нужно прописать или
   # функции get-succes_url или в settings  LOGOUT/LOGIN_REDIRECT_URL
   path('login/', views.LoginUser.as_view(), name='login'),     # для
   path('logout/', LogoutView.as_view(), name='logout'),
   path('register/', views.register, name='register'),
   path('profile/', views.profile_update, name='profile'),
   path('profile/delete/<int:temp_id>/', views.profile_delete, name='profile_delete'),
   path('profile/add_pet/', views.profile_add_pet, name='profile_add_pet'),
   path('profile/edit_pet/<int:temp_id>/', views.profile_edit_pet, name='profile_edit_pet'),
   path('register/done/', views.register_done, name='register_done'),
]