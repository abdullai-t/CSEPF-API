from django import template

register = template.Library()


@register.filter
def add_class(field, css):
    existing_class = field.field.widget.attrs.get("class", "")
    return field.as_widget(attrs={"class": "{} {}".format(existing_class, css)})
