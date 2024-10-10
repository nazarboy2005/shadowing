from django.db import models
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class AccountModel(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, related_name='account')
    full_name = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', default='default/img.png')
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'


class ConfirmationCodesModel(models.Model):
    code = models.CharField(max_length=6)
    email = models.EmailField(default='helloworld@gmail.com')  # Track by email
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.email}: {self.code}'

    class Meta:
        verbose_name = 'Confirmation Code'
        verbose_name_plural = 'Confirmation Codes'
        constraints = [
            models.UniqueConstraint(fields=['code', 'email'], name='unique_code_per_email')
        ]

