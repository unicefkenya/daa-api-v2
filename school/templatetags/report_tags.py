from django import template
from django.template import RequestContext
from django.template.loader import render_to_string


register = template.Library()


class ReportStartEndTag(template.Node):
    def render(self, context):
        try:
            context = context.flatten()
        except Exception as e:
            print(e)
            context = {}

        rendered_template = render_to_string("tags/report_start_end.html", context=context)
        return rendered_template


@register.tag("report_start_end_date")
def report_start_end_date(parser, token):
    return ReportStartEndTag()
