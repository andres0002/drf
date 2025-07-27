# py
import re
from datetime import datetime
# django
# drf
from rest_framework.response import Response
from rest_framework import status
# third
# own

def validar_pk_numerico(pk):
    try:
        return int(pk), None
    except (ValueError, TypeError):
        return None, Response(
            {'error': 'El ID debe ser numérico.'},
            status=status.HTTP_400_BAD_REQUEST
        )

def validar_slug(slug):
    SLUG_REGEX = re.compile(r'^[-a-zA-Z0-9_]+$')
    if not isinstance(slug, str) or not SLUG_REGEX.match(slug):
        return None, Response(
            {'error': 'El slug es inválido.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    return slug, None

def validate_files_with_copy(request, field, update=False):
    """
    :params
    :request: request.data.copy() # forma mas segura y recomendada en buenas practicas.
    :field: key of file
    """
    if update:
        if type(request[field]) == str:
            request.__delitem__(field)
    else:
        if type(request[field]) == str:
            request.__setitem__(field, None)
    return request

def validate_files_no_copy(request, field, update=False):
    """
    :params
    :request: request.data # forma brusca.
    :field: key of file
    """
    request._mutable = True
    if update:
        if type(request[field]) == str:
            del request[field]
    else:
        request[field] = None if type(request[field]) == str else request[field]
    request._mutable = False
    return request

def format_date(date):
    date = datetime.strptime(date, "%d/%m/%y")
    return f"{date.year}-{date.month}-{date.day}"