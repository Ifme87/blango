from django.contrib.auth import get_user_model
from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe

user_model = get_user_model()
register = template.Library()


@register.filter#(name="author_details") - to customize name of the func
def author_details(author):
  if not isinstance(author, user_model):
      # return empty string as safe default
      return ""

  if author.first_name and author.last_name:
      #escape() - safe, string will be interpreted as a string, no matter if html is in
      name = escape(f"{author.first_name} {author.last_name}") 
  else:
      name = escape(f"{author.username}")

  if author.email:
      email = escape(author.email)
      prefix = f'<a href="mailto:{email}">'
      suffix = "</a>"
  else:
      prefix = ""
      suffix = ""

  #mark_safe - later injected html will be interpreted as html, but not a text
  return mark_safe(f"{prefix}{name}{suffix}") 
        