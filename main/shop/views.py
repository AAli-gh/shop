from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import APIException
from rest_framework import  permissions, status
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.views import APIView
from django.core.mail import send_mail 
from django.http import Http404
import time
import pytz
from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import mixins, generics
from rest_framework.exceptions import AuthenticationFailed
from datetime import datetime
from django.db import IntegrityError
from django.core.cache import cache
from datetime import date


class Creatuser(viewsets.ModelViewSet):
    # permission_classes = [IsAdminUser]
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

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


class view_all(mixins.ListModelMixin, viewsets.GenericViewSet):   
    queryset =  Profile.objects.all()
    serializer_class = ProfileSerializer
    

class sign_up(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            
     
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            expiration_timestamp = refresh.access_token['exp']

            tehran_timezone = pytz.timezone('Asia/Tehran')
            expiration_datetime_utc = datetime.utcfromtimestamp(expiration_timestamp)
            expiration_datetime_teheran = expiration_datetime_utc.replace(tzinfo=pytz.utc).astimezone(tehran_timezone)
            expiration_time_teheran = expiration_datetime_teheran.strftime('%H:%M:%S %Z')
            token = {
                'access': access_token,
                'expires_at': expiration_time_teheran,
            }

            user.refresh_token = access_token
            user.save()

            return Response({
                "token": token,
            })
        except APIException as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
            return Response({"error":"IntegrityError occurred !!"})
        except Exception as e:
            return Response({"error": "An unexpected error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class Login(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = LoginSerializer
    def create(self, request, *args, **kwargs):
        try:
            rate_limit_key = f'rate_limit:{request.data.get("username")}' 
            request_count = cache.get(rate_limit_key, 0)
            if request_count >= 5: 
                return Response({'error': 'Too Many Requests'}, status=status.HTTP_429_TOO_MANY_REQUESTS)

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)

            expiration_timestamp = refresh.access_token['exp']
            tehran_timezone = pytz.timezone('Asia/Tehran')
            expiration_datetime_utc = datetime.utcfromtimestamp(expiration_timestamp)
            expiration_datetime_teheran = expiration_datetime_utc.replace(tzinfo=pytz.utc).astimezone(tehran_timezone)
            expiration_time_teheran = expiration_datetime_teheran.strftime('%H:%M:%S %Z')

            
            cache.set(rate_limit_key, request_count + 1, 160)  

            return Response({
                'access': str(refresh.access_token),
                'expires_at': expiration_time_teheran,
            })
        except ObjectDoesNotExist:
            raise Http404("User profile not found")
        except AuthenticationFailed:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        except serializers.ValidationError as e:
            return Response({'error': 'Bad Request', 'details': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': 'An unexpected error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)