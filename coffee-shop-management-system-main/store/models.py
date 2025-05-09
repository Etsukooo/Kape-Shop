from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    ARABICA = 'Arabica'
    ROBUSTA = 'Robusta'
    LIBERICA = 'Liberica'
    EXCELSA = 'Excelsa'
    COFFEE_TYPE_CHOICES = [
        (ARABICA, 'Arabica'),
        (ROBUSTA, 'Robusta'),
        (LIBERICA, 'Liberica'),
        (EXCELSA, 'Excelsa'),
    ]

    name = models.CharField(max_length=200)
    coffee_type = models.CharField(max_length=20, choices=COFFEE_TYPE_CHOICES, default=ARABICA)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to='products/', blank=True, null=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    COD = 'COD'
    GCASH = 'GCASH'
    DEBIT = 'DEBIT'
    CREDIT_CARD = 'CREDIT_CARD'
    PAYMENT_MODE_CHOICES = [
        (COD, 'Cash on Delivery'),
        (GCASH, 'GCASH'),
        (DEBIT, 'Debit Card'),
        (CREDIT_CARD, 'Credit Card'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_at = models.DateTimeField(auto_now_add=True)
    is_ordered = models.BooleanField(default=False)
    payment_mode = models.CharField(max_length=20, choices=PAYMENT_MODE_CHOICES, default=COD)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Cart of {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in {self.cart.user.username}'s cart"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.user.username
