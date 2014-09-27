import sys
import json
import base64
import re
import urllib
import urllib2
import xbmcaddon
import xbmcplugin
import xbmc
__addon__ = xbmcaddon.Addon(str(sys.argv[0]))
__proxy__ = __addon__.getSetting("url_proxy")
__quality__ = __addon__.getSetting("quality")
__addsearch__ = __addon__.getSetting("addsearch")

PAYLOAD = json.loads(base64.b64decode(sys.argv[1]))

def search(query):
    if __quality__ == "0":
        __best__ = '/search/%s/0/99/200'
    elif __quality__ == "1":
        __best__ = '/search/%s 1080p/0/99/200'
    elif __quality__ == "2":
        __best__ = '/search/%s 720p/0/99/200'
    elif __quality__ == "3":
        __best__ = '/search/%s 480p/0/99/200'

    pre1 = __proxy__
    pre2 = __best__
    pre3 = urllib.quote_plus(query)
    req = pre1 + pre2
    response = urllib2.urlopen((req % pre3). replace(" ", "%20"))
    data = response.read()
    if response.headers.get("Content-Encoding", "") == "gzip":
        import zlib
        data = zlib.decompressobj(16 + zlib.MAX_WBITS).decompress(data)
    return [{"uri": magnet} for magnet in re.findall(r'magnet:\?[^\'"\s<>\[\]]+', data)]

def search_episode(imdb_id, tvdb_id, name, season, episode):
    if __quality__ == "0":
        __best__ = '/search/%s/0/99/200'
    elif __quality__ == "1":
        __best__ = '/search/%s 1080p/0/99/200'
    elif __quality__ == "2":
        __best__ = '/search/%s 720p/0/99/200'
    elif __quality__ == "3":
        __best__ = '/search/%s 480p/0/99/200'

    pre1 = __proxy__
    pre2 = __best__
    pre3 = urllib.quote_plus
    req = pre1 + pre2
    response = urllib2.urlopen((req % pre3). replace(" ", "%20"))
    # xbmc.log('EP_Search: %s' % req, xbmc.LOGDEBUG)
    data = response.read()
    if response.headers.get("Content-Encoding", "") == "gzip":
        import zlib
        data = zlib.decompressobj(16 + zlib.MAX_WBITS).decompress(data)
    return search("%s S%02dE%02d" % (name, season, episode))


def search_movie(imdb_id, name, year):
    if __quality__ == "0":
        __best__ = '/0/99/200'
    elif __quality__ == "1":
        __best__ = ' 1080p/0/99/200'
    elif __quality__ == "2":
        __best__ = ' 720p/0/99/200'
    elif __quality__ == "3":
        __best__ = ' 480p/0/99/200'

    pre1 =  __proxy__
    pre2 = '/search/'
    pre3 =  name
    pre4 = __addsearch__
    pre5 = __best__
    req = pre1 + pre2 + pre3 + ' ' + pre4 + pre5
    response = urllib2.urlopen((req). replace(" ", "%20"))
    #xbmc.log('Movie_Search: %s' % req, xbmc.LOGDEBUG)
    data = response.read()
    if response.headers.get("Content-Encoding", "") == "gzip":
        import zlib
        data = zlib.decompressobj(16 + zlib.MAX_WBITS).decompress(data)
    return [{"uri": magnet} for magnet in re.findall(r'magnet:\?[^\'"\s<>\[\]]+', data)]

urllib2.urlopen(
    PAYLOAD["callback_url"],
    data=json.dumps(globals()[PAYLOAD["method"]](*PAYLOAD["args"]))
)

