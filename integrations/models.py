from django.db import models
from django.contrib.auth.models import User

class Token(models.Model):
    key = models.CharField(max_length=50)
    value = models.CharField(max_length=100)
    creator = models.ForeignKey(User, on_delete=models.PROTECT, related_name='TokenCreator', blank=True, null=True)
    creationTime = models.DateTimeField(null=True, blank=True)
    lastEditor = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='TokenLastEditor', blank=True, null=True)
    lastEditTime = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Tokens"
        verbose_name = "Token"

    def __str__(self):
        return self.key
