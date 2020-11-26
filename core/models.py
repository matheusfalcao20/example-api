from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings
from django.utils import timezone


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError(_('Users must have an email'))

        user = self.model(
            email=email,
            name=name,
            # username=username,
            # birthday=birthday
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password):
        user = self.create_user(
            email,
            name,
            # username,
            password=password,
        )

        user.is_admin = True
        user.save(using=self._db)

        return user

class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=50, blank=False)
    username = models.CharField(max_length=50, blank=True, null=True, unique=True)
    register_date = models.DateTimeField(auto_now_add=True)
    forgot_password_hash = models.CharField(max_length=255, null=True, blank=True)
    forgot_password_expire = models.DateTimeField(null=True, blank=True)
    allow_notification = models.BooleanField(default=True)
    allow_commercial_email = models.BooleanField(default=True)
    profile_image = models.ImageField(upload_to='profile_image/', null=True, blank=True)
    token_notification = models.CharField(max_length=255, null=True, blank=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', ]

    # def image_tag(self):
    #     return mark_safe('<img src="%s" height="200" />' % (self.profile_image.url))

    # image_tag.cf.name)

    def get_short_name(self):
        return self.name

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    @classmethod
    def change_password(cls, email, forgot_password_hash, new_password):
        try:
            user = cls.objects.get(email=email, forgot_password_hash=forgot_password_hash)
        except cls.DoesNotExist: 
            raise ForgotPasswordInvalidParams

        now = timezone.now()

        if user.forgot_password_expire < now:
            raise ForgotPasswordExpired

        user.set_password(new_password)
        user.forgot_password_expire = now
        user.save()
