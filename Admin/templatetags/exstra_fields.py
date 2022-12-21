from django.template.defaulttags import register
import json

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def convert(dictionary, key):
    return dictionary[key]

@register.filter
def check(str):
    return type(str)

@register.filter
def get_items(dictionary):
    return(dictionary.items())


