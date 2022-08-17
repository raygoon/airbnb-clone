import uuid
from django import template

register = template.Library()


@register.simple_tag
def uuid_code():
    code = uuid.uuid4().hex[:10]
    return code
