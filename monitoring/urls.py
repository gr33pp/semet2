from django.urls import path
from . import views


app_name = 'monitoring'

urlpatterns = [
    path('add_appliance/', views.add_appliance, name='add_appliance'),
    path('appliances/', views.appliance_list, name='appliance_list'),
    path('dash/', views.energy_dashboard, name='energy_dashboard'),
]
