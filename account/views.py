from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from account.serializers import UserRegistrationSerializer, UaerLoginSerializer, UserProfileSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from account.renderers import UserRenderer
from rest_framework.permissions import IsAuthenticated
from account.models import UserRefreshToken, User
from rest_framework_simplejwt.views import TokenRefreshView as BaseTokenRefreshView
from django.utils import timezone
from datetime import timedelta
from rest_framework_simplejwt.exceptions import InvalidToken


class UserTokenRefreshView(BaseTokenRefreshView):
    renderer_classes = [UserRenderer]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        print("11111")
        try:
            serializer.is_valid(raise_exception=True)
            refresh_token = serializer.validated_data['refresh']
            token = RefreshToken(refresh_token)
            UserRefreshToken.objects.filter(
                token=refresh_token,
                is_active=True).update(
                is_active=False)

            # Rotate refresh token and generate new access token
            new_refresh = str(token)
            new_access = str(token.access_token)

            # Save the new refresh token in the database
            user_id = token["user_id"]
            user = User.objects.get(id=user_id)
            UserRefreshToken.objects.create(
                user=user, token=new_refresh, is_active=True)

            response = Response({
                'access': new_access,
                'refresh': new_refresh,
            }, status=status.HTTP_200_OK)

            # Set the new refresh token and access token in the response
            # cookies
            response.set_cookie(
                'access_token',
                str(new_access),
                httponly=True,
                max_age=900,
                samesite='Strict')  # 15 minutes
            response.set_cookie(
                'refresh_token',
                str(new_refresh),
                httponly=True,
                max_age=86400,
                samesite='Strict')  # 1 day

            return response

        except Exception as e:
            return Response({'msg': f'Error refreshing token: {str(e)}'},
                            status=status.HTTP_400_BAD_REQUEST)


# Generate Token
def get_tokens_for_user(user):
    # Generate a new refresh token
    refresh = RefreshToken.for_user(user)

    # Invalidate the previous refresh tokens (set is_active to False)
    old_tokens = UserRefreshToken.objects.filter(user=user, is_active=True)
    old_tokens.update(is_active=False)  # Invalidate all old tokens

    # Create a new refresh token entry
    UserRefreshToken.objects.create(
        user=user,
        token=str(refresh),
        expires_at=timezone.now() + timedelta(days=1),  # Expiry date (e.g., 1 day)
        is_active=True
    )

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, fomat=None):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({'msg': 'registration successful'},
                        status=status.HTTP_201_CREATED)


class UserLoginView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, fomat=None):
        serializer = UaerLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        password = serializer.data.get('password')
        user = authenticate(email=email, password=password)
        if user:
            # Generate JWT
            tokens = get_tokens_for_user(user)
            response = Response(
                {'token': tokens, 'msg': 'Login successful'}, status=status.HTTP_200_OK)
            response.set_cookie(
                key='access_token',
                value=tokens['access'],
                httponly=True,
                # secure=True,  # Use HTTPS in production
                samesite='Strict',
                max_age=900  # 15 minutes for access token
            )
            response.set_cookie(
                key='refresh_token',
                value=tokens['refresh'],
                httponly=True,
                # secure=True,
                samesite='Strict',
                max_age=86400  # 1 day for refresh token
            )
            return response
        return Response(
            {
                'errors': {
                    'non_field_errors': 'Email or Password is incorrect'}},
            status=status.HTTP_404_NOT_FOUND)


class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserLogoutView(APIView):
    def post(self, request, format=None):
        # Get the refresh token from the cookies
        refresh_token = request.COOKIES.get('refresh_token')

        if refresh_token:
            try:
                # Get the associated refresh token record from the database
                refresh_token_obj = UserRefreshToken.objects.get(
                    token=refresh_token)

                # Mark the refresh token as inactive (revoked)
                refresh_token_obj.is_active = False
                refresh_token_obj.save()

            except UserRefreshToken.DoesNotExist:
                return Response({'msg': 'Refresh token not found'},
                                status=status.HTTP_400_BAD_REQUEST)

        # Clear the cookies for access_token and refresh_token
        response = Response(
            {'msg': 'Logged out successfully'}, status=status.HTTP_200_OK)
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')

        return response
