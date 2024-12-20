from django.urls import path
from . import views

urlpatterns=[
    path('view_offers/',views.view_offer,name='view_offers'),
    path('add_product_offer/',views.add_product_offer,name='add_product_offer'),
    path('edit_product_offer/<int:product_offer_id>/',views.edit_product_offer,name='edit_product_offer'),
    path('activate_product_offer/<int:product_offer_id>',views.activate_product_offer,name='activate_product_offer'),
    path('deactivate_product_offer/<int:product_offer_id>',views.deactivate_product_offer,name='deactivate_product_offer'),
    path('add_brand_offer/',views.add_brand_offer,name='add_brand_offer'),
    path('edit_brand_offer/<int:brand_offer_id>/',views.edit_brand_offer,name='edit_brand_offer'),
    path('activate_brand_offer/<int:brand_offer_id>',views.activate_brand_offer,name='activate_brand_offer'),
    path('deactivate_brand_offer/<int:brand_offer_id>',views.deactivate_brand_offer,name='deactivate_brand_offer') 
    
]