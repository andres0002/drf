# py
# django
from django.shortcuts import redirect
# drf
# third
# own

class SwaggerAndReDocLoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        protected_paths = [
            '/swagger/',
            '/swagger.json/',
            '/swagger/?format=openapi',
            '/redoc/',
            '/redoc.json/',
            '/redoc/?format=openapi',
        ]

        if any(request.path.startswith(path) for path in protected_paths):
            if not request.user.is_authenticated:
                return redirect(f'/accounts/login/?next={request.META.get('PATH_INFO')}') # Ajusta la URL de login si es otra

        return self.get_response(request)