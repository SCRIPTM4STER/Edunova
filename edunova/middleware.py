"""
Custom middleware for handling HTTP errors with JSON responses.
"""
import logging
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied, BadRequest
from django.urls import resolve
from django.urls.exceptions import Resolver404

logger = logging.getLogger(__name__)


class CustomErrorMiddleware:
    """
    Middleware to provide user-friendly JSON responses for standard HTTP errors.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        """
        Handle exceptions and return appropriate JSON responses.
        """
        # Handle specific HTTP status codes
        if isinstance(exception, PermissionDenied):
            logger.warning(f"403 Forbidden: {request.path} - {exception}")
            return JsonResponse(
                {
                    'error': 'Forbidden',
                    'detail': str(exception) or 'You do not have permission to access this resource.',
                    'status_code': 403
                },
                status=403
            )
        
        if isinstance(exception, BadRequest):
            logger.warning(f"400 Bad Request: {request.path} - {exception}")
            return JsonResponse(
                {
                    'error': 'Bad Request',
                    'detail': str(exception) or 'The request was malformed or invalid.',
                    'status_code': 400
                },
                status=400
            )
        
        # Handle 404 Not Found for API endpoints
        if isinstance(exception, Resolver404):
            # Only return JSON for API routes
            if request.path.startswith('/api/'):
                logger.warning(f"404 Not Found: {request.path}")
                return JsonResponse(
                    {
                        'error': 'Not Found',
                        'detail': 'The requested resource was not found.',
                        'status_code': 404
                    },
                    status=404
                )
            return None  # Let Django handle non-API 404s
        
        # Handle unexpected exceptions (500)
        if hasattr(exception, '__module__'):
            logger.error(
                f"500 Internal Server Error: {request.path} - {type(exception).__name__}: {exception}",
                exc_info=True
            )
            # Only return JSON for API routes
            if request.path.startswith('/api/'):
                detail = 'An internal server error occurred.'
                if hasattr(exception, 'message'):
                    detail = exception.message
                elif str(exception):
                    detail = str(exception)
                
                # In debug, expose internal error details; hide in production
                try:
                    from django.conf import settings as dj_settings
                    if getattr(dj_settings, 'DEBUG', False):
                        detail = f"{type(exception).__name__}: {str(exception)}"
                except Exception:
                    pass
                
                return JsonResponse(
                    {
                        'error': 'Internal Server Error',
                        'detail': detail,
                        'status_code': 500
                    },
                    status=500
                )
        
        return None  # Let Django handle other exceptions


def handle_404(request, exception):
    """
    Custom 404 handler for API routes.
    """
    if request.path.startswith('/api/'):
        logger.warning(f"404 Not Found: {request.path}")
        return JsonResponse(
            {
                'error': 'Not Found',
                'detail': 'The requested resource was not found.',
                'status_code': 404
            },
            status=404
        )
    # For non-API routes, return None to use default handler
    return None


def handle_400(request, exception):
    """
    Custom 400 handler for API routes.
    """
    if request.path.startswith('/api/'):
        logger.warning(f"400 Bad Request: {request.path} - {exception}")
        return JsonResponse(
            {
                'error': 'Bad Request',
                'detail': str(exception) if str(exception) else 'The request was malformed or invalid.',
                'status_code': 400
            },
            status=400
        )
    return None


def handle_403(request, exception):
    """
    Custom 403 handler for API routes.
    """
    if request.path.startswith('/api/'):
        logger.warning(f"403 Forbidden: {request.path} - {exception}")
        return JsonResponse(
            {
                'error': 'Forbidden',
                'detail': str(exception) if str(exception) else 'You do not have permission to access this resource.',
                'status_code': 403
            },
            status=403
        )
    return None


def handle_500(request):
    """
    Custom 500 handler for API routes.
    """
    if request.path.startswith('/api/'):
        logger.error(f"500 Internal Server Error: {request.path}")
        return JsonResponse(
            {
                'error': 'Internal Server Error',
                'detail': 'An internal server error occurred.',
                'status_code': 500
            },
            status=500
        )
    return None

