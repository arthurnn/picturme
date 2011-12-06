
from kdtree import KDTree

kd_tree = False

def autodiscover():
    global kd_tree
    
    from pixel.models import Pixel
    
    
    cc = list(Pixel.objects.all())
    kd_tree = KDTree.construct_from_data(cc)
