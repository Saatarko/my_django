from django.urls import path
from . import views
from .views import ReviewsListView, ReviewCreateView

urlpatterns = [
   path('', views.index, name='home'),
   path('about', views.about, name='about'),
   path('contacts', views.contacts, name='contacts'),
   # path('reviews', views.reviews, name='reviews'),
   path('reviews/delete/<int:id>/', views.reviews_delete, name='reviews_delete'),
   path('reviews/', ReviewsListView.as_view(), name='reviews-list'),
   path('reviews/add/', ReviewCreateView.as_view(), name='review-add'),
   # path('reviews', views.reviews, name='reviews'),
   # path('reviews/delete/<int:id>/', views.reviews_delete, name='reviews_delete'),
   path('personal_doctor', views.personal_doctor, name='personal_doctor'),
   path('gruming', views.gruming, name='gruming'),
]



