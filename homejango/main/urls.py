from django.urls import path
from . import views

urlpatterns = [
   path('', views.index, name='home'),
   path('about', views.about, name='about'),
   path('contacts', views.contacts, name='contacts'),
   path('reviews', views.reviews, name='reviews'),
   path('reviews/delete/<int:id>/', views.reviews_delete, name='reviews_delete'),
   path('personal_doctor', views.personal_doctor, name='personal_doctor'),
   path('gruming', views.gruming, name='gruming'),
]



