'''
Created on Nov 19, 2011

@author: arthurnn
'''
import datetime
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.models import Count
from django.core.files.base import ContentFile

from StringIO import StringIO
import urllib,hashlib,osaic
from PIL import Image

from fivehundred import FiveHundredPx

from pixel.models import Pixel,Photo


CONSUMER_KEY = 'HedA1jeHKM2KaXWIb1lPV9bIJJu9eIh84h2s613L'

class Command(BaseCommand):
    help = "Cron job to fetch images"
    

    def subdivide(self, image):
        w = image.size[0] / 3
        h = image.size[1] / 3
        subdivisions = [] 
        for y in range(3):
            for x in range(3):
                cropped = image.crop((x * w, y * h, x * w + w, y * h + h))
                subdivisions.append(cropped)
        return subdivisions
    
    def average_rgb(self, image):
        '''
        Calculates the average RGB of an image.
        Returns 3-tuple (R, G, B)
        '''
        average_red = 0
        average_green = 0
        average_blue = 0
        maxcolors = image.size[0]*image.size[1]
        colors = image.getcolors(maxcolors)
        for color in colors:
            try:
                (r,g,b) = (color[1][0],color[1][1],color[1][2])
            except TypeError:
                (r,g,b) = (color[1],color[1],color[1])
            
            average_red += r * color[0]
            average_green += g * color[0]
            average_blue += b * color[0]
        average_red /= maxcolors
        average_green /= maxcolors
        average_blue /= maxcolors
        return (average_red, average_green, average_blue)
    
    def handle(self, *args, **options):
        #t0 = datetime.datetime.now()
        
        api = FiveHundredPx(CONSUMER_KEY)
        
        iiter = api.get_photos(feature = args[0])
        
        
        count = 0
        for p in iiter:
            if count>1000:
                break
            count += 1
            
            
            url = p['image_url']
            fileIm = urllib.urlopen(url)
        
            im = StringIO(fileIm.read())
            img = Image.open(im)
            
            arr = self.subdivide(img)
            #arr.append(img)
            
#            w = osaic.ImageWrapper(filename=img.filename, blob=img)
#            main_rgb = osaic.average_color(w)
#            osaic.quantize_color(main_rgb, levels=2)
            
            photo = Photo()
            
            filename = hashlib.md5(im.getvalue()).hexdigest()+'.jpg'
            photo.image1.save(name=filename, content=ContentFile(im.getvalue()), save=True)
            
            #poszfile = None
            for a in arr:
                (r,g,b) = self.average_rgb(a)
                
                #o_id = r
                #o_id = (o_id<<8)+g
                #o_id = (o_id<<8)+b
                pos = arr.index(a)
                #obj, created = Pixel.objects.get_or_create(r=r,g=g,b=b,pos=pos,x=0,y=0)
                pix = Pixel(r=r,g=g,b=b,pos=pos,x=0,y=0)
                pix.photo = photo
                pix.save()
                
                #if created:
                    #rr = r+g+b
                    #if rr==0: rr = 1
                    
                    #obj.x = (float(r)/rr)*100
                    #obj.y = (float(r)/rr)*100
                    
                    #if pos==0:
                    #filename = hashlib.md5(im.getvalue()).hexdigest()+'.jpg'
                    #obj.image1.save(name=filename, content=ContentFile(im.getvalue()), save=False)
                        #poszfile = obj.image1.file
                    #else:
                        #obj.image1.file = poszfile
                    
                    #obj.save()
                
        
        #self.stdout.write("Popular Looks reloaded, in %s" % delta_t)