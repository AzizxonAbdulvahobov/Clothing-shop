from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('detail/<int:product_id>/', views.detail, name='detail'),
    path('category/<int:category>/', views.category_detail, name='category'),
    path('shop/', views.shop, name='shop'),
    path('cart/', views.cart, name='cart'),
    path('to_cart/<int:product_id>/<str:action>/', views.to_cart, name='to_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('register/', views.register, name='register'),
    path('log-in', views.log_in, name='log_in'),
    path('log-out', views.log_out, name='log_out')
]
