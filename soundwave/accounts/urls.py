from django.urls import path
from . import views

urlpatterns=[
    path('user_accounts/',views.user_account_view,name='user_account'),
    path('add_address/',views.add_address,name='add_address'),
    path('view_address/',views.view_address,name='view_address'),
    path('order_details',views.view_orders,name='order_details')

]