from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.template import RequestContext
from django.db import connection
from django.utils.translation import ugettext as _
from annoying.decorators import render_to
from django.core.files.base import ContentFile
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from StringIO import StringIO
import urllib,hashlib
from PIL import Image

from pixel.image2 import ImageTrans

from pixel.models import UserImage,UserTiles

import hashlib

@render_to('index.html')
def home(request):
    ids = [1,4,8,15,19]
    ii = UserImage.objects.filter(id__in=ids)
    return {'images':ii}
    

def upload(request):
    
    ff = request.FILES.get('file',False)
    if ff:
        imgFile = Image.open(StringIO(ff.read()))
        
        ap = ImageTrans()
        
        #imgFile.thumbnail((500,500))
        (mosaic,arr) = ap.main(imgFile)
        
        photo = UserImage()
        sio = StringIO()
        mosaic.save(sio,'JPEG')
        
        fn_image = hashlib.md5(sio.getvalue()).hexdigest()+'.jpg'
        photo.image.save(fn_image, ContentFile(sio.getvalue()), save=False)
        
        
        m_copy = mosaic.copy()
        m_copy.thumbnail((500,500))
        sio = StringIO()
        m_copy.save(sio,'JPEG')
        
        fn_image = hashlib.md5(sio.getvalue()).hexdigest()+'.jpg'
        photo.thumbnail.save(fn_image, ContentFile(sio.getvalue()), save=False)
        
        photo.save()
        
        
        for (pixel_id, xy_list) in arr.iteritems():
            tt = UserTiles(user_image=photo)
            tt.pixel_id = pixel_id
            tt.save()
            
        
#        for a in arr:
#            a.user_image=photo
#            a.save()
        
    return redirect('/detail/%s'%photo.id)


@render_to('details.html')
def detail(request, image_id):
    u = get_object_or_404(UserImage,pk=image_id)
    return {'pixel':u}
    

@render_to('details_thumbnails.html')
def thumbList(request, image_id):
    u = get_object_or_404(UserImage, pk=image_id)
    q = u.usertiles_set.all()
    
    
    paginator = Paginator(q, 6) # Show 13 per page
    try:
        list_pag = paginator.page(request.GET.get('page', 1))
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        list_pag = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        list_pag = paginator.page(paginator.num_pages)      
        
    return {'pag':list_pag}

