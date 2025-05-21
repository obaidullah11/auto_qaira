from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
import uuid
from rest_framework_simplejwt.tokens import RefreshToken

# Custom field for generating a unique 6-character ID
class CustomUserIDField(models.CharField):
    def pre_save(self, model_instance, add):
        if add and not getattr(model_instance, self.attname):
            return uuid.uuid4().hex[:6].upper()
        return super().pre_save(model_instance, add)


class MyUserManager(BaseUserManager):
    def create_user(self, email, username=None, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        
        email = self.normalize_email(email)
        username = username or email.split('@')[0]

        if self.model.objects.filter(email=email).exists():
            raise ValueError(f"The email '{email}' is already in use.")

        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username=None, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_approved', True)
        extra_fields.setdefault('user_type', 'superadmin')

        return self.create_user(email, username, password, **extra_fields)


class User(AbstractUser):
    USER_TYPES = (
        ('customer', 'Customer'),
        ('business', 'Business Owner'),
        ('superadmin', 'Super Admin'),
    )

    id = CustomUserIDField(primary_key=True, max_length=6, editable=False)
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)
    email = models.EmailField(unique=True)

    # gender = models.CharField(max_length=20, blank=True, null=True)/
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='customer')

    # phone = models.CharField(max_length=20, blank=True, null=True)
    profile_pic = models.ImageField(upload_to='profiles/', blank=True, null=True)
    device_token = models.CharField(max_length=255, blank=True, null=True)
    otp = models.CharField(max_length=6, blank=True, null=True)
    about_yourself = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    mobile = models.CharField(max_length=20, blank=True, null=True)

    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    is_superuser = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    is_mute = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    

    def get_jwt_token(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
