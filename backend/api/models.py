from django.db import models


class Photo(models.Model):

    path = models.CharField(max_length=256)
    name = models.CharField(max_length=100)
    date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'<Photo: {self.name}>'
