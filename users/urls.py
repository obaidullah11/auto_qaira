from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from users.views import *
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
# from . views import *
# user_profile_update = UserProfileViewSet.as_view({'patch': 'update_profile'})
urlpatterns = [
   
    # path("ChangeUserTypeView/", ChangeUserTypeView.as_view(), name="UserProfileView"),
    # path('check-email/', CheckEmailView.as_view(), name='check_email'),
    path('register/', RegisterUserView.as_view(), name='register-user'),
    # path('upload-doc/', FileUploadnView.as_view(), name='upload-doc'),
    # path('validate-token/', ValidateJWTView.as_view(), name='validate-token'),
    # path('check-Phonenumber/', CheckPhoneNumberView.as_view(), name='check_email'),
    path("login/", LoginView.as_view(), name="phone_login"),
    path("getuserprofile/", UserProfileView.as_view(), name="UserProfileView"),
    path('resend-otp/', ResendOTPView.as_view(), name='resend-otp'),
    # path('password_reset/', ResetPasswordAPIView.as_view(), name='password_reset'),
    # path('social-sign-in/', SocialLoginOrRegisterView.as_view(), name='social-sign-in'),
    # path('users/update-profile/', user_profile_update, name='update-profile'),
    # path('send-email/', SendEmailView.as_view(), name='send_email'),
    # path("register-send-otp/", newSendOTPView.as_view(), name="send_otp"),
    # path("send-otp/", SendOTPView.as_view(), name="send_otp"),
    path("verify-otp/", VerifyOTPView.as_view(), name="verify_otp"),
    path('profile_update/', UserProfileUpdateView.as_view(), name='user-profile-update'),
    # path('register_student/', register_student, name='register_student'),
    # path('register_teacher/', register_teacher, name='register_student'),
    # path('teachers/', TeacherListAPIView.as_view(), name='teacher-list'),
    # path('Students/', StudentListAPIView.as_view(), name='teacher-list'),
    # path('forgot-password/', ForgotPasswordAPIView.as_view(), name='forgot-password'),
    path('forgot-password/', ForgetPasswordViewApp.as_view(), name='forgot-password'),
    path('reset-password/', ResetPasswordAPIView.as_view(), name='reset-password'),
    
    # path('forgitpassword/', VerifyOTPResetPasswordAPIView.as_view(), name='verify-otp-reset-password'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# {
# "email": "jane.doe1@example.com",
# "password": "S3cur3P@ssw0rd",
# "user_type": "teacher"
# }

# {
#   "email": "jane.doe1@example.com",
#   "password": "S3cur3P@ssw0rd"
# }


# {
#     "email": "student@example.com",
#     "first_name": "John",
#     "last_name": "Doe"
    
# }
