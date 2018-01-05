"""Tests server by querying it with different test cases
"""

import httplib
import geocode as gc


local_conn = httplib.HTTPConnection('127.0.0.1', port=8000, timeout=10)

def query_local(address):
    print 'Querying %s...' % address
    request = '/geocode/address=%s' % address
    local_conn.request('GET', request)
    
    res = local_conn.getresponse()
    if res.status != httplib.OK:
        info = None
    else:
        info = gc.GeocodeInfo.from_jsons(res.read())
    
    if info is not None:
        print str(info)
    else:
        print 'No successful queries returned'


# Should work on Google
query_local('1600+Amphitheatre+Parkway,+Mountain+View,+CA')

# Should work on HERE but not Google
query_local('1600+Amphitheatre+Parkway,+Mountainish,+CA')

# Should work on neither
query_local('1600+Amphitheatre+Parkway,+MouMouMou,+PA')