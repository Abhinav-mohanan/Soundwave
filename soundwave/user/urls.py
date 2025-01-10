from django.urls import path
from . import views

urlpatterns=[
    path('signup/',views.signup,name='signup'),
    path('otp_validation/',views.otp_generation,name='otp_validation'),
    path('login/',views.user_login,name='user_login'),
    path('resend_otp/',views.resend_otp,name='resend_otp'),
    path('user_logout/',views.user_logout,name='user_logout'),
    path('',views.homepage,name='home'),
    path('productslist/',views.product_page,name='products'),
    path('details/<int:product_id>/<int:variant_id>/',views.product_detail,name='product_details'),
    path('search/', views.search_view, name='search'),
    path('forgot_password/',views.forgotpassword,name='forgot_password'),
    path('forgot_password_verify/',views.forgot_password_verify,name='forgot_password_verify'),
    path('reset_password/',views.reset_password,name='reset_password'),
    path('about_us',views.about_us,name='about_us'),
    path('help_page',views.helppage,name='help_page')
    
]  
