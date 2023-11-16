import math
import requests
from cs50 import SQL

def haversine(lat_1, lat_2, long_1, long_2):
    """ Returns the distance in miles between two points given by their latitude and longitude """
    earth_radius = 3959
    arcsin_content = math.sqrt((math.sin(math.radians((lat_2 - lat_1)/2)))**2 + math.cos(math.radians(lat_1)) * math.cos(math.radians(lat_2)) * math.sin(math.radians((long_2 - long_1)/2)**2))
    distance = 2 * earth_radius * math.asin(arcsin_content)
    return distance


def find_towns_in_radius(postcode, database, radius):
    """ Returns a list of the towns currently in the database which are close to the given postcode """
    near_cities = []

    # Queries API for longitude/latitude of user inputted postcode
    postcode_search = f"https://api.postcodes.io/postcodes/{postcode}"
    postcode_info = requests.get(postcode_search).json()
    if postcode_info["status"] != 200:
        return false
    else:
        user_lat, user_long = postcode_info["result"]["latitude"], postcode_info["result"]["longitude"]

    cities = database.execute("""SELECT * FROM cities WHERE (NOT latitude IS NULL AND NOT longitude IS NULL)""")

    # Runs through all cities in the database which have location information
    for city in cities:
        city_lat, city_long = city["latitude"], city["longitude"]

        # Calculates distance between user and city to determine if it falls in search radius
        distance = haversine(user_lat, city_lat, user_long, city_long)
        if distance <= radius:
            near_cities.append(city["city"])

    return near_cities


if __name__ == "__main__":
    pass
