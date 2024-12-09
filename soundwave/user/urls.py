from django.urls import path
from . import views

urlpatterns=[
    path('signup',views.signup,name='signup'),
    path('otp_validation',views.otp_generation,name='otp_validation'),
    path('login/',views.user_login,name='user_login'),
    path('resend_otp/',views.resend_otp,name='resend_otp'),
    path('user_logout/',views.user_logout,name='user_logout'),
    path('',views.homepage,name='home'),
    path('productslist/',views.product_page,name='products'),
    path('details/<int:product_id>/<int:variant_id>',views.details_pro,name='product_details'),
    path('search/', views.search_view, name='search')
    
]  
