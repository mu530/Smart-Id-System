from django import template

register = template.Library()


@register.filter
def add_bootstrap_validator(field):
    css_classes = field.field.widget.attrs.get("class", "")
    if field.errors:
        css_classes += " is-invalid"
    field.field.widget.attrs["class"] = css_classes
    return field


@register.filter
def add_custom_class(field, custom_class):
    css_classes = field.field.widget.attrs.get("class", "")
    css_classes += f" {custom_class}"
    field.field.widget.attrs["class"] = css_classes
    return field
