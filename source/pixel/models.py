from django.db import models
from PIL import Image
from StringIO import StringIO
from django.core.files.storage import FileSystemStorage

class Pixel(models.Model):
    image1 = models.ImageField(storage=FileSystemStorage(),upload_to='tiles/image1',null=False,blank=False)
    url = models.URLField(null=True,blank=True)
    
    r = models.PositiveIntegerField()
    g = models.PositiveIntegerField()
    b = models.PositiveIntegerField()
    
    qr = models.PositiveIntegerField()
    qg = models.PositiveIntegerField()
    qb = models.PositiveIntegerField()

    _image = None
    
    @property
    def color(self):
        #return (self.r,self.g,self.b) 
        return (self.qr,self.qg,self.qb) 
    
    @property
    def qcolor(self):
        return (self.qr,self.qg,self.qb) 
    
    @property
    def image(self):
        if self._image is None:
            self._image = Image.open(StringIO(self.image1.file.read()))
            
        return self._image        
        
    
class UserImage(models.Model):
    pixels = models.ManyToManyField(Pixel, through='UserTiles')
    
    image = models.ImageField(upload_to='user_images',null=False,blank=False)
    thumbnail = models.ImageField(upload_to='user_images/thumbnail',null=False,blank=False)
    
    
class UserTiles(models.Model):
    user_image = models.ForeignKey(UserImage)
    pixel = models.ForeignKey(Pixel)
    
    #x = models.PositiveIntegerField()
    #y = models.PositiveIntegerField()
