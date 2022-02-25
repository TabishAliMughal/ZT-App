from io import BytesIO                                                              # import windows file opener
from django.http import HttpResponse                                                # import httpresponce
from django.template.loader import get_template                                     # import the whole template
from xhtml2pdf import pisa                                                          # import python module

def PdfMaker(template_src, context_dict={}):                                        # Define Function Called From Views
    template = get_template(template_src)                                           # Define Template To Convert To Pdf
    html  = template.render(context_dict)                                           # Define data To Convert To Pdf
    result = BytesIO()                                                              # Windows Builtin Function To Open Files
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)             # Convert Html To Pdf
    if not pdf.err:                                                                 # Check For Errors
        return HttpResponse(result.getvalue(), content_type='application/pdf')      # return if no error
    return None                                                                     # If Got Error In Conversion Return None
