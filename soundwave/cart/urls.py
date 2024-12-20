from django.urls import path
from . import views

urlpatterns=[
    path('cart/',views.cart_detail,name='cart_detail'),
    path('cart/add/<int:variant_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('cart/remove/<int:cartitem_id>/',views.remove_from_cart,name='remove_from_cart'),
    path('whilist/add/<int:variant_id>/',views.add_wishlist,name='add_to_wishlist'),
    path('wishlist/',views.view_wishlist,name='wishlist_details'),
    path('wishlist/remove/<int:item_id>',views.remove_from_wishlist,name='remove_from_wishlist'),
    
]