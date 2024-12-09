from django.urls import path
from . import views

urlpatterns=[
    path('cart/',views.cart_detil,name='cart_detail'),
    path('cart/add/<int:variant_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>',views.update_cart_item,name='update_cart_item'),
    path('cart/remove/<int:cartitem_id>/',views.remove_from_cart,name='remove_from_cart'),
    path('cart/update/<int:cartitem_id>/', views.update_cart_quantity, name='update_cart_quantity')
    
]