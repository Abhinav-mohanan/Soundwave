from django.urls import path
from . import views

urlpatterns=[
    path('adminn/', views.admin_login,name='admin_login'),
    path('dashboard/', views.admin_home,name='dashboard'),
    path('list-user/',views.user_managment,name='list_user'),
    path('block_user/<int:id>',views.block_user,name='block_user'),
    path('unblock_user/<int:id>',views.unblock_user,name='unblock_user'),
    path('admin-logout/', views.admin_logout,name='logout'),
  
]