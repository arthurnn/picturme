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

from StringIO import StringIO
import urllib,hashlib
from PIL import Image

from pixel.image2 import *

from pixel.models import UserImage

import hashlib

def upload(request):
    
    ff = request.FILES.get('file',False)
    if ff:
        imgFile = Image.open(StringIO(ff.read()))
        
        mosaic = main(imgFile)
        
        photo = UserImage()
        fn_image = hashlib.md5(mosaic.getvalue()).hexdigest()+'.jpg'
        photo.image.save(fn_image, ContentFile(mosaic.getvalue()), save=False)
        photo.save()
        
    return redirect('/detail/%s'%photo.id)


@render_to('details.html')
def detail(request, id):
    u = get_object_or_404(UserImage,pk=id)
    return {'image':u.image}
    
    
