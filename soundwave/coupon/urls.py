from django.urls import path
from . import views

urlpatterns=[
     path('coupons/add/', views.add_coupons, name='add_coupons'),  
     path('coupons/',views.view_coupons,name='view_coupons'),
     path('coupons/edit/<int:coupon_id>',views.edit_coupons,name='edit_coupons'),
     path('coupons/activate/<int:coupon_id>',views.activate_coupon,name='activate_coupon'),
     path('coupons/deactivate/<int:coupon_id>',views.deactivate_coupon,name='deactivae_coupon'),
     path('apply-coupon/',views.apply_coupon,name='apply_coupon'),
     

]