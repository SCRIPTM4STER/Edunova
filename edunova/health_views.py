"""
Health check endpoint for monitoring server uptime.
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.db import connection
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """
    Simple health check endpoint that returns OK status.
    No authentication required.
    """
    return Response({
        'status': 'OK',
        'message': 'Server is running',
    }, status=200)


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check_detailed(request):
    """
    Detailed health check including database and cache status.
    """
    health_status = {
        'status': 'OK',
        'checks': {}
    }
    
    # Database check
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            health_status['checks']['database'] = 'OK'
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        health_status['checks']['database'] = 'FAILED'
        health_status['status'] = 'DEGRADED'
    
    # Cache check
    try:
        cache.set('health_check', 'ok', 10)
        if cache.get('health_check') == 'ok':
            health_status['checks']['cache'] = 'OK'
        else:
            health_status['checks']['cache'] = 'FAILED'
            health_status['status'] = 'DEGRADED'
    except Exception as e:
        logger.error(f"Cache health check failed: {e}")
        health_status['checks']['cache'] = 'FAILED'
        health_status['status'] = 'DEGRADED'
    
    status_code = 200 if health_status['status'] == 'OK' else 503
    return Response(health_status, status=status_code)

