from django.db import models
from django.contrib.auth.models import User


class Collective(models.Model):
    name = models.SlugField(max_length=100)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    is_visible = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    creator = models.ForeignKey(User, null=True, blank=True, default=None, on_delete=models.CASCADE)
    edited = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return '{}:{}'.format(self.name, self.title)
