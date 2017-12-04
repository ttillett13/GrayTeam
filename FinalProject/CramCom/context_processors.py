"""from django import template
from django.conf import settings

register = template.Library()

@register.tag
def FEATURES(request):
    return settings.FEATURES"""
from django.conf import settings
from django.shortcuts import render_to_response

def BASE_DIR(request):
    return {'BASE_DIR': settings.BASE_DIR}