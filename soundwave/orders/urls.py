from django.urls import path
from . import views

urlpatterns=[
    path('checkout/',views.checkout,name='checkout'),
    path('order_confirmation/',views.order_confirm,name='order_confirmation'),
    path('view_orders',views.view_orders,name='view_orders'),
    path('orders/change-status/<int:order_item_id>/<str:new_status>/', views.change_order_status, name='change_order_status'),
    path('checkout_address/',views.checkout_address,name='checkout_address'),
    path('place_order/',views.place_order,name='place_order')
]