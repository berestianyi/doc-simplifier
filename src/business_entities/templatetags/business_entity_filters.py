from django import template

register = template.Library()


@register.filter
def make_short_name(company_name, edrpou):
    print(edrpou)
    print(company_name)
    if len(edrpou) == 8:
        return f"ФОП {company_name}"
    elif len(edrpou) == 10:
        return f"ТОВ «{company_name}»"
    else:
        return company_name


@register.filter
def make_full_name(company_name, edrpou):
    if len(edrpou) == 8:
        return f"Фізична особа-підприємець {company_name}"
    elif len(edrpou) == 10:
        return f"Товариство з обмеженою відповідальністю «{company_name}»"
    else:
        return company_name

