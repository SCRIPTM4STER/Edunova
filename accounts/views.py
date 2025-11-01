from datetime import timedelta

from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import (
    MyTokenObtainPairSerializer,
    RegisterSerializer,
    ChangePasswordSerializer,
    GoogleSocialAuthSerializer,
    ProfileSerializer


)


User = get_user_model()


# ------------------------------------------------------
# JWT TOKEN VIEW
# ------------------------------------------------------
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# ------------------------------------------------------
# REGISTER VIEW
# ------------------------------------------------------
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


# ------------------------------------------------------
# GET ALL ROUTES (test)
# ------------------------------------------------------
@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/auth/token/',
        '/auth/register/',
        '/auth/token/refresh/',
        '/auth/change-password/',
        '/auth/reauth/',
        '/auth/google/',
    ]
    return Response(routes)


# ------------------------------------------------------
# TEST ENDPOINT
# ------------------------------------------------------
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def testEndPoint(request):
    if request.method == 'GET':
        data = f"Congratulation {request.user.username}, your API just responded to GET request"
        return Response({'response': data}, status=status.HTTP_200_OK)

    if request.method == 'POST':
        text = "Hello buddy"
        data = f"Congratulation your API just responded to POST request with text: {text}"
        return Response({'response': data}, status=status.HTTP_200_OK)

    return Response({}, status=status.HTTP_400_BAD_REQUEST)


# ------------------------------------------------------
# CHANGE PASSWORD VIEW
# ------------------------------------------------------
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not request.session.get('reauth_verified'):
            return Response(
                {'detail': 'Please re-authenticate before changing password.'},
                status=403
            )

        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            # Clear reauth session after password change
            request.session.pop('reauth_verified', None)
            return Response({'detail': 'Password changed successfully.'}, status=200)

        return Response(serializer.errors, status=400)


# ------------------------------------------------------
# GOOGLE LOGIN VIEW
# ------------------------------------------------------
class GoogleAuthView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = GoogleSocialAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'email': user.email,
                'username': user.username
            }
        })


# ------------------------------------------------------
# PROFILE VIEW
# ------------------------------------------------------
class ProfileView(generics.RetrieveAPIView):
    """
    Get the profile of the currently authenticated user.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_object(self):
        return self.request.user.profile
