from django.db import models
# Create your models here.
from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
    name = models.CharField(max_length=50)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)


