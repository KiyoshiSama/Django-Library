from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=225)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-id"] 

    def __str__(self):
        return self.name
