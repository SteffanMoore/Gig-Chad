# Extracts the unique event id from API json object where object is json_obj["_embedded"]["events"]
def extract_id(json_object):
    id = json_object['id']

    return id


# Extracts the event name from API json object where object is json_obj["_embedded"]["events"]
def extract_event_name(json_object):
    name = json_object['name']

    return name


# Extracts the artist from API json object where object is json_obj["_embedded"]["events"]
def extract_artist(json_object):
    try:
        artist = json_object['_embedded']['attractions'][0]['name']
    except KeyError:
        artist = "N/A"

    return artist


# Extracts the genre and subgenre from API json object where object is json_obj["_embedded"]["events"]
def extract_genres(json_object):
    try:
        genre = json_object['_embedded']['attractions'][0]['classifications'][0]['genre']['name']
        subgenre = json_object['_embedded']['attractions'][0]['classifications'][0]['subGenre']['name']
    except KeyError:
        try:
            genre = json_object['classifications'][0]['genre']['name']
            subgenre = json_object['classifications'][0]['subGenre']['name']
        except KeyError:
            genre = "none"
            subgenre = "none"

    return [genre, subgenre]


# Extracts the event date from API json object where object is json_obj["_embedded"]["events"]
def extract_event_date(json_object):
    try:
        date = json_object['dates']['start']['localDate']
    except KeyError:
        date = "none"

    return date


# Extracts the price range from API json object where object is json_obj["_embedded"]["events"]
def extract_price_range(json_object):
    try:
        prices = json_object['priceRanges']
        for i in prices:
            if i['type'] == "standard including fees":
                price_range = f"£{i['min']:.2f} - £{i['max']:.2f}"
                break
    except KeyError:
        price_range = "no price"

    return price_range


# Extracts the venue from API json object where object is json_obj["_embedded"]["events"]
def extract_venue(json_object):
    try:
        venue = json_object['_embedded']['venues'][0]['name']
    except KeyError:
        venue = "none"

    return venue


# Extracts the city from API json object where object is json_obj["_embedded"]["events"]
def extract_city(json_object):
    try:
        city = json_object['_embedded']['venues'][0]['city']['name']
    except KeyError:
        city = "none"

    return city


# Extracts the postcode from API json object where object is json_obj["_embedded"]["events"]
def extract_postcode(json_object):
    try:
        postcode = json_object['_embedded']['venues'][0]['postalCode']
    except KeyError:
        postcode = "none"

    return postcode


# Extracts all relevant fields from API data when passed json_obj["_embedded"]["events"]
def extract_all(json_object):
    genres = extract_genres(json_object)
    extracted_data = {'unique_id':extract_id(json_object), 'event_name':extract_event_name(json_object),
                      'artist':extract_artist(json_object), 'genre':genres[0], 'subgenre':genres[1],
                      'event_date':extract_event_date(json_object), 'price_range':extract_price_range(json_object),
                      'venue':extract_venue(json_object), 'city':extract_city(json_object),
                      'postcode':extract_postcode(json_object)}

    return extracted_data