"""Servers and handlers for REST requests
"""

import httplib
import BaseHTTPServer

from geocode.external_interfaces import ExternalGeocoder

class GeocodeServer(BaseHTTPServer.HTTPServer):
    def __init__(self, address):
        BaseHTTPServer.HTTPServer.__init__(self, address, GeocodeRequestHandler)

        self.coders = []

    def add_external(self, coder):
        if not isinstance(coder, ExternalGeocoder):
            raise ValueError('Object does not implement ExternalCoder interface')
        self.coders.append(coder)

class GeocodeRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    """Handles GET (REST) requests for querying geocodes

    Parameters
    ==========
    parser : function
        Parses a request string to a query address
    """

    @staticmethod
    def extract_address(request):
        """Basic implementation of an address parser that looks for format
        /geocode/address=<address>
        """
        # First find and strip out /geocode/
        header = '/geocode/'
        if not request.startswith(header):
            return None
        request = request.partition(header)[2]

        splits = request.split('&')
        for s in splits:
            parts = s.split('=')
            if len(parts) != 2:
                continue
            tag, value = parts
            if tag == 'address':
                return value
        return None


    def do_GET(self):
        address = GeocodeRequestHandler.extract_address(self.path)

        if address is None:
            self.send_error(code=httplib.BAD_REQUEST,
                            message='Could not parse address from request')
            return

        info = None
        for ext in self.server.coders:
            print 'Querying %s for %s...' % (ext.server_url, address)
            info = ext.query_address(address)
            if info is not None:
                break
        
        if info is None:
            self.send_error(code=httplib.BAD_REQUEST,
                            message='No successful queries')
            return

        self.send_response(code=httplib.OK)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        encoded = info.to_jsons()
        self.wfile.write(encoded)
