from django.db import models
from django.contrib import auth

# Create your models here.

# PremissionMixin is for model *only got User model// PermissionRequiredMixin is for views.
class User(auth.models.User,auth.models.PermissionsMixin):

    def __str__(self):
        return "@{}".format(self.username)
