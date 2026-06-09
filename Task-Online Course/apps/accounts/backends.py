from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()


class EmailBackend(ModelBackend):
    """Allow login with email address instead of username."""

    def authenticate(self, request, username=None, password=None, email=None, **kwargs):
        lookup_email = email or username
        try:
            user = User.objects.get(email__iexact=lookup_email)
        except User.DoesNotExist:
            return None
        except User.MultipleObjectsReturned:
            user = User.objects.filter(email__iexact=lookup_email).order_by('id').first()

        if user and user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
