"""
Custom exception handler for Django REST Framework.
Provides consistent JSON error responses.
"""
import logging
from rest_framework.views import exception_handler
from rest_framework import status
from rest_framework.response import Response
from django.core.exceptions import ValidationError as DjangoValidationError

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    Custom exception handler that provides consistent JSON error responses.
    """
    # Call DRF's default exception handler first
    response = exception_handler(exc, context)
    
    # If response is None, the exception wasn't handled by DRF
    if response is None:
        # Handle Django ValidationError
        if isinstance(exc, DjangoValidationError):
            logger.warning(f"ValidationError: {exc}")
            return Response(
                {
                    'error': 'Validation Error',
                    'detail': str(exc),
                    'status_code': status.HTTP_400_BAD_REQUEST
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Log unexpected exceptions
        logger.error(
            f"Unhandled exception: {type(exc).__name__}: {exc}",
            exc_info=True,
            extra={'context': context}
        )
        
        # Return generic 500 error for API routes
        request = context.get('request')
        if request and request.path.startswith('/api/'):
            return Response(
                {
                    'error': 'Internal Server Error',
                    'detail': 'An unexpected error occurred.',
                    'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        return None
    
    # Add status_code to response data for consistency
    if isinstance(response.data, dict):
        response.data['status_code'] = response.status_code
        
        # Format validation errors consistently
        if response.status_code == status.HTTP_400_BAD_REQUEST:
            if 'detail' not in response.data:
                response.data['error'] = 'Bad Request'
    
    return response
