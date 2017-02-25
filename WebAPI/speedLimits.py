#!/usr/bin/python
# -*- coding: utf-8 -*-

import googlemaps
import traffic
import json

gmaps = googlemaps.Client(key='AIzaSyDjLCEDNPFDYj8kzvwWXVaE3VO6ELF45qI')

def main2():
    from_address = \
        'University of Washington, Seattle, WA, United States'
    to_address = \
        'Legend House, Roosevelt Way Northeast, Seattle, WA, United States'

    startpnt = '5336 8th Ave NE, Seattle, WA 98105'
    endpnt = 'Space Needle , Seattle, WA 98105'

    start_coords = traffic.address_to_coords(startpnt)
    end_coords = traffic.address_to_coords(endpnt)

    print start_coords
    print end_coords

    # Directly get the raw data from waze website
    waze_resp = traffic.get_waze_resp(start_coords, end_coords)
    #print json.dumps(waze_resp, indent=4, sort_keys=True)
    # Export it to a JSON file just for kicks
    #exportToJSON(route, 'raw_route_data.txt')

    # Processed Route Data
    route_info = traffic.get_route_info(waze_resp)
    #print json.dumps(route_info, indent=4, sort_keys=True)
    route = traffic.get_route(waze_resp)
    print route
    #print json.dumps(route, indent=4, sort_keys=True)
    newroute = gmaps.snap_to_roads(route, interpolate=False)

    #speeds = gmaps.snapped_speed_limits(route)
    #print speeds

    # Open webpage with plot on google maps
    #plotOnMap(start_coords, route_info)

main2()
