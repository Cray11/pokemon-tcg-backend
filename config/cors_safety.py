from django.conf import settings
from django.http import HttpResponse


class CorsSafetyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        self._add_cors_headers(request, response)
        return response

    def process_exception(self, request, exception):
        origin = request.META.get("HTTP_ORIGIN", "")
        allowed = getattr(settings, "CORS_ALLOWED_ORIGINS", [])
        if origin and origin in allowed:
            response = HttpResponse(status=500)
            response["Access-Control-Allow-Origin"] = origin
            response["Access-Control-Allow-Credentials"] = "true"
            response["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
            response["Access-Control-Allow-Methods"] = "GET, POST, PUT, PATCH, DELETE, OPTIONS"
            return response
        return None

    def _add_cors_headers(self, request, response):
        origin = request.META.get("HTTP_ORIGIN", "")
        allowed = getattr(settings, "CORS_ALLOWED_ORIGINS", [])
        if origin and origin in allowed:
            response["Access-Control-Allow-Origin"] = origin
            response["Access-Control-Allow-Credentials"] = "true"
