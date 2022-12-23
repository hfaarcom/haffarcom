from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.urls import reverse


PRODUCT_STATUS = [
    ('approved', 'approved'),
    ('declined', 'declined'),
    ('pending', 'pending'),
    ('sold', 'sold'),
    ('Deleted', 'Deleted')
]

CATEGORY_STATUS = [
    ('approved', 'approved'),
    ('disabled', 'disabled')
]

ADS_STATUS = [
    ('approved', 'approved'),
    ('disabled', 'disabled')
]


def get_default():
    return {'title': 'required', 'price': 'required'}


class Product(models.Model):
    date = models.DateField(null=True, blank=True, auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    expire_date = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=100, null=True, choices=PRODUCT_STATUS)
    category = models.ForeignKey(
        'Category', on_delete=models.CASCADE, null=True)
    subCategory = models.ForeignKey(
        'SubCategory', on_delete=models.CASCADE, null=True)
    fields = models.JSONField()

    def get_absolute_url(self):
        return reverse('edit_product', kwargs={'pk': self.pk})


class Category(models.Model):
    name = models.CharField(max_length=500, null=True, blank=True)
    photo = models.CharField(max_length=500, null=True, blank=True)
    status = models.CharField(
        choices=CATEGORY_STATUS, null=True, blank=True, max_length=100, default='approved')
    fields = models.JSONField(null=True, default=get_default)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    mainCategory = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=1000, blank=True, null=True)
    photo = models.CharField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('edit_sub', kwargs={'pk': self.pk})


class AD(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(
        choices=ADS_STATUS, null=True, blank=True, max_length=100)
    photo = models.CharField(max_length=500, null=True, blank=True)
    date = models.DateTimeField(default=datetime.now, blank=True)
    expire_date = models.DateField(null=True, blank=True)
    contact = models.CharField(max_length=100, null=True)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=500, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class About(models.Model):
    app_name = models.CharField(max_length=100, null=True)
    icon_link = models.CharField(max_length=1000, null=True)
    privacy_policy = models.CharField(max_length=100000, null=True)
    about_us = models.CharField(max_length=10000, null=True)
    contact_number = models.CharField(max_length=100, null=True)
    whatsup_number = models.CharField(max_length=100, null=True)
    agree_text = models.CharField(max_length=100000, null=True)
    payment_info_text = models.CharField(max_length=100000, null=True)
    payment_info_link = models.CharField(
        max_length=1000, null=True, blank=True)
    product_expire_days = models.IntegerField(null=True)
