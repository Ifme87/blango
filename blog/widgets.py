from django.urls import reverse
from django.utils.safestring import mark_safe
from django.forms import widgets
from django.conf import settings


class RelatedFieldWidgetCanAdd(widgets.SelectMultiple):
    def __init__(self, related_model, related_url=None, *args, **kw):

        super(RelatedFieldWidgetCanAdd, self).__init__(*args, **kw)

        if not related_url:
            rel_to = related_model
            info = (rel_to._meta.app_label, rel_to._meta.object_name.lower())
            related_url = 'admin:%s_%s_add' % info

        # Be careful that here "reverse" is not allowed
        self.related_url = related_url

    def render(self, name, value, *args, **kwargs):
        self.related_url = reverse(self.related_url)
        output = ['<div class="row"><div class="col">']
        output.append(super(RelatedFieldWidgetCanAdd, self).render(name, value, *args, **kwargs))
        #output.insert(
        #    0, 
        #    '<div class="row"><div class="col">'
        #)
        output.append(
            '</div>'
            '<div class="col">'
            '<a href="%s" class="add-another" id="add_id_%s"> ' % (self.related_url, name)
        )
        output.append(
            '<img src="%simg/plus.png" width="25" height="25" style="vertical-align:middle">' % (settings.STATIC_URL)
        )
        output.append(
            '</a>'
            '</div>'
            '</div>'
        )
        return mark_safe(''.join(output))