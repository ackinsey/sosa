from django import template
from old.models import Section

register = template.Library()

class SectionNode(template.Node):
    def render(self,context):
        context['section_list']=Section.objects.all().order_by('order')
        return ''

@register.tag
def get_sections(parser,token):
    return SectionNode()
