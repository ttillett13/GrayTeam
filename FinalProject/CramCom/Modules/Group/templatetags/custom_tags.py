# from django import template
# from django.forms import CheckboxInput
#
# register = template.Library()
#
# @register.filter(name='is_checkbox')
# def is_checkbox(field):
#   return field.field.widget.__class__.__name__ == CheckboxInput().__class__.__name__
#
# @register.filter(name='pass_react')
# def pass_react(field):
#   return field.field.widget.__class__.__name__ == CheckboxInput().__class__.__name__