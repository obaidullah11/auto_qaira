from rest_framework import views, status, permissions
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from .models import Reel, ReelComment
from .serializers import ReelSerializer, ReelCommentSerializer

def api_response(success=True, message="", data=None, status_code=200):
    return Response({
        "success": success,
        "message": message,
        "data": data
    }, status=status_code)

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class ReelUploadView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(
        operation_description="Upload a new Reel",
        request_body=ReelSerializer,
        responses={201: ReelSerializer, 400: 'Bad Request'}
    )
    def post(self, request):
        data = request.data.copy()
        data['user'] = request.user.id
        serializer = ReelSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return api_response(True, "Reel uploaded", serializer.data, status.HTTP_201_CREATED)
        return api_response(False, "Upload failed", serializer.errors, status.HTTP_400_BAD_REQUEST)

class ReelListView(views.APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_description="Get all reels",
        responses={200: ReelSerializer(many=True)}
    )
    def get(self, request):
        reels = Reel.objects.all().order_by('-created_at')
        serializer = ReelSerializer(reels, many=True)
        return api_response(True, "All reels", serializer.data)

class UserReelListView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get reels uploaded by authenticated user",
        responses={200: ReelSerializer(many=True)}
    )
    def get(self, request):
        reels = Reel.objects.filter(user=request.user)
        serializer = ReelSerializer(reels, many=True)
        return api_response(True, "Your reels", serializer.data)
from rest_framework.exceptions import PermissionDenied

class ReelDetailView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk, user):
        reel = get_object_or_404(Reel, pk=pk)
        if reel.user != user:
            raise PermissionDenied("You do not have permission to modify this reel.")
        return reel

    @swagger_auto_schema(
        operation_description="Get reel details by ID",
        responses={200: ReelSerializer, 404: 'Not Found'}
    )
    def get(self, request, pk):
        reel = get_object_or_404(Reel, pk=pk)
        serializer = ReelSerializer(reel)
        return api_response(True, "Reel details", serializer.data)

    @swagger_auto_schema(
        operation_description="Update reel by ID",
        request_body=ReelSerializer,
        responses={200: ReelSerializer, 400: 'Bad Request', 404: 'Not Found'}
    )
    def put(self, request, pk):
        reel = self.get_object(pk, request.user)
        serializer = ReelSerializer(reel, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return api_response(True, "Reel updated", serializer.data)
        return api_response(False, "Update failed", serializer.errors, status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete reel by ID",
        responses={204: 'No Content', 404: 'Not Found'}
    )
    def delete(self, request, pk):
        reel = self.get_object(pk, request.user)
        reel.delete()
        return api_response(True, "Reel deleted", None, status.HTTP_204_NO_CONTENT)







@swagger_auto_schema(
    method='post',
    operation_description="Like or unlike a reel",
    responses={200: openapi.Response('Like status', schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'success': openapi.Schema(type=openapi.TYPE_BOOLEAN),
            'message': openapi.Schema(type=openapi.TYPE_STRING),
            'data': openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                'likes': openapi.Schema(type=openapi.TYPE_INTEGER)
            }),
        }
    ))},
)
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def like_unlike_reel(request, reel_id):
    reel = get_object_or_404(Reel, pk=reel_id)
    if request.user in reel.likes.all():
        reel.likes.remove(request.user)
        message = "Reel unliked"
    else:
        reel.likes.add(request.user)
        message = "Reel liked"
    return api_response(True, message, {"likes": reel.total_likes()})

@swagger_auto_schema(
    method='post',
    operation_description="Add comment to a reel",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['comment'],
        properties={
            'comment': openapi.Schema(type=openapi.TYPE_STRING, description='Comment text'),
        },
    ),
    responses={201: ReelCommentSerializer, 400: 'Bad Request'},
)
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def add_comment(request, reel_id):
    reel = get_object_or_404(Reel, pk=reel_id)
    comment_text = request.data.get('comment')
    if not comment_text:
        return api_response(False, "Comment text is required", status_code=400)
    comment = ReelComment.objects.create(reel=reel, user=request.user, comment=comment_text)
    serializer = ReelCommentSerializer(comment)
    return api_response(True, "Comment added", serializer.data, status_code=201)
