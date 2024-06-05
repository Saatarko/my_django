from django.urls import path
from . import views

urlpatterns = [
   path('procedure', views.procedure, name='procedure'),
   path('procedure/<str:name>/', views.procedure_named, name='procedure_named')
]