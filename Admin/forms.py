from django import forms
from core.models import *


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'


class ADForm(forms.ModelForm):
    class Meta:
        model = AD
        fields = '__all__'


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'status']


class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = '__all__'


class AboutForm(forms.ModelForm):
    class Meta:
        model = About
        fields = '__all__'
        widgets = {
            'about_us': forms.Textarea(attrs={'cols': 30, 'rows': 10}),
            'agree_text': forms.Textarea(attrs={'cols': 30, 'rows': 10}),
            'privacy_policy': forms.Textarea(attrs={'cols': 30, 'rows': 10}),
            'payment_info_text': forms.Textarea(attrs={'cols': 30, 'rows': 10})
        }
