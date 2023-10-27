from django.db import models
from django.contrib.auth import get_user_model

user = get_user_model()
# Create your models here.
class User(models.Model):
    User = models.OneToOneField(user, on_delete=models.CASCADE)
    # profile_picture = models.ImageField() --> ini buat profpic, perlu ga ya
    isAdmin = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    
    def is_admin(self):
        return self.isAdmin