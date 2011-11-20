'''
Created on Nov 19, 2011

@author: arthurnn
'''
#TODO: fix black artifacts
#TODO: optimize find_closest_match (better color matching)
#TODO: look into fractional ratios
#TODO: new repeat; allow repeats when out of images 
#TODO: new repeat; allow repeats at a specified distance

import os, sys
import Image
import time
import osaic
from math import sqrt
from PIL import Image
from pixel.models import Pixel,Photo
from StringIO import StringIO

def create_mosaic(source_image):
        tile_size = (50,50)
        #subdivide source image into tiles 
        #subdivision_size = (tile_size[0] / size_ratio, tile_size[1] / size_ratio)
        
        #source_grid = subdivide_source(source_image, subdivision_size)
        w = osaic.ImageWrapper(filename=source_image.filename, blob=source_image)
        #source_grid = osaic.tilefy(w,100)
        copy = source_image.copy()
        copy.thumbnail((100,100))
        
        source_grid = tilefy(w,copy.size)
        
        output_size = (len(source_grid[0]) * tile_size[0],
                       len(source_grid) * tile_size[1]) 
        mosaic = Image.new('RGB', output_size)
        
        top_down(source_grid, mosaic, tile_size)
            
        return mosaic

def top_down(grid, output, tile_size):
    '''
    Starts matching from top-left, going to bottom-right
    '''
    
    #cursor = Pixel.objects.all()
    image_list = ImageList(gen())
    
    counter = 0
    for yPos, y in enumerate(grid):
        for xPos, x in enumerate(grid[yPos]):
            #print counter, 
            #tile = find_closest_match(grid[yPos][xPos],cursor)
            
            #rgb = average_color(grid[yPos][xPos])
            rgb = grid[yPos][xPos].color
            tile = image_list.search(rgb).image.blob
            
            tile.thumbnail(tile_size) 
            xy = (xPos * tile_size[0], yPos * tile_size[1])
            #print tile
            output.paste(tile, xy)
            counter += 1
            #print counter

def gen():
    cursor = Photo.objects.all()[:300]
    
    for photo in cursor:
        tile = Image.open(StringIO(photo.image1.file.read())) 
        yield tile
        

def find_closest_match(image,cursor):
    '''
    Find the closest match of image from the image pool.
    Returns an Image instance. 
    '''
    #subdivide image into tiles again
    subs = subdivide_tile(image)
    target_rgb = []
    diff_rgb = []
    diff_id = []
    total_diff_for_tile = 0
    #get average RGB vector from the 9 subdivisions of the tile
    for sub in subs:
        target_rgb.append(average_rgb(sub))

    #(r,g,b)=average_rgb(image)
    #rr = r+g+b
    #if rr==0: rr = 1
    #x = (float(r)/rr)*100
    #y = (float(r)/rr)*100
    
    
    #qq = cursor.filter(x=x,y=y)
    #if qq.count() > 0:
    #    c = qq
    #else:
    c = cursor
    
    for row in c:
        pos = row.pos
        diff = difference((row.r, row.g, row.b), (target_rgb[pos]))
        total_diff_for_tile += diff
        if pos == 8:
            diff_rgb.append(total_diff_for_tile)
            diff_id.append(row.id)
#            if threshold and total_diff_for_tile < threshold:
#                diff_rgb = [total_diff_for_tile, ]
#                diff_id = [row[1], ]
            total_diff_for_tile = 0

    #find the imagepool tile with the least difference between source tile
    #print diff_rgb
    closest_rgb = min(diff_rgb)
    closest_id = diff_id[diff_rgb.index(closest_rgb)]
    
    pixel = cursor.get(pk=closest_id)
    
    
    closest_tile = Image.open(StringIO(pixel.photo.image1.file.read()))
    return closest_tile
    
    
#    subs = subdivide_tile(image)
#    target_rgb = []
#
#    #get average RGB vector from the 9 subdivisions of the tile
##    for sub in subs:
##        (r,g,b) = average_rgb(sub)
##        o_id = r
##        o_id = (o_id<<8)+g
##        o_id = (o_id<<8)+b
##        target_rgb.append(o_id)
##
##    qq = Pixel.objects.filter(pk__in=target_rgb)
#    
#    rgb = (r,g,b) = average_rgb(image)
#    #tile = None
#    o_id = r
#    o_id = (o_id<<8)+g
#    o_id = (o_id<<8)+b
#    
#    try:
#        pixel = Pixel.objects.get(pk=o_id)
#    except Pixel.DoesNotExist:
#        pixel1 = Pixel.objects.filter(pk__lt=o_id)[0]
#        pixel2 = Pixel.objects.filter(pk__gt=o_id)[0]
#        
#        if (o_id - pixel1.id) < (pixel2.id - o_id):
#            pixel = pixel1
#        else:
#            pixel = pixel2
#        
#        
#        
#    if pixel:
#        tile = Image.open(StringIO(pixel.image1.file.read()))
#    else:
#        tile = Image.new(image.mode,(100,100),rgb)
#    
##    if qq.count() <= 0:
##        tile = Image.new(image.mode,(100,100),target_rgb[0])
##    else:
##        tile = Image.open(StringIO(qq[0].image1.file.read()))
##        tile.thumbnail((100,100))
#        
#    return tile
    
    
def difference(rgb1, rgb2):
    '''
    Returns the 3-tuple difference between rgb1 and rgb 2
    '''
    diff = sqrt((rgb1[0] - rgb2[0]) ** 2 + (rgb1[1] - rgb2[1]) ** 2 + 
    (rgb1[2] - rgb2[2]) ** 2)
    return diff

def subdivide_source(image, tile_size):
    '''
    Subdivides a large image into smaller tiles of size tile_size.
    Returns a 2-dimensional list of Image tiles. 
    '''
    width = image.size[0] / tile_size[0]
    height = image.size[1] / tile_size[1]
    grid = [[None for w in range(width)] for h in range(height)]
    for y in range(height):
        for x in range(width):
            cell = image.crop((x * tile_size[0], 
                               y * tile_size[1],
                               x * tile_size[0] + tile_size[0], 
                               y * tile_size[1] + tile_size[1]))
            grid[y][x] = cell       
    return grid

def subdivide_tile(image):
    '''
    Subdivide tile image into 3x3 sub tile.
    Used for subsampling.
    Returns a 3x3 grid of Image tiles.
    '''
    w = image.size[0] / 3
    h = image.size[1] / 3
    subdivisions = [] 

    for y in range(3):
        for x in range(3):
            cropped = image.crop((x * w, y * h, x * w + w, y * h + h))
            subdivisions.append(cropped)
    return subdivisions

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

#def average_rgb(image):
#    '''
#    Calculates the average RGB of an image.
#    Returns 3-tuple (R, G, B)
#    '''
#    average_red = 0
#    average_green = 0
#    average_blue = 0
#    maxcolors = image.size[0]*image.size[1]
#    colors = image.getcolors(maxcolors)
#    for color in colors:
#        average_red += color[1][0] * color[0]
#        average_green += color[1][1] * color[0]
#        average_blue += color[1][2] * color[0]
#    average_red /= maxcolors
#    average_green /= maxcolors
#    average_blue /= maxcolors
#    return (average_red, average_green, average_blue)

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

def output_grid(grid, size, tile_size):
    output = Image.new('RGB', size)
    print tile_size
    for yPos, y in enumerate(grid):
        for xPos, x in enumerate(grid[yPos]):
            output.paste(x, (xPos * tile_size[0] / 2, yPos * tile_size[1] / 2))

    output_image(output, 'grid.jpg')

def output_image(image, filename):
    try:
        image.save(os.path.join(os.getcwd(), filename))
    except IOError:
        print 'Cannot save image ', filename

class ImageTrans():
    def main(self, img,ratio):
        return create_mosaic(img)
    
    
class ImageList(osaic.ImageList):

    def __init__(self, iterable=None):
        self._img_list = dict()

        for pil_img in iterable:
            pil_img.convert('RGB')
            
            img = osaic.ImageWrapper(filename=pil_img.filename,blob=pil_img)

            #color = osaic.average_color(img)
            color = average_color(pil_img)

            self._insert(osaic.ImageTuple(pil_img.filename, color, img))
            
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
