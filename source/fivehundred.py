

import urllib

# Find a JSON parser
try:
    import json
    _parse_json = lambda s: json.loads(s)
except ImportError:
    try:
        import simplejson
        _parse_json = lambda s: simplejson.loads(s)
    except ImportError:
        # For Google AppEngine
        from django.utils import simplejson
        _parse_json = lambda s: simplejson.loads(s)
        

class FiveHundredPx:
    BASE_URL = 'https://api.500px.com/v1'
    
    def __init__(self,consumer_key):
        self.consumer_key = consumer_key

    def request(self, path, args=None, post_args=None):
        """Fetches the given path in the Graph API.

        We translate args to a valid query string. If post_args is given,
        we send a POST request to the given path with the given arguments.
        """
        if not args: args = {}
        if self.consumer_key:
            if post_args is not None:
                post_args["consumer_key"] = self.consumer_key
            else:
                args["consumer_key"] = self.consumer_key
        
        post_data = None if post_args is None else urllib.urlencode(post_args)
        
        try:
            
            print 'log path: %s' % (FiveHundredPx.BASE_URL + path + "?" + urllib.urlencode(args))
            file_resp = urllib.urlopen(FiveHundredPx.BASE_URL + path + "?" +
                              urllib.urlencode(args), post_data)
        
            response = _parse_json(file_resp.read())
        finally:
            file_resp.close()
        if response.get("error"):
            pass
            #raise APIError(response["error"], response["status"])
            
        return response

    def get_photos(self,feature='editors'):
        args = {"feature": feature}
        
        data = self.request('/photos', args)
        total_pages = data['total_pages']
        
        page = data['current_page']
        
        while page <= total_pages:
        
            for p in data['photos']:
                yield p
            
            args['page'] = page = page+1
            data = self.request('/photos', args)
        
        
            
            
            