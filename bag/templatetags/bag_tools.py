from django import template

register = template.Library()

@register.filter(name='calc_subtotal')
def calc_subtotal(price, quantity):
    """Multiply price and quantity to return subtotal."""
    return price * quantity
