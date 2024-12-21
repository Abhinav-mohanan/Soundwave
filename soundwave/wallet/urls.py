from django.urls import path
from . import views

urlpatterns=[
    path('wallet_view/',views.wallet_view,name='wallet_view')

]