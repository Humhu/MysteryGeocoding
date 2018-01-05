"""Common representations
"""

import json


class GeocodeInfo:
    """Container for standard geocode query responses

    Parameters
    ==========
    address : string
        The matched address
    latitude : float
        The latitude of the found address
    longitude : float
        The longitude of the found address
    """

    def __init__(self, address, latitude, longitude):
        self.address = address
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self):
        return 'address: %s, latitude: %f, longitude: %f' \
               % (self.address, self.latitude, self.longitude)

    def to_jsons(self):
        """Converts the info into a JSON string
        """
        out = {'address': self.address,
               'latitude': self.latitude,
               'longitude': self.longitude}
        return json.dumps(out)

    @staticmethod
    def from_jsons(raw):
        """Creates a new info instance from a JSON string
        """
        parsed = json.loads(raw)
        try:
            return GeocodeInfo(address=parsed['address'],
                               latitude=parsed['latitude'],
                               longitude=parsed['longitude'])
        except KeyError:
            print 'Malformed JSON for GeocodeInfo'
            return None
