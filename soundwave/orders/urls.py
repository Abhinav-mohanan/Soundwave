from django.urls import path
from . import views

urlpatterns=[
    path('checkout/',views.checkout,name='checkout'),
    path('order_confirmation/',views.order_confirmation,name='order_confirmation'),
    path('view_orders',views.view_orders,name='view_orders'),
    path('orders/change-status/<int:order_item_id>/<str:new_status>/', views.change_order_status, name='change_order_status'),
    path('checkout_address/',views.checkout_address,name='checkout_address'),
    path('place_order/',views.place_order,name='place_order'),
    path('verify_payment',views.verify_payment,name='verify_payment'),
    path('cancel_orderitem/<int:order_item_id>',views.cancel_order_item,name='cancel_order_item'),
    path('return_order/<int:orderitem_id>/',views.return_order,name='return_order'),
    path('generate_invoice/<int:order_id>/', views.generate_invoice, name='generate_invoice'),
    path('orderitems_details/<int:order_id>',views.orderitems_detail,name='orderitems_details'),
    path('retry_payment/<int:order_id>/',views.retry_payment,name='retry_payment'),
    path('verify_retry_payment/',views.verify_retry_payment,name='verify_retry_payment')
]