import json
from io import BytesIO

import requests
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    print(result.getvalue())
    pdf = pisa.pisaDocument(BytesIO(html.encode("utf-8")), result)
    return HttpResponse(result.getvalue(), content_type='application/pdf')
    if not pdf.err:

        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None