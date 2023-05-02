from django.db import models
from django.utils.html import mark_safe

# Create your models here.
class MyModel(models.Model):
    image = models.ImageField(upload_to='images/')
    text = models.TextField()

    def img_preview(self): #new
        return mark_safe('<img src="{}" width="100" height="100" />'.format(self.image.url))
    img_preview.short_description = 'img_preview'
    img_preview.allow_tags = True
    
    def activate_button(self):
        return format_html('<a href="{}" class="link">Activate</a>',
            reverse_lazy("admin:admin_activate_scenario", args=[self.image])
        )

class Image(models.Model):
    file = models.ImageField(upload_to='user_images/')

    def __str__(self):
        return self.image.name

class WebcamImage(models.Model):
    image = models.ImageField(upload_to='webcam_images/')
    created_at = models.DateTimeField(auto_now_add=True)