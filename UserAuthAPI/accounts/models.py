from __future__ import unicode_literals
from django.db import models


from authemail.models import EmailUserManager, EmailAbstractUser


class MyUser(EmailAbstractUser):
    # Custom fields
    date_of_birth = models.DateField('Date of birth', null=True,
        blank=True)

    # Required
    objects = EmailUserManager()

# Create your models here.
