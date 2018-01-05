"""Test of external interfaces with Google and HERE
"""

import geocode as gc

google_coder = gc.GoogleGeocoder(api_key='AIzaSyCPUagqPZpa8jL1ZvWjnKV9wWextbhZ0EE')
here_coder = gc.HereGeocoder(app_id='2EJhFkBmtvfKut6jkpCC', 
                             app_code='cFUXcYjaN0mXmgrCr6IEdg')

good_query = '1600+Amphitheatre+Parkway,+Mountain+View,+CA'
print 'Querying Google for good query %s' % good_query
print google_coder.query_address(good_query)

print 'Querying HERE for good query %s' % good_query
print here_coder.query_address(good_query)

bad_query = '1600+Amphitheatre+Parkway,+Mountainish,+CA'
print 'Querying Google for bad query %s' % bad_query
print google_coder.query_address(bad_query)

print 'Querying HERE for bad query %s' % bad_query
print here_coder.query_address(bad_query)