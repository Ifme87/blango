from django.contrib.auth import get_user_model
from django import template
#from django.utils.html import escape
#from django.utils.safestring import mark_safe
from django.utils.html import format_html

user_model = get_user_model()
register = template.Library()


@register.filter#(name="author_details") - to customize name of the func
def author_details(author):
  if not isinstance(author, user_model):
      # return empty string as safe default
      return ""

  if author.first_name and author.last_name:
      #string can be inside escape() - safe, string will be interpreted as a string, no matter if html is in
      name = f"{author.first_name} {author.last_name}"
  else:
      name = f"{author.username}"

  if author.email:
      prefix = format_html('<a href="mailto:{}">', author.email)
      suffix = format_html("</a>")
  else:
      prefix = ""
      suffix = ""

  #except format_html, there can be mark_safe - later injected html will be interpreted as html, but not a text
  #format_html works 1) as str.format and escape every var 2) mark_safe == format_html 
  return format_html('{}{}{}', prefix, name, suffix) 
        