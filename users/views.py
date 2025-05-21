
import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import *
from .models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from datetime import datetime
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import logging

logger = logging.getLogger(__name__)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
# from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from django.utils.timezone import now
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import re

# User = get_user_model()


class ForgotPasswordAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="Send password reset email",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email'],
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL)
            }
        ),
        responses={
            200: openapi.Response(description="Password reset link sent"),
            400: openapi.Response(description="Email is required"),
            404: openapi.Response(description="User not found"),
        }
    )
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'success': False, 'message': 'Email is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'success': False, 'message': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        # Generate token
        tokens = user.get_jwt_token()
        # print ("=======================",tokens.access)
        access_token = tokens['access']

        # Password reset URL
        reset_url = f"https://yourfrontend.com/reset-password?token={access_token}"

        try:
            send_mail(
                subject="Password Reset Request",
                message=f"Click the link to reset your password:\n{reset_url}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )
            return Response({'success': True, 'message': 'Password reset link sent to your email.'}, status=status.HTTP_200_OK)
        except Exception:
            return Response({'success': False, 'message': 'Failed to send email.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ResetPasswordAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="Reset password using JWT token",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['token', 'new_password'],
            properties={
                'token': openapi.Schema(type=openapi.TYPE_STRING),
                'new_password': openapi.Schema(type=openapi.TYPE_STRING, format='password')
            }
        ),
        responses={
            200: openapi.Response(description="Password updated successfully"),
            400: openapi.Response(description="Invalid request or weak password"),
            401: openapi.Response(description="Token expired"),
        }
    )
    def post(self, request):
        token = request.data.get('token')
        new_password = request.data.get('new_password')

        if not token or not new_password:
            return Response({'success': False, 'message': 'Token and new password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        if len(new_password) < 8 or not re.search(r'\d', new_password) or not re.search(r'[A-Z]', new_password):
            return Response({
                'success': False,
                'message': 'Password must be at least 8 characters long and contain one uppercase letter and one digit.'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            access_token = AccessToken(token)
            user_id = access_token['user_id']
            user = User.objects.get(id=user_id)

            if access_token['exp'] < int(now().timestamp()):
                return Response({'success': False, 'message': 'Token has expired.'}, status=status.HTTP_401_UNAUTHORIZED)

            user.set_password(new_password)
            user.save()

            return Response({'success': True, 'message': 'Password updated successfully.'}, status=status.HTTP_200_OK)

        except Exception:
            return Response({'success': False, 'message': 'Invalid or expired token.'}, status=status.HTTP_400_BAD_REQUEST)

def send_otp_email(email, otp):
    subject = 'Complete Your Visuwalls Account Creation'
    message = f'''Dear User,

We received a request to create your account on Visuwalls.

Your One-Time Password (OTP) is: {otp}

Please use this OTP to complete your account creation process. If you did not request an OTP for account creation, please ignore this message.

Thank you,
The Visuwalls Team
'''
    from_email = 'your@example.com'
    to_email = [email]

    send_mail(subject, message, from_email, to_email)

class LoginView(APIView):
    @swagger_auto_schema(
        operation_description="Obtain JWT tokens by logging in with email and password",
        request_body=LoginSerializer,
        responses={
            200: openapi.Response(
                description="Login successful",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'success': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                        'message': openapi.Schema(type=openapi.TYPE_STRING),
                        'data': openapi.Schema(type=openapi.TYPE_OBJECT)
                    }
                )
            ),
            400: openapi.Response(description="Invalid credentials"),
        },
        tags=['Auth']
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {'success': False, 'message': 'Login failed', 'data': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        data = serializer.validated_data
        user = data.pop('user')
        user_data = UserProfileSerializernew(user).data
        payload = {
            'access': data.get('access'),
            'refresh': data.get('refresh'),
            'user': user_data
        }
        return Response(
            {'success': True, 'message': 'Login successful', 'data': payload},
            status=status.HTTP_200_OK
        )

class RegisterUserView(APIView):
    @swagger_auto_schema(
        operation_description="Register a new user with email and optional profile",
        request_body=RegisterUserSerializer,
        responses={
            201: openapi.Response(
                description="User successfully registered",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'success': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                        'message': openapi.Schema(type=openapi.TYPE_STRING),
                        'data': openapi.Schema(type=openapi.TYPE_OBJECT),
                        'email_sent': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                    }
                )
            ),
            400: openapi.Response(description="Validation errors"),
        },
        tags=['Auth']
    )
    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            logger.warning("Registration validation failed: %s", serializer.errors)
            return Response(
                {"success": False, "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = serializer.save()
        user_data = serializer.data

        # Send welcome email (optional)
        email_sent = False
        try:
            
            email_sent = True
        except Exception as e:
            logger.error("Welcome email failed for %s: %s", user.email, e)

        return Response(
            {
                "success": True,
                "message": "User registered successfully",
                "data": user_data,
                "email_sent": email_sent,
            },
            status=status.HTTP_201_CREATED
        )

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from users.models import User


class VerifyOTPView(APIView):

    @swagger_auto_schema(
        operation_description="Verify OTP and mark the user's email as verified.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'otp': openapi.Schema(type=openapi.TYPE_STRING, description='The OTP to verify')
            }
        ),
        responses={
            200: openapi.Response(
                description="OTP verified successfully and email verified.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'success': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Indicates whether the OTP was successfully verified'),
                        'message': openapi.Schema(type=openapi.TYPE_STRING, description='Success message')
                    }
                )
            ),
            400: openapi.Response(
                description="Invalid OTP or other errors.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, description='Error message')
                    }
                )
            )
        },tags=['Auth']
    )
    def post(self, request):
        otp = request.data.get('otp')

        print("Received OTP:", otp)  # OTP passed in request body

        if not otp:
            return Response({'detail': 'OTP is required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if OTP exists for any user
        user = User.objects.filter(otp=otp).first()
        print("user",user)

        if user:
            # OTP matched with a user, mark the user's email as verified
            user.is_email_verified = True
            user.save()

            return Response({
                'success': True,
                'message': 'OTP verified successfully and email verified.'
            }, status=status.HTTP_200_OK)
        
        return Response({'detail': 'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)




from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from users.serializers import UserProfileSerializer

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get logged-in user's profile using JWT.",
        responses={
            200: openapi.Response(
                description="Profile data retrieved successfully.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'success': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                        'message': openapi.Schema(type=openapi.TYPE_STRING),
                        'data': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'id': openapi.Schema(type=openapi.TYPE_STRING),
                                'email': openapi.Schema(type=openapi.TYPE_STRING),
                                'username': openapi.Schema(type=openapi.TYPE_STRING),
                                'user_type': openapi.Schema(type=openapi.TYPE_STRING),
                                'profile_pic': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI),
                                'about_yourself': openapi.Schema(type=openapi.TYPE_STRING),
                                'address': openapi.Schema(type=openapi.TYPE_STRING),
                                'mobile': openapi.Schema(type=openapi.TYPE_STRING),
                                'is_email_verified': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                            }
                        )
                    }
                )
            ),
            401: openapi.Response(description="Unauthorized")
        },
        tags=['User']
    )
    def get(self, request):
        user = request.user
        serializer = UserProfileSerializernew(user)
        return Response({
            "success": True,
            "message": "User profile fetched successfully",
            "data": serializer.data
        })
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from users.serializers import UserProfileUpdateSerializer


class UserProfileUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(
        operation_description="Update user profile (including profile image).",
        manual_parameters=[
            openapi.Parameter('username', openapi.IN_FORM, type=openapi.TYPE_STRING),
            openapi.Parameter('about_yourself', openapi.IN_FORM, type=openapi.TYPE_STRING),
            openapi.Parameter('address', openapi.IN_FORM, type=openapi.TYPE_STRING),
            openapi.Parameter('mobile', openapi.IN_FORM, type=openapi.TYPE_STRING),
            openapi.Parameter('profile_pic', openapi.IN_FORM, type=openapi.TYPE_FILE),
        ],
        responses={
            200: openapi.Response(
                description="Profile updated successfully.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'success': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                        'message': openapi.Schema(type=openapi.TYPE_STRING),
                        'data': openapi.Schema(type=openapi.TYPE_OBJECT),
                    }
                )
            ),
            400: openapi.Response(description="Validation error")
        },
        tags=["User"]
    )
    def put(self, request):
        user = request.user
        serializer = UserProfileUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "Profile updated successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            "success": False,
            "message": "Profile update failed",
            "data": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
import random
import string
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.hashers import make_password
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from users.models import User

from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.hashers import make_password
import random
import string
from users.models import User


class ForgetPasswordViewApp(APIView):
    parser_classes = [FormParser, MultiPartParser, JSONParser]

    @swagger_auto_schema(
        operation_description="Send new password to user's email if email exists.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email'],
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description="User's email"),
            }
        ),
        responses={
            200: openapi.Response(
                description="Password reset successfully.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'success': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                        'message': openapi.Schema(type=openapi.TYPE_STRING),
                    }
                )
            ),
            400: openapi.Response(
                description="Invalid email or sending failed.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'success': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                        'message': openapi.Schema(type=openapi.TYPE_STRING),
                    }
                )
            ),
            500: openapi.Response(
                description="Error sending email.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'success': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                        'message': openapi.Schema(type=openapi.TYPE_STRING),
                    }
                )
            ),
        },
        tags=['Auth']
    )
    def post(self, request):
        email = request.data.get('email')

        if not email:
            return Response({
                "success": False,
                "message": "Email is required."
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)

            # Generate random 8-character password
            new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
            user.password = make_password(new_password)
            user.save()

            # Send password to user's email
            send_mail(
                subject='Your New Password',
                message=f'Your new password is: {new_password}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )

            return Response({
                "success": True,
                "message": "New password sent to your email."
            }, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({
                "success": False,
                "message": "User with this email does not exist."
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                "success": False,
                "message": f"Error sending email: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import random
from users.models import User  # adjust this import based on your app structure


class ResendOTPView(APIView):

    @swagger_auto_schema(
        operation_description="Resend a new OTP to the user's email.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email'],
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description="User's email"),
            }
        ),
        responses={
            200: openapi.Response(
                description="OTP resent successfully.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'success': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                        'message': openapi.Schema(type=openapi.TYPE_STRING),
                    }
                )
            ),
            400: openapi.Response(
                description="User not found or email is missing.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'success': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                        'message': openapi.Schema(type=openapi.TYPE_STRING),
                    }
                )
            ),
        },
        tags=["Auth"]
    )
    def post(self, request):
        email = request.data.get('email')

        if not email:
            return Response({
                "success": False,
                "message": "Email is required."
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)

            # Generate and save new OTP
            otp = str(random.randint(1000, 9999))
            user.otp = otp
            user.save()

            # Send OTP email
            subject = 'Complete Your Auto Qira Account Creation'
            message = f'''Dear User,

We received a request to create your account on Auto Qira.

Your One-Time Password (OTP) is: {otp}

Please use this OTP to complete your account creation process. If you did not request an OTP for account creation, please ignore this message.

Thank you,
The Auto Qira Team
'''
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

            return Response({
                "success": True,
                "message": "OTP has been resent to your email."
            }, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({
                "success": False,
                "message": "User with this email does not exist."
            }, status=status.HTTP_400_BAD_REQUEST)
