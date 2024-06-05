from django.urls import path
from . import views

urlpatterns = [
   path('procedure', views.procedure, name='procedure'),
   path('procedure/<str:name>/', views.procedure_named, name='procedure_named'),
   path('procedure/<str:name>/order', views.order, name='order'),
   path('procedure/<str:name>/order/thanks', views.thanks, name='thanks')
]