from django.db import models
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class AccountModel(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, related_name='account')
    full_name = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'


class ConfirmationCodesModel(models.Model):
    code = models.CharField(max_length=6)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='sent_codes')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}: {self.code}'

    class Meta:
        verbose_name = 'Confirmation Code'
        verbose_name_plural = 'Confirmation Codes'
        constraints = [
            models.UniqueConstraint(fields=['code', 'user'], name='unique_code_per_user')
        ]
