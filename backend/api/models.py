from django.db import models


class Photo(models.Model):

    src = models.CharField(max_length=256)
    name = models.CharField(max_length=100)
    date = models.DateTimeField(null=True, blank=True)
    is_liked = models.BooleanField(default=False)

    def __str__(self):
        return f'<Photo: {self.name} on {self.date.strftime("%Y-%m-%d")}>'
