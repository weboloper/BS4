from hepsiburada import *
from tables import *

import urllib.parse as urlparse
from urllib.parse import urlencode


#url = input("url")
url = "https://www.hepsiburada.com/dekorasyon-c-18021300"

url_parts = list(urlparse.urlparse(url))
name = url_parts[2][1:]

results = scrapHepsiburada(url, 30)
writeExcel(results, name)
