from django import template
import locale
from django.template.defaultfilters import floatformat
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
register = template.Library()
 
 
@register.filter(name='currency')
def currency(value):
    return locale.currency(float(value), grouping=True)
 
@register.filter(name='percent')
def percent(value):
  if value is None:
    return None
  elif value < 0:
  	return "<div class='red'>" + str(floatformat(float(value) * 100.0, 2) + '%') + "</div>"
  else:
  	return floatformat(float(value) * 100.0, 2) + '%'
  
@register.filter(name='colorize')
def colorize(value):
	if value < 0:
		return "<div class='red'>" + str(value) + "</div>"
	else:
		return value