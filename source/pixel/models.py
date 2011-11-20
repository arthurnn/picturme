from django.db import models


class Pixel(models.Model):
    image1 = models.ImageField(upload_to='tiles/image1',null=False,blank=False)
    url = models.URLField(null=True,blank=True)
    
    
    r = models.PositiveIntegerField()
    g = models.PositiveIntegerField()
    b = models.PositiveIntegerField()
    
    qr = models.PositiveIntegerField()
    qg = models.PositiveIntegerField()
    qb = models.PositiveIntegerField()
    
    
class UserImage(models.Model):
    pixels = models.ManyToManyField(Pixel, through='UserTiles')
    
    image = models.ImageField(upload_to='user_images',null=False,blank=False)
    thumbnail = models.ImageField(upload_to='user_images/thumbnail',null=False,blank=False)
    
    
class UserTiles(models.Model):
    user_image = models.ForeignKey(UserImage)
    pixel = models.ForeignKey(Pixel)
    
    #x = models.PositiveIntegerField()
    #y = models.PositiveIntegerField()
