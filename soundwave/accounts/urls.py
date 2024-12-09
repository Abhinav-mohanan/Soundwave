from django.urls import path
from . import views

urlpatterns=[
    path('user_accounts/',views.user_account_view,name='user_account'),
    path('edit_details/',views.edit_details,name='edit_details'),
    path('add_address/',views.add_address,name='add_address'),
    path('view_address/',views.view_address,name='view_address'),
    path('edit_address/<int:address_id>/',views.edit_address,name='edit_address'),
    path('order_details/',views.user_orders,name='order_details')

]