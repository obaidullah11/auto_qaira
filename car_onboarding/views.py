from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.generics import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import CarListing, UploadedFile
from .serializers import CarListingSerializer, UploadedFileSerializer

# Utility response function
def api_response(success=True, message="", data=None, status_code=200):
    return Response({
        "success": success,
        "message": message,
        "data": data
    }, status=status_code)

# Schema for car listing creation
manual_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=["title", "brand", "model", "year", "registration_number"],
    properties={
        'title': openapi.Schema(type=openapi.TYPE_STRING),
        'brand': openapi.Schema(type=openapi.TYPE_STRING),
        'model': openapi.Schema(type=openapi.TYPE_STRING),
        'year': openapi.Schema(type=openapi.TYPE_INTEGER),
        'transmission': openapi.Schema(type=openapi.TYPE_STRING),
        'fuel_type': openapi.Schema(type=openapi.TYPE_STRING),
        'engine_capacity': openapi.Schema(type=openapi.TYPE_STRING),
        'color': openapi.Schema(type=openapi.TYPE_STRING),
        'registration_number': openapi.Schema(type=openapi.TYPE_STRING),
        'mileage': openapi.Schema(type=openapi.TYPE_INTEGER),
        'seating_capacity': openapi.Schema(type=openapi.TYPE_INTEGER),
        'car_type': openapi.Schema(type=openapi.TYPE_STRING),
        'location': openapi.Schema(type=openapi.TYPE_STRING),
        'pickup_location': openapi.Schema(type=openapi.TYPE_STRING),
        'available_from': openapi.Schema(type=openapi.FORMAT_DATE),
        'available_until': openapi.Schema(type=openapi.FORMAT_DATE),
        'availability_type': openapi.Schema(type=openapi.TYPE_STRING),
        'delivery_available': openapi.Schema(type=openapi.TYPE_BOOLEAN),
        'price_per_day': openapi.Schema(type=openapi.TYPE_INTEGER),
        'price_per_week': openapi.Schema(type=openapi.TYPE_INTEGER),
        'price_per_month': openapi.Schema(type=openapi.TYPE_INTEGER),
        'security_deposit': openapi.Schema(type=openapi.TYPE_INTEGER),
        'minimum_rent_days': openapi.Schema(type=openapi.TYPE_INTEGER),
        'air_conditioning': openapi.Schema(type=openapi.TYPE_BOOLEAN),
        'gps': openapi.Schema(type=openapi.TYPE_BOOLEAN),
        'bluetooth': openapi.Schema(type=openapi.TYPE_BOOLEAN),
        'usb_charging': openapi.Schema(type=openapi.TYPE_BOOLEAN),
        'child_seat': openapi.Schema(type=openapi.TYPE_BOOLEAN),
        'fuel_policy': openapi.Schema(type=openapi.TYPE_STRING),
        'additional_notes': openapi.Schema(type=openapi.TYPE_STRING),
        'driver_allowed': openapi.Schema(type=openapi.TYPE_BOOLEAN),
        'with_driver_only': openapi.Schema(type=openapi.TYPE_BOOLEAN),
        'driver_charges_per_day': openapi.Schema(type=openapi.TYPE_INTEGER),
        'max_km_per_day': openapi.Schema(type=openapi.TYPE_INTEGER),
        'extra_km_charge': openapi.Schema(type=openapi.TYPE_INTEGER),
        'cancellation_policy': openapi.Schema(type=openapi.TYPE_STRING),
        'images': openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Items(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI),
            description='List of image URLs or metadata'
        ),
    }
)

# -----------------------------
# Car Listing Create
# -----------------------------
class CarListingCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[],
        request_body=manual_schema,
        operation_summary="Create Car Listing",
        operation_description="Add a new car listing. Images should be a JSON array of URLs or metadata.",
        responses={201: openapi.Response('Created', CarListingSerializer), 400: 'Bad Request'},
        tags=['Car Management']
    )
    def post(self, request):
        data = request.data.copy()
        data['user'] = request.user.id
        serializer = CarListingSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            car = serializer.save()
            return api_response(True, "Car listing created successfully.", CarListingSerializer(car).data, status.HTTP_201_CREATED)
        return api_response(False, "Validation failed.", serializer.errors, status.HTTP_400_BAD_REQUEST)

# -----------------------------
# File Upload
# -----------------------------
class FileUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(
        operation_summary="Upload a file",
        operation_description="Uploads a file and returns its public URL.",
        manual_parameters=[
            openapi.Parameter('file', in_=openapi.IN_FORM, type=openapi.TYPE_FILE, required=True, description='File to upload')
        ],
        responses={
            201: openapi.Response(
                description="Success",
                examples={
                    "application/json": {
                        "success": True,
                        "message": "File uploaded successfully.",
                        "data": {"file_url": "http://127.0.0.1:8000/media/uploads/yourfile.jpg"}
                    }
                }
            )
        },
         tags=['Image Management']
    )
    def post(self, request, format=None):
        serializer = UploadedFileSerializer(data=request.data)
        if serializer.is_valid():
            uploaded_file = serializer.save()
            file_url = request.build_absolute_uri(uploaded_file.file.url)
            return api_response(True, "File uploaded successfully.", {"file_url": file_url}, status.HTTP_201_CREATED)
        return api_response(False, "Invalid file upload.", serializer.errors, status.HTTP_400_BAD_REQUEST)

# -----------------------------
# List All Car Listings (Public)
# -----------------------------
class CarListingList(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description="List of all car listings",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'success': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                        'message': openapi.Schema(type=openapi.TYPE_STRING),
                        'data': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_OBJECT))
                    }
                )
            )
        }, tags=['Car Management']
    )
    def get(self, request):
        cars = CarListing.objects.all()
        serializer = CarListingSerializer(cars, many=True)
        return api_response(True, "All car listings retrieved", serializer.data)

# -----------------------------
# List User's Car Listings
# -----------------------------
class UserCarListing(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description="List of car listings for the authenticated user",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'success': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                        'message': openapi.Schema(type=openapi.TYPE_STRING),
                        'data': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_OBJECT))
                    }
                )
            )
        }, tags=['Car Management']
    )
    def get(self, request):
        cars = CarListing.objects.filter(user=request.user)
        serializer = CarListingSerializer(cars, many=True)
        return api_response(True, "Your car listings retrieved", serializer.data)

# -----------------------------
# Car Listing Detail / Update / Delete
# -----------------------------
class CarListingDetail(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description="Car retrieved",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'success': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                        'message': openapi.Schema(type=openapi.TYPE_STRING),
                        'data': openapi.Schema(type=openapi.TYPE_OBJECT),
                    }
                )
            )
        }, tags=['Car Management']
    )
    def get(self, request, pk):
        car = get_object_or_404(CarListing, pk=pk, user=request.user)
        serializer = CarListingSerializer(car)
        return api_response(True, "Car retrieved", serializer.data)

    @swagger_auto_schema(
        request_body=CarListingSerializer,
        responses={
            200: openapi.Response(
                description="Car updated",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'success': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                        'message': openapi.Schema(type=openapi.TYPE_STRING),
                        'data': openapi.Schema(type=openapi.TYPE_OBJECT),
                    }
                )
            )
        }, tags=['Car Management']
    )
    def put(self, request, pk):
        car = get_object_or_404(CarListing, pk=pk, user=request.user)
        serializer = CarListingSerializer(car, data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return api_response(True, "Car updated", serializer.data)
        return api_response(False, "Validation error", serializer.errors, status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        responses={204: openapi.Response(description="Car deleted")}, tags=['Car Management']
    )
    def delete(self, request, pk):
        car = get_object_or_404(CarListing, pk=pk, user=request.user)
        car.delete()
        return api_response(True, "Car deleted successfully", None, status.HTTP_204_NO_CONTENT)
