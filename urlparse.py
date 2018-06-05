import urllib.parse as urlparse
from urllib.parse import urlencode


def paginateUrl(url, page):
    
    params = {'sayfa': page }

    url_parts = list(urlparse.urlparse(url))
    query = dict(urlparse.parse_qsl(url_parts[4]))
    query.update(params)

    url_parts[4] = urlencode(query)

    return(urlparse.urlunparse(url_parts))

#örnek çağırma
#getpage = paginateUrl(url, page = 2)
