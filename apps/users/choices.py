from django.db.models import TextChoices


class UserRoleChoice(TextChoices):

    admin = 'admin'
    driver = 'driver'
