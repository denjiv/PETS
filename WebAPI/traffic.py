#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import logging
import requests
import gmplot
import webbrowser
import matplotlib.pyplot as plt
import numpy as np

WAZE_URL = 'https://www.waze.com/'
NUMBER_OF_PATHS = 1
ZOOM = 13

def address_to_coords(address):
    """Convert address to coordinates"""

    get_cords = 'SearchServer/mozi?'
    url_options = {
        'q': address,
        'lang': 'eng',
        'origin': 'livemap',
        'lon': '19.040',
        'lat': '47.498',
        }
    response = requests.get(WAZE_URL + get_cords, params=url_options)
    response_json = response.json()[0]
    lon = response_json['location']['lon']
    lat = response_json['location']['lat']
    return {'lon': lon, 'lat': lat}


def get_waze_resp(start_coords, end_coords):
    """Get route data from waze"""

    routing_req = 'RoutingManager/routingRequest'

    url_options = {
        'from': 'x:%s y:%s' % (start_coords['lon'], start_coords['lat']),
        'to': 'x:%s y:%s' % (end_coords['lon'], end_coords['lat']),
        'at': 0,
        'returnJSON': 'true',
        'returnGeometries': 'true',
        'returnInstructions': 'true',
        'timeout': 60000,
        'nPaths': NUMBER_OF_PATHS,
        'options': '',
        }
    print url_options
    response = requests.get(WAZE_URL + routing_req, params=url_options)

    response_json = response.json()

    if response_json.get('error'):
        print 'ERROR'
    if response_json.get('alternatives'):
        return response_json['alternatives'][NUMBER_OF_PATHS-1]['response']
    return response_json['response']

def get_route(waze_resp):
    r = waze_resp
    results = r['results']
    route = []
    for segment in results:
        path = segment['path']
        route.append([path['y'], path['x']])
    return route

def get_route_info(r):
    """Calculate route info."""

    results = r['results']

    total_time = 0
    total_distance = 0
    node = 0

    lats = []
    lons = []

    route_info = {}

    for segment in results:
        this_time = segment['crossTime']
        this_distance = segment['length']

        total_time += this_time
        total_distance += this_distance

        this_time_hrs = hrs_to_sec(this_time)
        this_distance_miles = m_to_miles(this_distance)
        this_speed = this_distance_miles / this_time_hrs

        path = segment['path']
        node = node + 1
        route_info[node] = {}
        route_info[node]['location'] = (path['y'], path['x'])
        lats.append(path['y'])
        lons.append(path['x'])
        route_info[node]['time'] = this_time
        route_info[node]['speed'] = this_speed
        route_info[node]['distance'] = this_distance_miles
        route_info[node]['distance_from_start'] = m_to_miles(total_distance)

    route_distance = m_to_miles(total_distance)

    route_info['lons'] = lons
    route_info['lats'] = lats

    route_info['total_time'] = total_time
    route_info['total_distance'] = route_distance
    route_info['node_count'] = node

    print 'Total Route Time (mins): ', total_time / 60.00
    print 'Total Route Distance (miles)', route_distance

    return route_info

def main_traffic():

    from_address = \
        'University of Washington, Seattle, WA, United States'
    to_address = \
        'Legend House, Roosevelt Way Northeast, Seattle, WA, United States'

    start_coords = address_to_coords(from_address)
    end_coords = address_to_coords(to_address)

    print start_coords
    print end_coords

    # Directly get the raw data from waze website
    waze_resp = get_waze_resp(start_coords, end_coords)

    # Export it to a JSON file just for kicks
    #exportToJSON(route, 'raw_route_data.txt')

    # Processed Route Data
    route_info = get_route_info(waze_resp)

    route = get_route(waze_resp)

    # Open webpage with plot on google maps
    plotOnMap(start_coords, route_info)
    plot_speeds(route_info)

##################################
##### OTHER USEFUL FUNCTIONS #####
##################################

def plotOnMap(start_coords, route_info):

    lats = route_info['lats']
    lons = route_info['lons']

    gmap = gmplot.GoogleMapPlotter(start_coords['lat'],
                                   start_coords['lon'], ZOOM)

    gmap.plot(lats, lons, 'cornflowerblue', edge_width=6)

    url = 'mymap.html'

    gmap.draw(url)
    webbrowser.open(url, new=2)

def plot_speeds(route_info):
    lats = route_info['lats']
    lons = route_info['lons']

    distances = []
    times = []
    speeds = []

    node_count = route_info['node_count']
    for i in range(1, node_count):
        distances.append(route_info[i]['distance_from_start'])
        speeds.append(route_info[i]['speed'])
        times.append(route_info[i]['time'])

    plt.figure()
    plt.subplot(1, 1, 1)
    plt.plot(distances, speeds)
    plt.show()

def hrs_to_sec(sec):
    return sec / (60.00 * 60.00)

def m_to_miles(m):
    return m / 1000.00 * 0.621371

def exportToJSON(route, fileName):
    with open(fileName, 'w') as outfile:
        json.dump(route, outfile, sort_keys=True, indent=4,
                      ensure_ascii=False)
