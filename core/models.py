from django.db import models
from django.contrib.auth.models import User
import datetime
from django.urls import reverse
from datetime import timedelta
from django.utils import timezone

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


def default_category_fields():
    return {'title': 'text', 'price': 'number', 'description': 'text'}


class Product(models.Model):
    date = models.DateTimeField(
        null=True, blank=True, default=timezone.now() + timedelta(hours=3))
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    expire_date = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=100, null=True, choices=PRODUCT_STATUS)
    category = models.ForeignKey(
        'Category', on_delete=models.CASCADE, null=True)
    subCategory = models.ForeignKey(
        'SubCategory', on_delete=models.CASCADE, null=True)
    photos = models.JSONField()
    fields = models.JSONField()
    uudi = models.CharField(max_length=100, null=True)
    views = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse('edit_product', kwargs={'pk': self.pk})


class Category(models.Model):
    name = models.CharField(max_length=500, null=True, blank=True)
    photo = models.CharField(max_length=500, null=True, blank=True)
    status = models.CharField(
        choices=CATEGORY_STATUS, null=True, blank=True, max_length=100, default='approved')
    fields = models.JSONField(null=True, default=default_category_fields)

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
    date = models.DateTimeField(default=datetime.date.today, blank=True)
    expire_date = models.DateField(null=True, blank=True)
    contact = models.CharField(max_length=100, null=True)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=500, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.date.today)
    replaies = models.ManyToManyField('CommentReplay')


class CommentReplay(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=500, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.date.today)


class About(models.Model):
    app_name = models.CharField(max_length=100, null=True, blank=True)
    icon_link = models.CharField(max_length=1000, null=True, blank=True)
    privacy_policy = models.CharField(max_length=100000, null=True, blank=True)
    about_us = models.CharField(max_length=10000, null=True, blank=True)
    contact_number = models.CharField(max_length=100, null=True, blank=True)
    whatsapp_number = models.CharField(max_length=100, null=True, blank=True)
    agree_text = models.CharField(max_length=100000, null=True, blank=True)
    payment_info_text = models.CharField(
        max_length=100000, null=True, blank=True)
    payment_info_link = models.CharField(
        max_length=1000, null=True, blank=True)
    product_expire_days = models.IntegerField(null=True, blank=True)
    products_num = models.IntegerField(default=0, blank=True)


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.CharField(max_length=1000)
    date = models.DateField(default=datetime.date.today)
