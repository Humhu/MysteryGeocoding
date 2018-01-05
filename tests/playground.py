"""A little playground for me to figure out how this HTTP thing works
"""

import sys
import httplib
import json

def parse_here_response(response_data):
    """Parses a response string from HERE geocoding to get lat, lng
    """
    decoded = json.loads(response_data)
    base = decoded['Response']['View'][0]['Result'][0]['Location']['NavigationPosition'][0]
    return base['Latitude'], base['Longitude']

def parse_google_response(response_data):
    """Parses a response string from Google Maps to get lat, lng
    """
    decoded = json.loads(response_data)
    base = decoded['results'][0]['geometry']['location']
    return base['lat'], base['lng']


# An example request for my credentials using HERE's service
#here_url = 'https://geocoder.cit.api.here.com/6.2/geocode.json?searchtext=200%20S%20Mathilda%20Sunnyvale%20CA&app_id=2EJhFkBmtvfKut6jkpCC&app_code=cFUXcYjaN0mXmgrCr6IEdg&gen=8'
here_server = 'geocoder.cit.api.here.com'
here_request = '/6.2/geocode.json?searchtext=200%20S%20Mathilda%20Sunnyvale%20CA&app_id=2EJhFkBmtvfKut6jkpCC&app_code=cFUXcYjaN0mXmgrCr6IEdg&gen=8'

# An example request for my credentials using Google Maps' service
#google_url = 'https://maps.googleapis.com/maps/api/geocode/json?address=1600+Amphitheatre+Parkway,+Mountain+View,+CA&key=AIzaSyCPUagqPZpa8jL1ZvWjnKV9wWextbhZ0EE'
google_server = 'maps.googleapis.com'
google_request = '/maps/api/geocode/json?address=1600+Amphitheatre+Parkway,+Mountain+View,+CA&key=AIzaSyCPUagqPZpa8jL1ZvWjnKV9wWextbhZ0EE'

# Test querying HERE
try:
    here_conn = httplib.HTTPSConnection(here_server, timeout=10)
except httplib.HTTPException as e:
    print 'Could not connect to HERE: %s' % str(e)
    sys.exit(-1)

here_conn.request('GET', here_request)
here_res = here_conn.getresponse()
print here_res.status, here_res.reason
here_data = here_res.read()
print parse_here_response(here_data)

# Test querying Google Maps
try:
    google_conn = httplib.HTTPSConnection(google_server, timeout=10)
except httplib.HTTPException as e:
    print 'Could not connect to Google: %s' % str(e)
    sys.exit(-1)

google_conn.request('GET', google_request)
google_res = google_conn.getresponse()
print google_res.status, google_res.reason
google_data = google_res.read()
print parse_google_response(google_data)