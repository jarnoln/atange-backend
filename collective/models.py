from django.db import models


class Collective(models.Model):
    name = models.SlugField(max_length=100)
    title = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    edited = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return '{}:{}'.format(self.name, self.title)
