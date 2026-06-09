import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'learnhub.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

email = 'admin@example.com'
password = 'admin'

user, created = User.objects.get_or_create(email=email, defaults={'username': 'admin'})
user.set_password(password)
user.is_staff = True
user.is_superuser = True
user.save()

if created:
    print(f"Created new superuser: {email} / {password}")
else:
    print(f"Reset password for existing user: {email} / {password}")
