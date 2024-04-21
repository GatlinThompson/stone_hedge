from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

# Create your models here.


class Log(models.Model):
    approved = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_logs', null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    approved_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='approved_logs', null=True, blank=True)
    name = models.CharField(max_length=30)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    time = models.PositiveIntegerField(validators=[MinValueValidator(1)], blank=True, null=True)
