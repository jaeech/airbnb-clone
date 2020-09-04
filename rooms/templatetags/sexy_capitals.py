from django import template

register = template.Library()


@register.filter
# value는 html에서 받아오는 것
# 그 뒤에 이를 가지고 가공해서, return valeu를
# 보내주는 것
def sexy_capitals(value):
    return value.upper()
