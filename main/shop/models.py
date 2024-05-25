from django.db import models
from django.core.validators import RegexValidator
import re
import uuid

phone_regex = RegexValidator(
    regex="^(?:(?:\+|00)98|0)?9\d{9}$",
    message="Please enter a valid Iranian phone number."
)

password_validator = RegexValidator(
    regex=r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[^\w\s]).{8,}$',
    message="Passwords must be at least 8 characters long and contain "
            "at least one digit, one lowercase letter, one uppercase "
            "letter, and one non-alphanumeric character.",
)



class Profile(models.Model):
    username = models.CharField(max_length=200, null=False, unique=True , blank=False)
    email = models.EmailField(max_length=50, null=False, unique=True , blank=False)
    fullname = models.CharField(max_length=20, null=False , blank=False)
    address = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(validators=[phone_regex], max_length=13, blank=True)
    def save(self, *args, **kwargs):
        # Use regular expression to extract only the digits from the phone number
        digits_only = re.sub(r'\D', '', self.phone_number)
        if self.phone_number.startswith("98"):
        # Prepend "0" to the extracted digits to remove the country code
            digits_only = "0" + digits_only[2:]
        formatted_number = digits_only.lstrip('0')
        self.phone_number = formatted_number
        super().save(*args, **kwargs)

    password = models.CharField(max_length=128, validators=[password_validator], null=False)
    created_at = models.DateTimeField(auto_now =True , editable=False)
    is_confirmed =  models.BooleanField(default = False)

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # image = models.ImageField(upload_to='products/', null=True, blank=True)
    quantity = models.PositiveIntegerField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')
    
    def __str__(self):
        return f"Image for {self.product.name}"


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
    
