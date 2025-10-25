

# from django.db import models
# from users.models import User
# from products.models import Product

# class Order(models.Model):
#     STATUS_CHOICES = (
#         ('Pending', 'Pending'),
#         ('Shipped', 'Shipped'),
#         ('Delivered', 'Delivered'),
#     )

#     PAYMENT_METHOD_CHOICES = (
#         ('Cash on Delivery', 'Cash on Delivery'),
#         ('Razorpay Online Payment', 'Razorpay Online Payment'),
#     )

#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
#     total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     address = models.CharField(max_length=255)
#     payment_method = models.CharField(max_length=30, choices=PAYMENT_METHOD_CHOICES, default='Cash on Delivery')
#     payment_id = models.CharField(max_length=100, blank=True, null=True)  # Razorpay payment id
#     is_paid = models.BooleanField(default=False)  # Track payment status
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
#     date = models.DateTimeField(auto_now_add=True)

#     def save(self, *args, **kwargs):
#         if self.pk:
#             self.total = sum(item.subtotal() for item in self.items.all())
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f"Order #{self.id} - {self.user.username}"


# class OrderItem(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=1)

#     def subtotal(self):
#         return self.product.price * self.quantity

#     def __str__(self):
#         return f"{self.product.title} x {self.quantity}"


from django.db import models
from users.models import User
from products.models import Product

class Order(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
    )

    PAYMENT_METHOD_CHOICES = (
        ('Cash on Delivery', 'Cash on Delivery'),
        ('Razorpay Online Payment', 'Razorpay Online Payment'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    address = models.CharField(max_length=255)
    payment_method = models.CharField(max_length=30, choices=PAYMENT_METHOD_CHOICES, default='Cash on Delivery')
    payment_id = models.CharField(max_length=100, blank=True, null=True)  # Razorpay payment id
    is_paid = models.BooleanField(default=False)  # Track payment status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.pk:
            self.total = sum(item.subtotal() for item in self.items.all())
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.product.title} x {self.quantity}"
