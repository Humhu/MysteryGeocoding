# MysteryGeocoding
Mini project to learn about geocoding, HTTP servers, and Python. 

Provides a rudimentary server that handles basic geocode requests

## Requirements
Uses only the Python standard library, so there are no external requirements.

## Structure
A small library `geocode` can be found in `/geocode`. It contains classes for interacting with external geocoding, common formats, and handling. The server itself can be found in `/app`, and a few tests are in `/test`.

## Supported Geocoding Services
* Google Maps: https://developers.google.com/maps/documentation/geocoding/start
* HERE: https://developer.here.com/documentation/geocoder/topics/quick-start.html

## Query Order
The server is currently hardcoded to first query from Google Maps, and then HERE in case of failure.

# Command Line Usage
## Running the Server
To launch the server from the command line, add the project folder to your PYTHONPATH and run:
```
python app/geocode_server.py [parameters]
```
By default, the server will use my keys for HERE/Google Maps. You can specify your own keys with the following optional parameters:
* --here_app_id: The application ID to use with HERE
* --here_app_code: The application code to use with HERE
* --google_api_key: The API key to use with Google Maps

Also by default, the server will initialize to the local machine on port 8000. To change this behavior, use the following optional parameters:
* --server_address: The address to start the HTTP server on
* --server_port: The port to start the HTTP server with

You can also see help on the command line by running the server with `-h`.

## Querying the Server
Once the server is running, queries can be made on the command line or browser by navigating to URLs in the format:
```
http://<server_address>:<server_port>/geocode/address=<address>
```

where the appropriate server info should be specified and `<address>` should be replaced with the query address string. If a match is found, a JSON string will be returned with the matched address, latitude, and longitude. If no match is found, the server will return a 400 code (BAD_REQUEST).

As an example, with the default server settings `http://127.0.0.1:8000/geocode/address=1600+Amphitheatre+Parkway,+Mountain+View,+CA` returns the address of a Google building as:
```
{"latitude": 37.4224082, "longitude": -122.0856086, "address": "Google Building 41, 1600 Amphitheatre Pkwy, Mountain View, CA 94043, USA"}
```

# Geocode API Usage
The `geocode` library used in this project contains a few classes that may be useful in other projects, or to extend here. The source files are fully documented, and an overview is given here for each module.

* `common`: Core geocode information representation class GeocodeInfo
* `external_interfaces`: Base class ExternalGeocoder that can be extended for supporting new geocoding services
* `rest_handler`: Server, handler, and parsing implementations for this project's server
