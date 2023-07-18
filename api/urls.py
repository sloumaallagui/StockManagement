from django.urls import path
from . import views


urlpatterns = [
    path('export/', views.export, name='export'),
    
    path('group/create/', views.group_create, name='group_create'),
    path('group/<int:group_id>/delete/', views.group_delete, name='group_delete'),
    path('group/<int:group_id>/update/', views.group_update, name='group_update'),
    path('group/list/', views.group_list, name='group_list'),
    path('group/<int:group_id>/detail/', views.group_detail, name='group_detail'), 
    path('group/list/all/', views.group_list_all, name='group_list_all'),

    path('group/<int:group_id>/product/list/', views.group_product_list, name='group_product_list'),
    path('group/<int:group_id>/primary/list/', views.group_primary_list, name='group_primary_list'),
    path('group/<int:group_id>/base/list/', views.base_list_by_group, name='group_base_list'),

    path('product/create/', views.product_create, name='product_create'),
    path('product/<int:product_id>/delete/', views.product_delete, name='product_delete'),
    path('product/<int:product_id>/update/', views.product_update, name='product_update'),
    path('product/list/', views.product_list, name='product_list'),
    path('product/<int:product_id>/detail/', views.product_detail, name='product_detail'),
    path('product/<str:product_name>/search/', views.product_search, name='product_search'),
    path('product/<int:product_id>/primary/list/', views.product_primary_list, name='product_primary_list'),
    path('product/list/all/', views.product_list_all, name='product_list_all'),
      
    path('primary/create/', views.primary_create, name='primary_create'),
    path('primary/<int:primary_id>/delete/', views.primary_delete, name='primary_delete'),
    path('primary/<int:primary_id>/update/', views.primary_update, name='primary_update'),
    path('primary/list/', views.primary_list, name='primary_list'),
    path('primary/<int:primary_id>/detail/', views.primary_detail, name='primary_detail'),
    path('primary/<str:primary_name>/search/', views.primary_search, name='primary_search'),
    
    path('base/create/', views.base_create, name='base_create'),
    path('base/<int:base_id>/delete/', views.base_delete, name='base_delete'),
    path('base/<int:base_id>/update/', views.base_update, name='base_update'),
    path('base/list/', views.base_list, name='base_list'),
    path('base/<int:base_id>/detail/', views.base_detail, name='base_detail'),
    path('base/<str:base_name>/search/', views.base_search, name='base_search'),

]