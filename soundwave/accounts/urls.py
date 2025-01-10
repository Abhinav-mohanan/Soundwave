from django.urls import path
from . import views

urlpatterns=[
    path('user_accounts/',views.user_account_view,name='user_account'),
    path('edit_details/',views.edit_details,name='edit_details'),
    path('add_address/',views.add_address,name='add_address'),
    path('view_address/',views.view_address,name='view_address'),
    path('edit_address/<int:address_id>/',views.edit_address,name='edit_address'),
    path('order_details/',views.user_orders,name='order_details'),
    path('change_password/',views.change_password,name='change_password'),
    path('list_orders/',views.order_list,name='list_order'),
    path('delete_address/<int:address_id>/',views.deactivate_address,name='delete_address'),
    path('manage_orders/<int:order_id>/',views.manage_order,name='manage_order')
]