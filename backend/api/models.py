from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Photo(models.Model):

    src = models.CharField(max_length=256)
    name = models.CharField(max_length=100)
    date = models.DateTimeField(null=True, blank=True)
    is_liked = models.BooleanField(default=False)

    def __str__(self):
        return f'<Photo: {self.name} on {self.date.strftime("%Y-%m-%d")}>'
    
    class Meta:
        ordering = ['-date']


class Project(models.Model):

    name = models.CharField(max_length=30)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    date_created = models.DateTimeField(verbose_name='date created', auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-date_created']