from django.urls import path
from . import views

urlpatterns = [

   path('procedure', views.ProcedureDetailView.as_view(), name='procedure'),
   path('procedure/<str:name>/', views.ProcedureNameDetailView.as_view(), name='procedure_named'),
   path('procedure/<str:name>/<str:additional_param>/order', views.order, name='order'),
   path('schedule', views.schedule, name='schedule'),
   path('procedure/<str:name>/<str:additional_param>/order/order_confirm', views.schedule, name='order_confirm')

]