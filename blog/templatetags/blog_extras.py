from django.contrib.auth import get_user_model
from django import template

# from django.utils.html import escape
# from django.utils.safestring import mark_safe
from django.utils.html import format_html
from blog.models import Post
import logging

logger = logging.getLogger(__name__)
user_model = get_user_model()
register = template.Library()

"""
#access template context
@register.simple_tag(takes_context=True)
def author_details_tag(context):
    request = context["request"]
    current_user = request.user
    post = context["post"]
    author = post.author

    if author == current_user:
        return format_html("<strong>me</strong>")

    if author.first_name and author.last_name:
        name = f"{author.first_name} {author.last_name}"
    else:
        name = f"{author.username}"

    if author.email:
        prefix = format_html('<a href="mailto:{}">', author.email)
        suffix = format_html("</a>")
    else:
        prefix = ""
        suffix = ""

    return format_html("{}{}{}", prefix, name, suffix)

And in template:
<small>By {% author_details_tag %} on {{ post.published_at|date:"M, d Y" }}</small>
"""

# without accessing template context
@register.filter  # (name="author_details") - to customize name of the func
def author_details(author, current_user=None):
    if not isinstance(author, user_model):
        # return empty string as safe default
        return ""

    if author == current_user:
        return format_html("<strong>me</strong>")

    if author.first_name and author.last_name:
        # string can be inside escape() - safe, string will be interpreted as a string, no matter if html is in
        name = f"{author.first_name} {author.last_name}"
    else:
        name = f"{author.email}"

    if author.email:
        prefix = format_html('<a href="mailto:{}">', author.email)
        suffix = format_html("</a>")
    else:
        prefix = ""
        suffix = ""

    # except format_html, there can be mark_safe - later injected html will be interpreted as html, but not a text
    # format_html works 1) as str.format and escape every var 2) "mark_safe" with str argument  == format_html with str argument
    return format_html("{}{}{}", prefix, name, suffix)


@register.simple_tag  # (name="author_details") - to customize name of the func
def row(extra_classes=""):
    return format_html('<div class="row {}">', extra_classes)


@register.simple_tag  # (name="author_details") - to customize name of the func
def endrow():
    return format_html("</div>")


@register.simple_tag  # (name="author_details") - to customize name of the func
def col(extra_classes=""):
    return format_html('<div class="col {}">', extra_classes)


@register.simple_tag  # (name="author_details") - to customize name of the func
def endcol():
    return format_html("</div>")


@register.inclusion_tag("blog/post-list.html")
def recent_posts(post):
    posts = Post.objects.exclude(pk=post.pk).order_by("-pk")[:3]
    logger.debug("Loaded %d recent posts for post %d", len(posts), post.pk)
    return {"title": "Recent Posts", "posts": posts}
