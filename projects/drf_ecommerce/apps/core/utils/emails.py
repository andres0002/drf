# py
# django
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
# drf
# third
from decouple import config  # type: ignore
# own

# general
def load_template_with_context_general(**kwargs):
    # Carga plantilla HTML con contexto
    html_content = render_to_string(kwargs.get('template_name'), kwargs.get('context'))
    return html_content

def send_email_general(**kwargs):
    body = load_template_with_context_general(**kwargs.get('body'))
    email = EmailMultiAlternatives(
        from_email=config('EMAIL_HOST_USER_DEV'), # app, web.
        subject=kwargs.get('subject'),
        body=body,
        to=kwargs.get('to'),
        reply_to=kwargs.get('reply_to'),
    )
    try:
        # Adjuntar HTML como alternativa
        email.attach_alternative(body, "text/html")
        email.send()
        # ok...
        return (True,'Ningúno.')
    except Exception as error:
        # error...
        return (False,error)