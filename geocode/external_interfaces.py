"""Classes and software to interface with external geocoding services

NOTE: While it would be nice to move each implementation into its own file,
ie. google_maps.py, here.py, I will leave them together here for ease of reading
"""

import abc
import json
import httplib

from geocode.common import GeocodeInfo

# TODO Handle multiple results on queries
# TODO Do more parsing of address to common format
class ExternalGeocoder:
    """Base class for all external geocoding wrapper classes. Provides functionality
    for querying the latitude and longitude of a string address.

    Parameters
    ==========
    timeout : numeric (default 10)
        Number of seconds to wait before timing out when connecting to the server
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, timeout=10):
        self._timeout = timeout

    def query_address(self, address):
        """Queries the external geocoding service with the specified address.
        Connects to the server on each call for robustness. Returns None if 
        the query fails.

        Parameters
        ==========
        address : string
            The address to query

        Returns
        =======
        res : GeocodeInfo or None
            If successful, returns found address info, else None
        """
        try:
            conn = httplib.HTTPSConnection(
                self.server_url, timeout=self._timeout)
        except httplib.HTTPException as e:
            print 'Could not connect to server %s\n%s' % (self.server_url, str(e))
            return None

        conn.request('GET', self.assemble_request(address))
        response = conn.getresponse()
        if response.status != httplib.OK:
            print 'Error in response when querying %s\n%s' % (address, response.reason)
            return None

        data = response.read()
        res = self.parse_response(data)
        if res is None:
            print 'Did not find any matches for %s' % address
        return res

    @abc.abstractproperty
    def server_url(self):
        """Return the server URL for this external geocoding service
        """
        pass

    @abc.abstractmethod
    def assemble_request(self, address):
        """Forms a HTTP request string for the specified address to go
        with this external geocoding service

        NOTE: Does not do any error checking on the string - that is handled
        by looking at the service response data

        Parameters
        ==========
        address : string
            Query address to retrieve

        Returns
        =======
        request : string
            URL to use with HTTP GET operation for querying
        """
        pass

    @abc.abstractmethod
    def parse_response(self, data):
        """Parses the returned data from a successful query into
        a standard dict format, described below.

        Dict Fields
        ===========
        latitude : Query latitude
        longitude : Query longitude
        address : Matched address

        Parameters
        ==========
        data : string
            Received data from a successful HTTP GET

        Returns
        =======
        parsed : dict
            Parsed information in dict form
        """
        pass

class GoogleGeocoder(ExternalGeocoder):
    """Provides access to the Google Maps geocoding service

    Parameters
    ==========
    api_key : string
        The Google API key to use for service requests
    """

    def __init__(self, api_key, **kwargs):
        ExternalGeocoder.__init__(self, **kwargs)
        self._api_key = api_key

    @property
    def api_key(self):
        return self._api_key

    @property
    def server_url(self):
        return 'maps.googleapis.com'

    def assemble_request(self, address):
        return '/maps/api/geocode/json?address=%s&key=%s' % (address, self._api_key)

    def parse_response(self, data):
        decoded = json.loads(data)
        results = decoded['results']
        if len(results) == 0:
            return None
        else:
            result = results[0]
            return GeocodeInfo(address=result['formatted_address'],
                               latitude=result['geometry']['location']['lat'],
                               longitude=result['geometry']['location']['lng'])


class HereGeocoder(ExternalGeocoder):
    """Provides access to the HERE geocoding service

    Parameters
    ==========
    app_id : string
        HERE account application ID
    app_code : string
        HERE account application code
    """

    def __init__(self, app_id, app_code, **kwargs):
        ExternalGeocoder.__init__(self, **kwargs)
        self._app_id = app_id
        self._app_code = app_code

    @property
    def app_id(self):
        return self._app_id

    @property
    def app_code(self):
        return self._app_code

    @property
    def server_url(self):
        return 'geocoder.cit.api.here.com'

    def assemble_request(self, address):
        return '/6.2/geocode.json?searchtext=%s&app_id=%s&app_code=%s&gen=8' \
               % (address, self._app_id, self._app_code)

    def parse_response(self, data):
        decoded = json.loads(data)
        view = decoded['Response']['View']
        if len(view) == 0:
            return None
        else:
            base = view[0]['Result'][0]['Location']
            return GeocodeInfo(address=base['Address']['Label'],
                               latitude=base['NavigationPosition'][0]['Latitude'],
                               longitude=base['NavigationPosition'][0]['Longitude'])
