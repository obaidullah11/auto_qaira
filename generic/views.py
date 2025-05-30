from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework import status
from .models import SitePolicy
from .serializers import SitePolicySerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class PrivacyPolicyView(APIView):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['content'],
            properties={
                'content': openapi.Schema(type=openapi.TYPE_STRING, description='Privacy policy content'),
            },
        ),
        responses={200: openapi.Response(description="Success")},
        tags=['Privacy Policy']
    )
    def post(self, request):
        content = request.data.get('content')
        policy, created = SitePolicy.objects.update_or_create(
            title="Privacy Policy",
            defaults={'content': content}
        )
        return Response({
            'success': True,
            'message': 'Privacy policy updated',
            'data': SitePolicySerializer(policy).data
        })


class PrivacyPolicyRetrieveView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        responses={200: openapi.Response(description="Success")},
        tags=['Privacy Policy Retrieval']
    )
    def get(self, request):
        try:
            policy = SitePolicy.objects.get(title="Privacy Policy")
            return Response({
                'success': True,
                'message': 'Privacy policy retrieved successfully',
                'data': SitePolicySerializer(policy).data
            })
        except SitePolicy.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Privacy policy not found',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)

















from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework import status
from .models import SitePolicy, Termandpolicy
from .serializers import SiteTermandpolicy
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class TermandpolicyView(APIView):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['content'],
            properties={
                'content': openapi.Schema(type=openapi.TYPE_STRING, description='Terms and Conditions content'),
            },
        ),
        responses={200: openapi.Response(description="Success")},
        tags=['Terms and Conditions']
    )
    def post(self, request):
        content = request.data.get('content')
        policy, created = Termandpolicy.objects.update_or_create(
            title="Terms and Conditions",
            defaults={'content': content}
        )
        return Response({
            'success': True,
            'message': 'Terms and Conditions updated',
            'data': SiteTermandpolicy(policy).data
        })


class TermandpolicyRetrieveView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        responses={200: openapi.Response(description="Success")},
        tags=['Terms and Conditions Retrieval']
    )
    def get(self, request):
        try:
            policy = Termandpolicy.objects.get(title="Terms and Conditions")
            return Response({
                'success': True,
                'message': 'Terms and Conditions retrieved successfully',
                'data': SiteTermandpolicy(policy).data
            })
        except Termandpolicy.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Terms and Conditions not found',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)
