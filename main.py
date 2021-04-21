from math import radians, cos, sin, asin, sqrt
import collections
import sys


def travel_time(lat1, lat2, lon1, lon2):
    '''
    Time taken to travel between two geo locations using
    Havershine formula with average speed 20 km/hr
    '''
    # The math module contains a function named
    # radians which converts from degrees to radians.
    lon1 = radians(lon1)
    lon2 = radians(lon2)
    lat1 = radians(lat1)
    lat2 = radians(lat2)

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2

    c = 2 * asin(sqrt(a))

    # Radius of earth in kilometers
    r = 6371

    # calculate the result
    return(c * r)/20


def route_travel_time(route):
    '''
    Time taken to cover all locations in the given route
    '''
    total_time = 0
    for i in range(len(route)-1):
        total_time = total_time + travel_time(
            route[i].lat, route[i+1].lat, route[i].lon, route[i+1].lon)
    return total_time


def get_efficient_route(sorted_orders, initial_position):
    '''
    returns a list of locations(restaurants and customers) representing a route
    for the delivery person, which completes the deliveries
    in shortest possible time

    '''
    number_of_orders = len(sorted_orders)

    first_order = sorted_orders[0]
    test_route = [initial_position, first_order.R, first_order.C]
    test_route_travel_time = []

    for order_num in range(1, number_of_orders):
        order = sorted_orders[order_num]
        test_route_length = len(test_route)

        test_route_travel_time = (float("inf"), (0, 0))
        '''
        get shortest delivery time for the orders
        using bruteforce(try all possible delivery routes)
        '''
        for i in range(2, test_route_length+1):
            test_route.insert(i, order.R)

            for j in range(i+1, test_route_length+2):
                test_route.insert(j, order.C)
                tt = route_travel_time(test_route)

                if tt < test_route_travel_time[0]:
                    test_route_travel_time = (tt, (i, j))
                del(test_route[j])

            del(test_route[i])

        optimal_position = test_route_travel_time[1]

        test_route.insert(optimal_position[0], order.R)
        test_route.insert(optimal_position[1], order.C)
    return test_route


def shortest_delivery_time(orders, initial_position):
    '''
    returns the shortest delivery time for a list of
    orders and an initial position of the
    delivery person
    '''

    '''
    The orders are sorted such that the order which is
    ready or about to get ready when
    the delivery person reaches the restaurant is preferred
    '''
    sorted_orders = sorted(
        orders,
        key=lambda o: abs(o[2] - travel_time(
            initial_position.lat, o.R.lat, initial_position.lon, o.R.lon))
        )
    efficient_route = get_efficient_route(sorted_orders, initial_position)
    sys.stdout.write('Best route: ' + str(efficient_route) + '\n')
    delivery_time = route_travel_time(efficient_route)
    return delivery_time


if __name__ == '__main__':
    '''
    Driver function for obtaining best route
    to deliver food for concurrent orders
    '''

    '''
    Input:
        location: (latitude, longitude)
        Order = (Restaurant:location, Customer:location, PreperationTime: in hrs)
    '''
    Order = collections.namedtuple('order', ['R', 'C', 'PT'])
    Location = collections.namedtuple('location', ['lat', 'lon'])

    DELIVERY_PERSON_LOCATION = Location(12.931560, 77.625560)
    CONCURRENT_ORDERS = [
        Order(
            Location(12.989990, 77.682400),
            Location(13.103882, 77.568687),
            0.8
            ),
        Order(
            Location(12.897510, 77.613460),
            Location(12.962000, 77.597040),
            1
            ),
        Order(
            Location(13.076816, 77.596264),
            Location(13.041083, 77.590716),
            0.5
            )
        ]

    shortest_delivery_time = shortest_delivery_time(
        CONCURRENT_ORDERS, DELIVERY_PERSON_LOCATION)
    sys.stdout.write(
        'Shortest possible time: ' + str(shortest_delivery_time) + ' hrs')
