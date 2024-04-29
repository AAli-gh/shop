from django.urls import path
from rest_framework import routers
from django.urls import include, path
from .views import *
router = routers.DefaultRouter()

router.register(r'Creatuser', Creatuser,basename='Creatuser')
router.register(r'Product', Product,basename='product')
router.register(r'Brand', Brand,basename='Brand')
router.register(r'Category',Category,basename= 'Category')
router.register(r'sign_up', sign_up ,basename='sign_up')
router.register(r'Login', Login ,basename='Login')
router.register(r'view all',view_all,basename='view all')

urlpatterns = [
    path('', include(router.urls)),
]
