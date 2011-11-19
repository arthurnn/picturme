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
from math import sqrt
from PIL import Image
from pixel.models import Pixel
from StringIO import StringIO

def create_mosaic(source_image, output, ratio):
        '''
        source = source image; must be 4:3 or 3:4 ratio
        output = output filename
        image_pool_dir = directory of the tile image pool; 
                            must have imagepool.db inside
        ratio = ratio between output and source;
                e.g. ratio of 2 means output will be 2 times bigger than source
                the higher the ratio, the more detailed the output
        repeat = if tiles can be repeated or not
        threshold = threshold to use for acceptable difference between colors
        '''
        size_ratio = ratio
        tile_size = (100,100)
        #subdivide source image into tiles 
        subdivision_size = (tile_size[0] / size_ratio, tile_size[1] / size_ratio)
        
        source_grid = subdivide_source(source_image, subdivision_size)
        output_size = (len(source_grid[0]) * tile_size[0],
                       len(source_grid) * tile_size[1]) 
        mosaic = Image.new('RGB', output_size)
        
        #width = source_image.size[0] / (tile_size[0] / size_ratio)
        #height = source_image.size[1] / (tile_size[1] / size_ratio)
        #print '%d x %d = %d' % (width, height, width * height)

        #Loop through tile_grid, then compare each tile from source_image with every 
        #tile in imagepool. Find the closest match, then place that tile in place.
        #try:
        top_down(source_grid, mosaic, tile_size)
        #except KeyboardInterrupt:
            #print 'Cancelled by user. '
            #return
        #else:
            #output_image(mosaic, output)
            #print 'Success! Generated %s' % (output)
            
        return mosaic

def top_down(grid, output, tile_size):
    '''
    Starts matching from top-left, going to bottom-right
    '''
    
    cursor = Pixel.objects.all()
    
    counter = 0
    for yPos, y in enumerate(grid):
        for xPos, x in enumerate(grid[yPos]):
            #print counter, 
            tile = find_closest_match(grid[yPos][xPos],cursor)
             
            xy = (xPos * tile_size[0], yPos * tile_size[1])
            #print tile
            output.paste(tile, xy)
            counter += 1



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
    
    
    closest_tile = Image.open(StringIO(pixel.image1.file.read()))
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

def average_rgb(image):
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
        average_red += color[1][0] * color[0]
        average_green += color[1][1] * color[0]
        average_blue += color[1][2] * color[0]
    average_red /= maxcolors
    average_green /= maxcolors
    average_blue /= maxcolors
    return (average_red, average_green, average_blue)


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
        return create_mosaic(img, 'test.jpg', ratio)
