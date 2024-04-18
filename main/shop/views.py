from rest_framework import viewsets
from .models import *
from .serializers import *



class Creatuser(viewsets.ModelViewSet):
    # permission_classes = [IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserSerializer

class Category(viewsets.ModelViewSet):
    # permission_classes = [IsAdminUser]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class Brand(viewsets.ModelViewSet):
    # permission_classes = [IsAdminUser]
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

class Product(viewsets.ModelViewSet):
    # permission_classes = [IsAdminUser]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
