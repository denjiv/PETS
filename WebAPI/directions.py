
class routePoint(object):
    def __init__(self, inLat, inLon, inEle=None, inStart=False, inEnd=False):
        self.lat = inLat
        self.lon = inLon
        self.ele = inEle
        self.start = inStart
        self.end = inEnd

    def display(self):
        print("\n" + repr(self.lat) + "\t" + repr(self.lon) + "\t" + repr(self.ele) + "\t" + repr(self.start) + " " + repr(self.end))


def routeInfo(startpnt, endpnt, key, mode='driving', plot=True, plotfile='mymap.html'):
    import googlemaps
    import json
    import polyline
    client = googlemaps.Client(key)
    dirResult = client.directions(startpnt, endpnt, mode, waypoints=None,
    alternatives=False, avoid=None, language=None, units="imperial", region=None,
    departure_time='now', arrival_time=None, optimize_waypoints=True,
    transit_mode=None, transit_routing_preference=None, traffic_model='pessimistic')

    print json.dumps(dirResult, indent=4, sort_keys=True)

    # Intiating all arrays
    # stores routePoint data structure
    routePoints = []
    # For elevation calculation
    points = []
    # For  plotting on the map
    latitudes1 = []
    longitudes1 = []
    samples = 0;

    # Get lat and lon points from the dictionary
    for item in dirResult[0]['legs'][0]['steps']:
        code = str(item['polyline']['points'])
        poly = polyline.decode(code)
        for coord in poly:
            tmpPoint = routePoint(coord[0], coord[1])
            if (samples == 0):
                tmpPoint.start = True
            routePoints.append(tmpPoint)
            samples = samples + 1
            points.append(coord)
            latitudes1.append(coord[0])
            longitudes1.append(coord[1])

    # Get the elevation points
    eleResult = client.elevation_along_path(points, samples)
    for i in range(0, samples):
        routePoints[i].ele = eleResult[i]['elevation']
        if (i == samples-1):
            routePoints[i].end = True

    # Plot html map. Saved in mymap.html
    if plot:
        import gmplot
        gmap = gmplot.GoogleMapPlotter(47.6682253, -122.3195193, 16)
        gmap.plot(latitudes1, longitudes1, 'cornflowerblue', edge_width=10)
        gmap.scatter(latitudes1, longitudes1, 'r', marker=True)
        gmap.draw(plotfile)

    return routePoints

# Testing the route
# Make into a test method later.
startpnt = '5336 8th Ave NE, Seattle, WA 98105'
endpnt = 'Space Needle , Seattle, WA 98105'
mode = 'driving'
key = "AIzaSyDjLCEDNPFDYj8kzvwWXVaE3VO6ELF45qI"
route = routeInfo(startpnt, endpnt, key)
# Print as a table
import texttable as tt
tab = tt.Texttable()
x = [[]] # The empty row will have the header
for point in route:
    x.append([point.lat,point.lon,point.ele,point.start,point.end])
tab.add_rows(x)
tab.set_cols_align(['r','r','r','r','r'])
tab.header(['Latitude', 'Longitude', 'Elevation','Start','End'])
print tab.draw()
