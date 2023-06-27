from django.db import models

# Create your models here.


class BroadwayData(models.Model):
    shows_names = models.TextField(null=True,blank=True)
    shows_links = models.TextField(null=True,blank=True)

class Image(models.Model):
    user_image_file = models.ImageField(upload_to='user_images/')

    def __str__(self):
        return self.image.name