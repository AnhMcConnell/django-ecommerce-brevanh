from django.urls import path
from . import views

app_name = 'my_app'

urlpatterns = [
    path('shop/', views.shop, name='shop'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('shop/update_item/',views.updateItem, name='update_item'),
    path('cart/update_item/', views.updateItem, name='update_item'),
    path('checkout/process_order/',views.processOrder, name='process_order'),
]
