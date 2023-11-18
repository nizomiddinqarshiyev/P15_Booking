from django.db import models


class Role(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class UserRole(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    role = models.ForeignKey('accounts.Role', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
