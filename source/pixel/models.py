from django.db import models


class Pixel(models.Model):
    image1 = models.ImageField(upload_to='tiles/image1',null=False,blank=False)
    #image2 = models.ImageField(upload_to='tiles/image2',null=False,blank=False)
    #image3 = models.ImageField(upload_to='tiles/image3',null=False,blank=False)
    
    r = models.PositiveIntegerField()
    g = models.PositiveIntegerField()
    b = models.PositiveIntegerField()
    
    
    x = models.PositiveIntegerField()
    y = models.PositiveIntegerField()
    
    pos = models.PositiveIntegerField(default=0)
    
    
class UserImage(models.Model):
    pixels = models.ManyToManyField(Pixel)
    
    
    image = models.ImageField(upload_to='user_images',null=False,blank=False)