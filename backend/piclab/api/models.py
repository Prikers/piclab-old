from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Project(models.Model):

    name = models.CharField(max_length=30)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    date_created = models.DateTimeField(verbose_name='date created', auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-date_created']


class Photo(models.Model):

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='photos')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='photos')
    name = models.CharField(max_length=50)
    date_created = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    is_liked = models.BooleanField(default=False)

    def __str__(self):
        return f'<Photo: {self.name} on {self.date_created.strftime("%Y-%m-%d")}>'
    
    class Meta:
        ordering = ['-date_created']
