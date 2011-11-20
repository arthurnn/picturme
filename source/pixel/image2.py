'''
Created on Nov 19, 2011

@author: arthurnn
'''
import os, sys
import Image
import time
import osaic
from math import sqrt
from PIL import Image
from pixel.models import Pixel
from StringIO import StringIO
from collections import namedtuple
from pixel.models import UserTiles

def create_mosaic(source_image):
        tile_size = (50,50)
        
        w = osaic.ImageWrapper(filename=source_image.filename, blob=source_image)
        copy = source_image.copy()
        copy.thumbnail((100,100))
        
        source_grid = tilefy(w,copy.size)
        
        output_size = (len(source_grid[0]) * tile_size[0],
                       len(source_grid) * tile_size[1]) 
        mosaic = Image.new('RGB', output_size)
        
        arr =  top_down(source_grid, mosaic, tile_size)
            
        return (mosaic,arr)

def top_down(grid, output, tile_size):
    '''
    Starts matching from top-left, going to bottom-right
    '''
    
    #user_image = UserImage()
    
    #cursor = Pixel.objects.all()
    image_list = ImageList(gen())
    users = []
    
    
    _tile_list = dict()
    
    
    counter = 0
    for yPos, y in enumerate(grid):
        for xPos, x in enumerate(grid[yPos]):
            #print counter, 
            rgb = grid[yPos][xPos].color
            #tile = image_list.search(rgb).image.blob
            tile_wrapper = image_list.search(rgb)
            tile_pixel = tile_wrapper.pixel
            
            
            #print tile_pixel.id
            tile = tile_wrapper.image
            
            tile.thumbnail(tile_size) 
            xy = (xPos * tile_size[0], yPos * tile_size[1])
            #print tile
            output.paste(tile, xy)
            counter += 1
            
            #users.append(UserTiles(x=xy[0],y=xy[1],pixel=tile_pixel))
            
            _tile_list.setdefault((tile_pixel.id), list()).append((xy[0],xy[1]))
            
            #tile.close()
            #print counter
    return _tile_list;

import random
def gen():
    
    size = 200
    mm = Pixel.objects.count()-size
    if max > 10:
        index = random.randint(0,mm)
    else:
        index = 0
    
    cursor = Pixel.objects.all()[index:size]
    
    for photo in cursor:
        yield photo
        #tile = Image.open(StringIO(photo.image1.file.read())) 
        #yield tile
        

def tilefy(img, tiles):
    matrix = [[None for i in xrange(tiles[0])] for j in xrange(tiles[1])]
    (width, height) = img.size
    (tile_width, tile_height) = (width // tiles[0], height // tiles[1])
    (x, y) = (0, 0)
    for (i, y) in enumerate(xrange(0, tile_height * tiles[1], tile_height)):
        for (j, x) in enumerate(xrange(0, tile_width * tiles[0], tile_width)):
            rect = (x, y, x + tile_width, y + tile_height)
            tile = img.crop(rect)
            matrix[i][j] = osaic.ImageTuple(img.filename, osaic.average_color(tile), None)
    return matrix

def average_color(img):
    """Return the average color of the given image.
    
    The calculus of the average color has been implemented by looking at
    each pixel of the image and accumulate each rgb component inside
    separate counters.
    
    """
    (width, height) = img.size
    (n, r, g, b) = (0, 0, 0, 0)
    maxcolors = width*height
    colors = img.getcolors(maxcolors)
    
    for (many, color) in colors:
        try:
            (cr,cg,cb) = (color[0],color[1],color[2])
        except TypeError:
            (cr,cg,cb) = (color,color,color)        

        n += many
        r += many * cr
        g += many * cg
        b += many * cb
    return (r // n, g // n, b // n)

class ImageTrans():
    def main(self, img):
        return create_mosaic(img)
    

"""Object passed between different functions."""
ImageTuple = namedtuple('ImageTuple', 'color pixel image'.split())


class ImageList(osaic.ImageList):

    def __init__(self, iterable=None):
        self._img_list = dict()

        for pixel in iterable:
            #pil_img.convert('RGB')
            
            #img = osaic.ImageWrapper(filename=pil_img.filename,blob=pil_img)

            #color = osaic.average_color(img)
            color = (pixel.r,pixel.g,pixel.b)

            image = Image.open(StringIO(pixel.image1.file.read())) 

            self._insert(ImageTuple(color, pixel, image))
    
    @property
    def list(self):
        return self._img_list
    
    def __len__(self):
        """Get the length of the list of images."""
        return len(self._img_list)

    def _insert(self, image):
        """Insert a new image in the list.
        
        Objects enqueued in the list are dictionaries containing the
        minimal amount of meta-data required to handle images, namely the
        name of the image, its average color (we cache the value), and
        a blob object representing the raw processed image. Note that
        after the application of the ``postfunc`` filter, it is possible
        for the blob object to be None.

        """
        # create two levels of hierarchy by first indexing group of
        # images having the same quantized average color.
        #qcolor = quantize_color(image.color)
        pixel = image.pixel
        
        qcolor = (pixel.qr,pixel.qg,pixel.qb)
        
        self._img_list.setdefault(qcolor, list()).append(image)
                    
    def search(self, color):
        """Search the most similar image in terms of average color."""
        # first find the group of images having the same quantized
        # average color.
        qcolor = osaic.quantize_color(color)
        best_img_list = None
        best_dist = None
        for (img_list_color, img_list) in self._img_list.iteritems():
            dist = osaic.squaredistance(qcolor, img_list_color)
            if dist==0:
                best_img_list = img_list
                break
            if best_dist is None or dist < best_dist:
                best_dist = dist
                best_img_list = img_list
        # now spot which of the images in the list is equal to the
        # target one.
        best_img = None
        best_dist = None
        for img_wrapper in best_img_list:
            dist = osaic.squaredistance(color, img_wrapper.color)
            if best_dist is None or dist < best_dist:
                best_dist = dist
                best_img = img_wrapper
        
        # finally return the best match.
        return best_img
