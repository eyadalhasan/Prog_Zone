from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    birthday = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)  # Remove blank=True
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name='custom_users_groups',  # Unique related_name
        related_query_name='user',
    )
    street=models.CharField(max_length=30,blank=True,null=True)
    country=models.CharField(max_length=30,blank=True,null=True)
    city=models.CharField(max_length=30,blank=True,null=True)
    phone_number=models.IntegerField(blank=True,null=True)

    # Provide a unique related_name for the user_permissions field
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='custom_users_permissions',  # Unique related_name
        related_query_name='user',
    )
    def save(self, *args, **kwargs):
        if not self.pk:  # Check if the instance is being created
            # Perform your actions for newly created instances here
            self.is_active = True  # Set is_active to True for new instances

        super().save(*args, **kwargs)  # Call the save method of the superclass




