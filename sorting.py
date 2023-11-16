from datetime import datetime, timedelta

def find_datetime(input_date):
    """ Returns datetime date for string date formatted as YYYY-MM-DD """

    datetime_date = datetime.strptime(input_date, "%Y-%m-%d")

    return datetime_date


def get_date_string(datetime_date):
    """ Returns the written date formatted for the website """
    day = int(datetime_date.strftime("%d"))

    if day in [1, 21, 31]:
        suffix = "st"
    elif day in [2, 22]:
        suffix = "nd"
    elif day in [3, 23]:
        suffix = "rd"
    else:
        suffix = "th"

    # Adds the suffix to the longform date
    formatted_date = datetime_date.strftime(f"%-d{suffix} %B %Y")

    return formatted_date


def find_date_index(event_date, date_list):
    """ Inserts datetime into an ascending position in the list """

    length = len(date_list)

    # Runs through date list to compare magnitude
    for index in range(length):
        if event_date > date_list[length - (index + 1)]:
            date_list.insert(length - index, event_date)
            return

    date_list.insert(0, event_date)
    return


def sort_dates(event_list):
    """ Returns a dictionary of events ordered by date """

    date_list, event_date_dict = [], {}

    # Initially goes through all events and adds them to a dictionary and ordering their dates in a list
    for event in event_list:
        event_date = find_datetime(event['date'])

        if event_date in event_date_dict:
            event_date_dict[event_date].append(event)
        else:
            event_date_dict[event_date] = [event]
            find_date_index(event_date, date_list)

    # Creates a new date ordered dictionary under which all events are stored
    final_event_dictionary = {}
    for index, date in enumerate(date_list):
        final_event_dictionary[index] = {get_date_string(date): event_date_dict[date]}

    return final_event_dictionary

