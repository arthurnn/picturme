'''
Created on Nov 19, 2011

@author: arthurnn
'''
import os, sys
import Image
import time
import random
from math import sqrt
from PIL import Image
from pixel.models import Pixel
from StringIO import StringIO
from collections import namedtuple
from pixel.models import UserTiles
from django.core.cache import cache
import operator

from kdtree import KDTree

def create_mosaic(source_image):
        tile_size = (50,50)
        
        copy = source_image.copy()
        copy.thumbnail((100,100))
        
        source_grid = tilefy(source_image,copy.size)
        
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
    
#    size = 500
#    mm = Pixel.objects.count()-size-1
#    if mm > 10:
#        index = random.randint(0,mm)
#    else:
#        index = 0
#    
#    cursor = Pixel.objects.all()[index:index+size]
    
    cursor = Pixel.objects.all()
    
    #image_list = ImageList(gen(cursor))
    
    image_list = KDTree.construct_from_data(list(cursor))

    #nearest = tree.query(query_point=(5,4,3), t=3)
    
    
    _tile_list = dict()
    
    counter = 0
    for yPos, y in enumerate(grid):
        for xPos, x in enumerate(grid[yPos]):
            #print counter, 
            rgb = grid[yPos][xPos].color
            
            qrgb = quantize_color(rgb)
            
            #tile = image_list.search(rgb).image.blob
            #tile_wrapper = image_list.search(rgb)
            
            w = image_list.query(query_point=qrgb, t=1)
            
            #i = random.randint(0,len(w)-1)
            
            tile_pixel = w[0]
            
            #tile_pixel = tile_wrapper.pixel
            #print tile_pixel.id
            #tile = tile_wrapper.image
            #tile = Image.open(StringIO(tile_pixel.image1.file.read())) 
            tile = tile_pixel.image
            
            
            tile.thumbnail(tile_size) 
            xy = (xPos * tile_size[0], yPos * tile_size[1])
            #print tile
            output.paste(tile, xy)
            counter += 1
            
            _tile_list.setdefault((tile_pixel.id), list()).append((xy[0],xy[1]))
            
            #print counter
    return _tile_list;

def gen(cursor):
    for photo in cursor:
        yield photo
        #tile = Image.open(StringIO(photo.image1.file.read())) 
        #yield tile
        
""" These methods are a variation of the osaic python api!  """
def tilefy(img, tiles):
    matrix = [[None for i in xrange(tiles[0])] for j in xrange(tiles[1])]
    (width, height) = img.size
    (tile_width, tile_height) = (width // tiles[0], height // tiles[1])
    (x, y) = (0, 0)
    for (i, y) in enumerate(xrange(0, tile_height * tiles[1], tile_height)):
        for (j, x) in enumerate(xrange(0, tile_width * tiles[0], tile_width)):
            rect = (x, y, x + tile_width, y + tile_height)
            tile = img.crop(rect)
            matrix[i][j] = ImageTuple(average_color(tile), None, None)
    return matrix

def average_color(img):
    """  Return the average color of the given image.  """
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

def quantize_color(color):
    levels = 8 
    mode = 'middle'
    
    if mode == 'top':
        inc = 256 // levels - 1
    elif mode == 'middle':
        inc = 256 // levels // 2
    else: # 'bottom'
        inc = 0

    # first map each component from the range [0, 256[ to [0, levels[:
    #       v * levels // 256
    # then remap values to the range of default values [0, 256[, but
    # this time instead of obtaining all the possible values, we get
    # only discrete values:
    #       .. * 256 // levels
    # finally, depending on the specified mode, grab the bottom, middle
    # or top value of the result range:
    #       .. + inc
    ret = [(v * levels) // 256 * (256 // levels) + inc for v in color]
    return tuple(ret)

def difference(vec1, vec2):
    """Return difference between given vectors."""
    return map(operator.sub, vec1, vec2)

def squaredistance(vec1, vec2):
    """Return the square distance between given vectors."""
    return sum(v ** 2 for v in difference(vec1, vec2))

class ImageTrans():
    def main(self, img):
        return create_mosaic(img)
    

"""Object passed between different functions."""
ImageTuple = namedtuple('ImageTuple', 'color pixel image'.split())


class ImageList():

    def __init__(self, iterable=None):
        self._img_list = dict()

        for pixel in iterable:
            #pil_img.convert('RGB')
            

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
        """ Insert a new image in the list. """
        # create two levels of hierarchy by first indexing group of
        # images having the same quantized average color.
        #qcolor = quantize_color(image.color)
        pixel = image.pixel
        
        qcolor = (pixel.qr,pixel.qg,pixel.qb)
        
        self._img_list.setdefault(qcolor, list()).append(image)
                    
    def search(self, color):
        qcolor = quantize_color(color)
        
#        pixel_id = cache.get('%d%d%d' % qcolor)
#        if pixel_id is not None:
#            pixel = Pixel.objects.get(pk=pixel_id)
#            image = Image.open(StringIO(pixel.image1.file.read())) 
#            return ImageTuple(color, pixel, image)
        
        best_img_list = None
        best_dist = None
        for (img_list_color, img_list) in self._img_list.iteritems():
            dist = squaredistance(qcolor, img_list_color)
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
            dist = squaredistance(color, img_wrapper.color)
            if best_dist is None or dist < best_dist:
                best_dist = dist
                best_img = img_wrapper
        
        
#        cache.set('%d%d%d' % qcolor, best_img.pixel.id)
        # finally return the best match.
        return best_img
