from django.test import TestCase
from .models import *

class TestClass(TestCase):
    def setup(self):
        Product.objects.get(id=1)
