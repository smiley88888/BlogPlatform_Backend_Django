from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.utils.decorators import method_decorator

def token_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        auth = JWTAuthentication()
        try:
            user_auth_tuple = auth.authenticate(request)
            if user_auth_tuple is None:
                return Response({'error': 'Invalid or missing token'}, status=status.HTTP_401_UNAUTHORIZED)
            request.user = user_auth_tuple[0]
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        return view_func(request, *args, **kwargs)
    return _wrapped_view