from django.urls import path
from . import views

urlpatterns=[  
    path('list-products/', views.view_product,name='list_product'),
    path('add-products/', views.add_products,name='add_products'),
    path('list-category/', views.view_category,name='list_category'),
    path('add-category/', views.add_category,name='add_category'),
    path('add-subcategory/<int:id>',views.add_subcategory,name='add_subcategory'),
    path('view-subcategory/<int:id>',views.view_subcategory,name='view_subcategory'),
    path('list-brand/',views.view_brand,name='list_brand'),
    path('add-brand/',views.add_brand,name='add_brand'),
    path('list-varient/<int:id>',views.view_varient,name='list_variant'),
    path('add-varient/<int:id>',views.add_variant,name='add_variant'),
    path('edit-category<int:id>',views.edit_category,name='edit_category'),
    path('edit-subcategory<int:id>,',views.edit_subcategory,name='edit_subcategory'),
    path('edit-brand/<int:id>',views.edit_brand,name='edit_brand'),
    path('edit-product/<int:id>',views.edit_product,name='edit_product'),
    path('list_category/<int:id>',views.list_category,name='list_category'),
    path('unlist_category/<int:id>',views.unlist_category,name='unlist_category'),
    path('list_brand/<int:id>',views.list_brand,name='list_brand'),
    path('unlist_brand/<int:id>',views.unlist_brand,name='unlist_brand'),
    path('list_product/<int:id>',views.list_product,name='list_product'),
    path('unlist_product/<int:id>,',views.unlist_product,name='unlist_product'),
    path('edit-vaiant/<int:id>',views.edit_variant,name='edit_variant'),
]