from django.db import models


class Image(models.Model):

    path = models.CharField(max_length=256)
    name = models.CharField(max_length=100)
    date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'<Image: {self.name}>'
