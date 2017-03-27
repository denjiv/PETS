import directions
import json
import traffic
import polyline
import gmplot
import webbrowser
import matplotlib.pyplot as plt
import pprint
from collections import namedtuple
import map_functions
import googlemaps
from elevation import Elevation


GMAPI_KEY = 'AIzaSyDjLCEDNPFDYj8kzvwWXVaE3VO6ELF45qI'
WAZE_URL = 'https://www.waze.com/'
NUMBER_OF_PATHS = 1
leg_node_array_total = {}

def get_elevation(coordinate, samples):
    client = googlemaps.Client(GMAPI_KEY)
    # coordinate = {}
    # coordinate['lat'] = 48
    # coordinate['lng'] = -122
    elevation = client.elevation_along_path(coordinate)
    # print elevation
    return elevation
    # for i in range(0, samples):
    #     routePoints[i].ele = elevation[i]['elevation']
    #     if (i == samples-1):
    #         routePoints[i].end = True

#----- WAZE -----#
def get_waze_nodes(complete_waze, parsed_waze):
    waze_coords  = parsed_waze  # waze link coord

    waze_data = {}
    points = []
    waze_lat = []
    waze_lon = []
    waze_type = []
    waze_speed = []
    node = 0

    for i in range(1,complete_waze+1):
        node = node + 1
        waze_data[node] = {}

        lat = waze_coords[str(i)]["location"][0]
        lon = waze_coords[str(i)]["location"][1]

        waze_lat.append(lat)
        waze_lon.append(lon)
        waze_type.append('WAZE')
        points.append([lat, lon])

        waze_data[node]['lat'] = lat
        waze_data[node]['lon'] = lon
        waze_data[node]['speed'] = parsed_waze[str(i)]['speed']
        waze_data[node]['ele'] = '0'
        waze_data[node]['type'] = 'WAZE'
        print lat
        print len(waze_data)

    elevation = Elevation()
    # print elevation.getElevations(points)
    elevation_output = elevation.getElevations(points)

    node = 0

    for i in elevation_output:
        node = node + 1
        waze_data[node]['ele'] = i
    map_functions.export_to_JSON(waze_data, 'waze_nodes.json')
    map_functions.plot_coords(waze_lat, waze_lon, waze_type, 16, 'waze_nodes.html')
    return waze_data


def get_google_nodes(waze_count, waze_coords):
    g_lat = []
    g_lon = []
    g_speed = []
    g_type = []
    g_elev = []

    index = 1
    waze_index = 1
    total_index = 1
    total_node_index = 1

    while (index < waze_count):
        g_start     = [waze_coords[index]['lat'], waze_coords[index]['lon']]
        g_end       = [waze_coords[index + 1]['lat'], waze_coords[index + 1]['lon']]
        leg_nodes   = directions.routeInfo(g_start, g_end, GMAPI_KEY)
        leg_size    = len(leg_nodes)

        leg_index = 1
        leg_array = {}

        for i in leg_nodes:
            leg_array[leg_index] = {}
            if (leg_index == 1) or (leg_index == waze_count):  # start node of google leg nodes
                leg_array[leg_index] = waze_coords[index]     # replace first leg index with waze point

                g_lat.append(waze_coords[index]['lat'])
                g_lon.append(waze_coords[index]['lon'])
                g_type.append(waze_coords[index]['type'])
                waze_index = waze_index + 1
            else:
                g_lat.append(i.lat)
                g_lon.append(i.lon)
                g_type.append('google')

                leg_array[leg_index]['lat'] = i.lat
                leg_array[leg_index]['lon'] = i.lon
                leg_array[leg_index]['speed'] = i.speed
                leg_array[leg_index]['ele'] = i.ele
                leg_array[leg_index]['type'] = i.type

            leg_index = leg_index + 1
            total_node_index = total_node_index + 1
        for item in leg_array:
            leg_node_array_total[total_index] = leg_array[item]
            total_index = total_index + 1
        index = index + 1

    if (index == waze_count):
        leg_node_array_total[total_index] = waze_coords[waze_count]     # replace first leg index with waze point
        g_lat.append(waze_coords[waze_count]['lat'])
        g_lon.append(waze_coords[waze_count]['lon'])
        g_type.append(waze_coords[waze_count]['type'])
    return [g_lat, g_lon, g_type]



def main():
    route = map_functions.intro()
    infile = "To_REI_PRIUS_Waze_3-24-2017.txt"
    with open(infile) as data_file:
        result = json.load(data_file)

    start_coords    = route['start']
    end_coords      = route['end']
    complete_waze   = 0   # raw data from waze as JSON
    parsed_waze     = result   # processed route info as JSON

    #map_functions.export_to_JSON(complete_waze, 'waze_complete.json')

    waze_count = parsed_waze['node_count']

    map_functions.export_to_JSON(parsed_waze, 'waze_full_output.json')
    route_index = get_waze_nodes(waze_count, parsed_waze)

    total_nodes = get_google_nodes(waze_count, route_index)
    g_lat       = total_nodes[0]
    g_lon       = total_nodes[1]
    g_type      = total_nodes[2]

    map_functions.plot_coords(g_lat, g_lon, g_type, 16, 'total_nodes.html')
    map_functions.export_to_JSON(leg_node_array_total, 'total_nodes.json')

main()
