from django import template

register = template.Library()


@register.filter
def make_short_name(company_name, director_name):
    if company_name:
        return f"ТОВ «{company_name}»"

    return f"ФОП {director_name}"


@register.filter
def make_full_name(company_name, edrpou):
    if len(edrpou) == 10:
        return f"Фізична особа-підприємець {company_name}"
    elif len(edrpou) == 8:
        return f"Товариство з обмеженою відповідальністю «{company_name}»"
    else:
        return company_name


@register.filter(name="add_attrs")
def add_attrs(field, attrs):
    """
    Adds attributes to a form field.
    Usage: {{ field|add_attrs:"x-model:id_field_name" }}
    """
    attr_name, attr_value = attrs.split(":")
    field.field.widget.attrs[attr_name] = attr_value
    return field
