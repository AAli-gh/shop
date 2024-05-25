from django.urls import path
from rest_framework import routers
from django.urls import include, path
from .views import *
router = routers.DefaultRouter()

router.register(r'Creatuser', Creatuser,basename='Creatuser')
router.register(r'Product', Productview,basename='product')
router.register(r'Brand', Brand,basename='Brand')
router.register(r'Category',Category,basename= 'Category')
router.register(r'sign_up', sign_up ,basename='sign_up')
router.register(r'Login', Login ,basename='Login')
router.register(r'view all',view_all,basename='view all')

# router.register(r'ProductList',ProductListView,basename='ProductList')

urlpatterns = [
    path('', include(router.urls)),
    path('UserProfileAPIView/', UserProfileAPIView.as_view(), name='UserProfileAPIView'),
    path('ProductListView/', ProductListView.as_view(), name='ProductListView'),
    path('ProductsearchView/', ProductsearchView.as_view(), name='ProductsearchView'),
    path('cart-items/', CartItemListView.as_view(), name='cart-item-list'),
    path('cart-items/<int:pk>/', CartItemDetailView.as_view(), name='cart-item-detail'),
    path('products/<int:product_id>/images/', ProductImageCreate.as_view(), name='product-image-create'),


]
