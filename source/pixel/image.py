'''
Created on Nov 19, 2011

@author: arthurnn
'''



def find_closest_match(image):
    '''
    Find the closest match of image from the image pool.
    Returns an Image instance. 
    '''
    cursor = db.cursor()
    #subdivide image into tiles again
    subs = subdivide_tile(image)
    target_rgb = []
    diff_rgb = []
    diff_id = []
    total_diff_for_tile = 0
    #get average RGB vector from the 9 subdivisions of the tile
    for sub in subs:
        target_rgb.append(average_rgb(sub))

    #get all usable tile images from imagepool database
    if repeat:
        cursor.execute(
            '''SELECT id, image_id, red, green, blue, pos
            FROM Colors'''
        )
    else:
        cursor.execute(
            '''SELECT C.id, C.image_id, C.red, C.green, C.blue, C.pos
            FROM Colors C, Images I 
            WHERE C.image_id=I.id 
            AND used=0'''
        )
    #compare each sub-tile of subs to each average color in Colors table
    #calculate the difference
    #then get the total difference between the source tile and the
    #imagepool tile
    for row in cursor:
        pos = row[5]
        diff = difference((row[2], row[3], row[4]), (target_rgb[pos]))
        total_diff_for_tile += diff
        if pos == 8:
            diff_rgb.append(total_diff_for_tile)
            diff_id.append(row[1])
            if threshold and total_diff_for_tile < threshold:
                diff_rgb = [total_diff_for_tile, ]
                diff_id = [row[1], ]
            total_diff_for_tile = 0

    #find the imagepool tile with the least difference between source tile
    #print diff_rgb
    closest_rgb = min(diff_rgb)
    closest_id = diff_id[diff_rgb.index(closest_rgb)]
    if not repeat:
        cursor.execute(
            '''UPDATE Images SET used=1 WHERE id=?''', (closest_id, )
        )
        db.commit()
    cursor.execute(
        '''SELECT image FROM Images WHERE id=?''', (closest_id, )
    )
    closest_tile = cursor.fetchone()[0]
    if verbose:
        print closest_tile, closest_rgb
    return closest_tile

def top_down(grid, output, tile_size, pool_dir, db, repeat, threshold, verbose):
    '''
    Starts matching from top-left, going to bottom-right
    '''
    counter = 0
    for yPos, y in enumerate(grid):
        for xPos, x in enumerate(grid[yPos]):
            if verbose:
                print counter, 
            tile_name = find_closest_match(grid[yPos][xPos], 
                                           db, repeat,
                                          threshold, verbose)
            tile = Image.open(os.path.join(pool_dir, tile_name))
            output.paste(tile, (xPos * tile_size[0], yPos * tile_size[1]))
            counter += 1
      

from pixel.models import Pixel
from PIL import Image
from StringIO import StringIO
import os
def main(image):
    count = 0;
    #image.thumbnail((50,50))
    
    output = Image.new(image.mode,(image.size[0]*10,image.size[1]*10))
    
    for y in range(image.size[1]):
        for x in range(image.size[0]):
            rgb = (r,g,b) = image.getpixel((x,y))
            
            arr = []
            
            o_id = r
            o_id = (o_id<<8)+g
            o_id = (o_id<<8)+b
                
            arr.append(o_id)
            for _ in range(5):
                o_id += 1
                arr.append(o_id)
            
            qq = Pixel.objects.filter(pk__in=arr)
            if qq.count() <= 0:
                count+=1
            tile = Image.new(image.mode,(10,10),rgb)
            output.paste(tile, (x * 10, y * 10))
#            else:
#                if qq[0].image1.file:
#                    tile = Image.open(StringIO(qq[0].image1.file.read()))
#                    output.paste(tile, (x * 10, y * 10))
                
    print "not exist: %d" % ((image.size[0]*image.size[1]) - (count))
    output.save(os.path.join(os.getcwd(), 'test.jpg'))
    return output
                
            
    
    
    