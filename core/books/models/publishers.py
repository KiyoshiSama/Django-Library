from django.db import models


class Publisher(models.Model):
    name = models.CharField(max_length=225)
    address = models.CharField(max_length=400)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
