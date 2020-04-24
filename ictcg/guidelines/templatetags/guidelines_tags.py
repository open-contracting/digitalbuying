from django import template

register = template.Library()

@register.simple_tag()
def hex_to_rgb(value):
  """Return (red, green, blue) for the color given as #rrggbb."""
  value = value.lstrip('#')
  lv = len(value)
  return ','.join(str(int(value[i:i + lv // 3], 16)) for i in range(0, lv, lv // 3))