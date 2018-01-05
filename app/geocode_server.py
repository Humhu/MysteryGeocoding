"""Main application to launch the server
"""

import argparse
import sys
import geocode as gc

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Launches a geocoding server wrapping '
                                     + 'HERE and Google Maps geocoding')
    parser.add_argument('--here_app_id',
                        default='2EJhFkBmtvfKut6jkpCC',
                        help='The application ID to use with HERE')
    parser.add_argument('--here_app_code',
                        default='cFUXcYjaN0mXmgrCr6IEdg',
                        help='The application code to use with HERE')
    parser.add_argument('--google_api_key',
                        default='AIzaSyCPUagqPZpa8jL1ZvWjnKV9wWextbhZ0EE',
                        help='The API key to use with Google Maps')

    args = parser.parse_args()

    google_coder = gc.GoogleGeocoder(api_key=args.google_api_key)
    here_coder = gc.HereGeocoder(app_id=args.here_app_id,
                                 app_code=args.here_app_code)

    # NOTE Order of adding determines precedence
    server_address = ('', 8000)
    server = gc.GeocodeServer(server_address)
    server.add_external(google_coder)
    server.add_external(here_coder)
    server.serve_forever()

    sys.exit(-1)
