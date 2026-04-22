#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DjangoProject777.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()

from django.contrib.auth import get_user_model
from calculator.models import Profile # Check the app name

User = get_user_model()

# Finds all users who do NOT have a linked Profile object
users_without_profile = User.objects.filter(profile__isnull=True)

print(f"Found {users_without_profile.count()} user(s) missing a Profile.")

for user in users_without_profile:
    # Create the Profile instance and link it to the User
    Profile.objects.create(user=user)
    print(f"Profile created for user: {user.username}")
