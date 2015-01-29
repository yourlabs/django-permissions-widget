from django import template
from django.utils.translation import ugettext

register = template.Library()


@register.filter
def get_item(d, key):
    return d.get(key, None)


@register.filter(name='translate')
def translate(text):
    return ugettext(text)


@register.tag
def capture(parser, token):
    """
    Capture contents of block into context
    --------------------------------------

    Use case: variable accessing based on current variable values.

    {% capture foo %}{{ foo.value }}-suffix{% endcapture %}
    {% if foo in bar %}{% endif %}

    Created on Monday, February 2012 by Yuji Tomita
    """
    nodelist = parser.parse(('endcapture',))
    parser.delete_first_token()
    varname = token.contents.split()[1]
    return CaptureNode(nodelist, varname)


class CaptureNode(template.Node):
    def __init__(self, nodelist, varname):
        self.nodelist = nodelist
        self.varname = varname

    def render(self, context):
        context[self.varname] = self.nodelist.render(context)
        return ''