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
   path('profile/delete/<int:pk>/', views.PetsDelete.as_view(), name='profile_delete'),
   # path('profile/add_pet/', views.profile_add_pet, name='profile_add_pet'),

# большая разница между <int:temp_id>  и <int:pk>. В первом случае просто указываем что это число
   # подходит для функций. Если используем класс надо четко указать id(<int:pk>) или slug
   path('profile/add_pet/', views.AddPets.as_view(), name='profile_add_pet'),
   path('profile/edit_pet/<int:pk>/', views.UpdatePets.as_view(), name='profile_edit_pet'),
]