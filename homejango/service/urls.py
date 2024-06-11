from django.urls import path
from . import views

urlpatterns = [

   path('procedure', views.ProcedureDetailView.as_view(), name='procedure'),
   path('procedure/<str:name>/', views.procedure_named, name='procedure_named'),
   path('procedure/<str:name>/<str:additional_param>/order', views.order, name='order'),
   path('schedule', views.schedule, name='schedule'),
   path('service/procedure/order_confirm/<int:procedure_id>/<int:client_id>/<str:date_temp>/<str:time_temp>/', views.order_confirm, name='order_confirm'),

]