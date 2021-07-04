"""Custom tempalte tags for explorer project."""
from typing import List

from django import template
from django.core.handlers.wsgi import WSGIRequest

register = template.Library()


@register.simple_tag
def get_values_url(value: str, request: WSGIRequest) -> str:
    """Get new URL based on whether or not param is in kwarg"""
    values_params: str = request.GET.get("values", "")
    values_list: List[str] = []
    if values_params:
        values_list = values_params.split(",")
        if value in values_list:
            values_list.remove(value)
        else:
            values_list.append(value)
    else:
        values_list.append(value)

    return f"{request.path}?values={','.join(values_list)}"
