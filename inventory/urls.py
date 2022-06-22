from django.urls import path
from .views import (inventory_list, device_type_list,
                    add_new_device, edit_device, delete_device)


app_name = "inventory"

urlpatterns = [
    path('inventory_list/', inventory_list, name='inventory_list'),
    path('device_type_list/', device_type_list, name='device_type_list'),
    path('add_new_device/', add_new_device, name='add_new_device'),
    path('<int:id>/<str:device_type>/edit_device/',
         edit_device, name='edit_device'),
    path('<int:id>/<str:device_type>/delete_device/',
         delete_device, name='delete_device'),
]
