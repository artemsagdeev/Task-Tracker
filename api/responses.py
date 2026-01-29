from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone

def success_response(*, data=None, message=None, metadata=None, status_code=status.HTTP_200_OK):
    return Response(
        {
            'success': True,
            'data': data or {},
            'message': message,
            'metadata': metadata or {},
        },
        status=status_code,
    )

def error_response(*, code, message=None, details=None, status_code):
    return Response(
        {
            'success': False,
            'error': {
                'code': code,
                'message': message,
                'details': details or {},
            },
            'timestamp': timezone.now().isoformat()
        },
        status=status_code,
    )

