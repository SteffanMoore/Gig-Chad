from cs50 import SQL
import requests
from ticketmaster import retrieve_server_update

def check_pref_exist(database, user_id):
    """ Checks whether a preference entry exists for a user """

    preferences = database.execute("""SELECT * FROM preferences WHERE id = ?""", user_id)

    # Returns True if a user row is found but false if the index doesn't exist
    try:
        preferences[0]
        return True
    except IndexError:
        return False


def retrieve_postcode(database, user_id):
    """ Returns user's postcode or False if no postcode entered """

    user_postcode = database.execute("""SELECT postcode FROM preferences WHERE id = ?""", user_id)

    if user_postcode[0]["postcode"] == None:
        return False
    else:
        return user_postcode[0]["postcode"]


def create_pref_entry(database, user_id):
    """ Creates a new preference entry for the user """

    database.execute("""INSERT INTO preferences (id) VALUES(?)""", user_id)


def retrieve_column(database, user_id, column):
    """ Retrieves a string from preferences and returns it as a list """

    retrieved = database.execute(f"""SELECT {column} FROM preferences WHERE id = ?""", user_id)[0][column]

    # If no data is found in the preference column, an empty list is returned. Otherwise the found string is converted to list.
    if retrieved == None:
        retrieved_list = []
        return retrieved_list
    else:
        retrieved_list = list(retrieved.split('", '))
        return retrieved_list


def retrieve_genres(database, user_id):
    """ Retrieves the user preference genres and all genres and returns a dictionary of genres
        of which are prefered by the user and which aren't
        """

    # Selects the genre lists from the server update list and user preference
    user_genres = retrieve_column(database, user_id, "genres")
    city_list, genre_list = retrieve_server_update(database)

    # For all genres, checks whether they are saved as a preference or not
    present_in_pref = {}
    for genre in genre_list:
        if genre in user_genres:
            present_in_pref[genre] = 1
        else:
            present_in_pref[genre] = 0

    return present_in_pref



def update_column(database, user_id, column, pref_list):
    """ Converts an input list into a string and saves it into preferences """

    # Runs through the input list and converts into a string delimited with '", '
    pref_string = ''
    for item in pref_list:
        pref_string += str(item)
        if item != pref_list[-1]:
            pref_string += '", '

    database.execute(f"""UPDATE preferences SET {column} =  ? WHERE id = ?""", pref_string, user_id)


def update_postcode(database, user_id, postcode):
    """ Checks the new postcode is valid before updating the database value for a user, returning the request result """

    # Queries API to check if postcode is valid
    validation_request = requests.get(f"https://api.postcodes.io/postcodes/{postcode}/validate")
    validation = validation_request.json()

    # If the postcode is validated, the database is updated
    if validation['result'] == True:
        database.execute("""UPDATE preferences SET postcode = ? WHERE id = ?""", postcode, user_id)

    return validation['result']


def update_preference(database, user_id, preference, add_items, remove_items):
    """ Retrieves preferences for a single preference from the database and then adds or removes items """

    saved_items = retrieve_column(database, user_id, preference)

    if add_items != None:
        for new_item in add_items:
            if new_item in saved_items:
                pass
            else:
                saved_items.append(new_item)

    if remove_items != None:
        for unwanted in remove_items:
            if unwanted in saved_items:
                saved_items.remove(unwanted)

    update_column(database, user_id, preference, saved_items)


def update_user_preferences(database, user_id, postcode=None, add_events=None, remove_events=None,
                            add_genres=None, remove_genres=None, add_whitelist=None, remove_whitelist=None,
                            add_blacklist=None, remove_blacklist=None):
    """ Updates a user preferences """

    if postcode != None:
        if update_postcode(database, user_id, postcode) == False:
            return False

    if add_events != None or remove_events != None:
        update_preference(database, user_id, "saved_events", add_events, remove_events)

    if add_genres != None or remove_genres != None:
        update_preference(database, user_id, "genres", add_genres, remove_genres)

    if add_whitelist != None or remove_whitelist != None:
        update_preference(database, user_id, "whitelist", add_whitelist, remove_whitelist)

    if add_blacklist != None or remove_blacklist != None:
        update_preference(database, user_id, "blacklist", add_blacklist, remove_blacklist)


if __name__ == "__main__":
    pass
