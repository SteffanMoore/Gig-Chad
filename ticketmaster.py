# Use GB as the country code for the ticketmaster API
# API key: l2Fai6cbv95uwgP5dN8UAkNdg7Uhk4bX

import requests
from datetime import datetime, timedelta
from data_extraction import extract_all
from cs50 import SQL
import time


api_key = "l2Fai6cbv95uwgP5dN8UAkNdg7Uhk4bX"
api_url = "https://app.ticketmaster.com/discovery/v2/"

# Converts a datetime object into the string format used by ticketmaster
def convert_time_to_string(time):
    formatted_time = time.strftime("%Y-%m-%dT%H:%M:%SZ")

    return formatted_time


# Converts the string format used by ticketmaster into a datetime object
def convert_string_to_time(string):
    time_object = datetime.strptime(string, "%Y-%m-%dT%H:%M:%SZ")

    return time_object


# Takes the strings stored in the update server table and converts them to a list
def interpret_server_update_strings(cities, genres):
    city_list = list(cities.split('", '))
    genre_list = list(genres.split('", '))

    return city_list, genre_list


# Takes lists and creates strings to store them in the database
def format_server_update_strings(cities, genres, date):
    city_string, genre_string = '', ''

    for city in cities:
        city_string += str(city)
        if city != cities[-1]:
            city_string += '", '

    for genre in genres:
        genre_string += str(genre)
        if genre != genres[-1]:
            genre_string += '", '

    date_string = convert_time_to_string(date)

    return city_string, genre_string, date_string


def retrieve_server_update(database):
    """ Searches the server_updates table from input database for most recent entry and returns a list of genres/cities """

    stored_categories = database.execute("SELECT * FROM server_updates WHERE update_index = (SELECT MAX(update_index) FROM server_updates)")

    # If the row is found the strings are interpretted and put into a list (otherwise returns empty list)
    try:
        found_cities, found_genres = interpret_server_update_strings(stored_categories[0]["cities"], stored_categories[0]["genres"])
    except IndexError:
        found_cities, found_genres = [], []

    return found_cities, found_genres


def city_locator(database):
    """ Goes through cities saved to server_updates table and, if not in the cities table, uses postcode API to return
        latitude and longitude.
    """

    cities_found, unused_genre_list = retrieve_server_update(database)

    # For each city in the server_update table, the API is called to retrieve info about it
    for city in cities_found:

        city_query = f"https://api.postcodes.io/places?q=[{city}]"
        city_info = requests.get(city_query).json()

        # Sets up conditions to find the largest settlement in the returned information
        possible_sizes = {"City": 4, "Town": 3, "Suburban Area": 2, "Village": 1, "Hamlet": 0}
        current_size = -1
        largest_settlement_index = 0

        # Runs through settlements returned in the result to find the biggest (so most likely)
        for settlement in range(len(city_info["result"])):
            settlement_size = city_info["result"][settlement]['local_type']
            if settlement_size in possible_sizes:
                if possible_sizes[settlement_size] > current_size:
                    current_size = possible_sizes[settlement_size]
                    largest_settlement_index = settlement


        # If no location data on the city is found, it is added without the longitude and latitude
        try:
            city_lat, city_long = city_info["result"][largest_settlement_index]["latitude"], city_info["result"][largest_settlement_index]["longitude"]

            # The city is only added if it's not already in the database
            try:
                database.execute("BEGIN TRANSACTION")
                database.execute("""INSERT INTO cities (city, latitude, longitude) VALUES(?, ?, ?)""", city, city_lat, city_long)
                database.execute("COMMIT")
            except ValueError:
                database.execute("ROLLBACK")

        except IndexError:
            try:
                database.execute("BEGIN TRANSACTION")
                database.execute("""INSERT INTO cities (city) VALUES(?)""", city)
                database.execute("COMMIT")
            except ValueError:
                database.execute("ROLLBACK")


# Adds a page returned by the API to the events table in the database
def add_page_to_db(database, json_object, city_list, genre_list):

    # Extracts and adds each event in the json object to the database
    for event in json_object["_embedded"]["events"]:
        data = extract_all(event)

        # Adds city and genre to available list stored in server update table
        if data["city"] not in city_list:
            city_list.append(data["city"])

        if data["genre"] not in genre_list:
            genre_list.append(data["genre"])

        if data["subgenre"] not in genre_list:
            genre_list.append(data["subgenre"])

        # Attempts to add event to database
        try:
            database.execute("BEGIN TRANSACTION")
            database.execute("""INSERT INTO events (event_id, city, postcode, venue, price_range, genre, subgenre, date, artist, event_name, saved) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",\
                            data['unique_id'], data['city'], data['postcode'], data['venue'], data['price_range'],\
                                data['genre'], data['subgenre'], data['event_date'], data['artist'], data['event_name'], 0)
            database.execute("COMMIT")

        except ValueError:
            database.execute("ROLLBACK")


def populate_event_db(days=30, time_width=5):
    """ Used to retrieve events using ticketmaster API """

    target_db = SQL("sqlite:///gigchad_db.db")

    added_cities, added_genres = retrieve_server_update(target_db)

    # Search time constraints
    search_time_width = timedelta(days=time_width)
    search_initial_start_time = datetime.now()

    # Sets up initial search time variables
    search_start_time = search_initial_start_time
    search_end_time = search_start_time + search_time_width
    current_end_time = time_width

    # Retrieves data from sections within the overall search period
    while current_end_time <= days:
        start_time_formatted = convert_time_to_string(search_start_time)
        end_time_formatted = convert_time_to_string(search_end_time)

        # Carries out individual searches within the time section being searched
        initial_query_string = f"events.json?size=200&page=0&classificationName=music&countryCode=GB&startDateTime={start_time_formatted}&endDateTime={end_time_formatted}&apikey={api_key}"
        initial_search = requests.get(api_url + initial_query_string)

        # If the search is a success, number of pages is found and all pages are added to database
        if initial_search.status_code == 200:
            print(f"primary success - end time up to {current_end_time}")
            initial_response = initial_search.json()
            add_page_to_db(target_db, initial_response, added_cities, added_genres)

            # Retrieves data from all pages in time range
            for page in range(initial_response["page"]["totalPages"] - 1):
                search_complete = False
                query_string = f"events.json?size=200&page={page + 1}&classificationName=music&countryCode=GB&startDateTime={start_time_formatted}&endDateTime={end_time_formatted}&apikey={api_key}"

                # Attempts to retrieve page until it receives a success status code
                while search_complete == False:
                    search = requests.get(api_url + query_string)

                    if search.status_code == 200:
                        response = search.json()
                        print(f"success - page {page + 1} also retrieved")
                        add_page_to_db(target_db, response, added_cities, added_genres)
                        search_complete = True
                    else:
                        print("failure")
                        time.sleep(1)
                        continue

        else:
            print("primary failure")
            time.sleep(1)
            continue


        # Changes section end time to the lastest requested time for the last section
        if current_end_time != days and current_end_time + time_width > days:
            current_end_time = days
            search_end_time = search_initial_start_time + timedelta(days=days)
        # Otherwise section end time is the previous + section width
        else:
            current_end_time += time_width
            search_end_time = search_end_time + search_time_width

        # Changes the section start time to the next section
        search_start_time = search_start_time + search_time_width

    # Converts the cities and genres in the database to a string for storage
    update_server_log = format_server_update_strings(added_cities, added_genres, search_initial_start_time)
    target_db.execute("""INSERT INTO server_updates (date, cities, genres) VALUES(?, ?, ?)""", update_server_log[2], update_server_log[0], update_server_log[1])


def delete_old_events():
    """ Deletes old events once they have occured (unless they are saved) """

    target_db = SQL("sqlite:///gigchad_db.db")
    current_time = datetime.now()

    # Selects all unsaved events
    unsaved_events = target_db.execute("""SELECT * FROM events WHERE saved = 0""")

    # Runs through events and deletes them if they occured in the past
    for event in unsaved_events:
        if datetime.strptime(event["date"], "%Y-%m-%d") < current_time:
            target_db.execute("""DELETE FROM events WHERE event_id=?""", event["event_id"])


def update_event_db(update_span, sub_widths):
    """ Updates the database with new events and deletes old events if necessary. """

    target_db = SQL("sqlite:///gigchad_db.db")
    latest_update = target_db.execute("SELECT * FROM server_updates WHERE update_index = (SELECT MAX(update_index) FROM server_updates)")

    # Updates the server if it hasn't been updated within the past 24hrs.
    if (convert_string_to_time(latest_update[0]["date"]) + timedelta(days=1)) < datetime.now():
        print("Database updating")
        populate_event_db(days=update_span, time_width=sub_widths)
        print("New events added - deleting old events")
        delete_old_events()
        print("Retrieving city location information")
        city_locator(target_db)
        print("Update complete")
    else:
        print("Database updated within the last 24hrs")


# Only use this to initially populate the database
if __name__ == "__main__":
    datab = SQL("sqlite:///gigchad_db.db")
    print(datab.execute("""SELECT * FROM events WHERE ((city in (?) AND (genre in (?) OR subgenre in (?))) AND artist NOT IN (?)) OR artist in (?)""", ["Bristol"], ["Punk"], ["Punk"], ["Mr Blobby"], ["Circa Waves"]))


