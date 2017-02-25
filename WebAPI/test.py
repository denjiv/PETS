import elevation
import traffic




def main():

    from_address = \
        'University of Washington, Seattle, WA, United States'
    to_address = \
        'Legend House, Roosevelt Way Northeast, Seattle, WA, United States'

    start_coords = traffic.address_to_coords(from_address)
    end_coords = traffic.address_to_coords(to_address)

    print start_coords
    print end_coords

    # Directly get the raw data from waze website
    waze_resp = traffic.get_waze_resp(start_coords, end_coords)

    # Processed Route Data
    route_info = traffic.get_route_info(waze_resp)
    route = traffic.get_route(waze_resp)

    ele = elevation.Elevation()
    elevations = ele.getElevations(route)


main()
