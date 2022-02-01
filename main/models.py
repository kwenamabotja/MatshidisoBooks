from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver

from bellabooks.settings import VAT
from main.enums import ProvinceType


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100, null=True, blank=True)
    price = models.FloatField()
    cover_image = models.ImageField(upload_to='uploads/cover/', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    mobile_number = models.CharField(max_length=15)
    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.email} - {self.mobile_number} - {self.message}"


class Address(models.Model):
    line_1 = models.CharField(max_length=30)
    line_2 = models.CharField(max_length=30)
    suburb = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    # province = models.Choices(ProvinceType)
    postal_code = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.line_1}, {self.line_2}, {self.suburb}, {self.city}"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    paid = models.BooleanField(default=False)
    payment_reference = models.CharField(max_length=50, blank=True, null=True)
    delivery_address = models.CharField(max_length=150, blank=True, null=True)
    delivered = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total(self):
        # items = OrderItem.objects.filter(order=self)
        sum= 0.0
        for order_item in OrderItem.objects.filter(order=self):
            sum += order_item.item.price * order_item.quantity
        return sum * (1 + VAT)

    @property
    def get_items(self):
        return OrderItem.objects.filter(order=self)

    def __str__(self):
        return f"Order {self.pk}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING)
    item = models.ForeignKey(Book, on_delete=models.DO_NOTHING)
    quantity = models.PositiveIntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Item {self.pk} of Order {self.order.pk}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)
    # other fields...


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class RequestLog(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.IPAddressField()
    request = models.TextField()
    response = models.TextField()
    response_code = models.IntegerField(default=0)
    duration = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Request: {self.request} \n Response: {self.response} \n  Code: {self.response_code}"