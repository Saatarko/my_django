from django.urls import path
from . import views

urlpatterns = [
   path('', views.index, name='home'),
   path('about', views.about, name='about'),
   path('contacts', views.contacts, name='contacts'),
   path('reviews', views.reviews, name='reviews'),
   path('reviews_delete', views.reviews_delete, name='reviews_delete')
]



