# Gig Chad
The aim of this project was to develop a web-based application to display music-based events near a user which could be filtered by a users preferences. To do this, I enlisted the help of the TicketMaster API to retrieve all music events in the UK (sorry to those outside the UK but this only works for within the UK), put them into a SQL database and, based on user inputted postcode and genre choices, filter entered events to those relevant to the user. The easiest way for me to describe the project in any detail is, in my view, to go through it page by page as the user would see it. So without further ado...

## Startup
Although not a page itself, the start-up process is worth mentioning as its own section (even though a standard "user" wouldn't encounter it). Currently, I am just running the app on the Flask development server so a simple "flask run" in the terminal is sufficient to get everything kicked off. When run, the app immediately checks whether it needs to update its data (it is set to update once per day). It does this by accessing the SQLite database "gigchad_db.db" and checking the server_updates table to see when the most recent update occured. If it was within the last 24 hours, it simply moves on. On the other hand, if it has been over 24 hours, the update procedure (in ticketmaster.py) runs - this is comprised of three steps: retrieving new events, deleting old events and finding city location info.

New events are retrieved by making requests through the ticketmaster API (the free API key permits 10,000 requests per day although it is throttled) - each request returns 200 events, allowing for a large time span to be searched for event with the non-partner API (I have opted to only return gigs from up to 100 days in the future). The update then attempts to insert each event into the "events" table in the database but, since the event_id field has the "UNIQUE" flag in the table, trying to insert the same event twice raises a value error, preventing duplicates.

Deleting old events is relatively straightforward - for all events, it checks whether the event date is in the past and, if it is, deletes it.

The final update step is the city location retrieval which is a matter of convenience (this used to occur when opening the "find gigs" page but simply took too long from a user perspective). This searches the database for all cities in the events table and finds their longitude and latitude using the postcodes.io API. Since multiple towns can be named the same thing, it chooses the largest settlement in the list of returned places. After this, it tries to insert the city (with its respective location information) into the cities table in the database.

After this, the update is complete, and the flask app runs.

## Index

Log in             |
:-------------------------:|
<img src="/readme_pics/Login.gif" />  |


The first page any new user would be welcomed with is the index page using the "/" route. This functions as both the login page and the registration page with any user who isn't logged in being rediected here (the log in system has been recycled from the "Finance" CS50 project). The initial two "register" and "sign in" buttons both trigger JavaScript functions on click to lower a div containing the two "sign in" and "register" forms. Only one of these forms is displayed at a time through the div but they can be swapped between using a button underneath each form which simply shifts displaces the form container left or right. All of the animation is handled by CSS transitions so that it changes made in JavaScript appear smooth.

The login/registration forms themselves are quite simple - in the "/" route, handles both of them when the POST request method is used. A hidden input in each form is used to determine which form was posted and then the form is checked to ensure the correct details have been entered to sign up or log in. For log in, it's a case of attempting to retrieve the user's account information from the database and, if a discrepancy is found, blocking the log in. For registration, the database must first be checked for accounts using the same name as the user input before creating a new entry in the "users" table if none are found. For both forms, if an error in the form is detected, a 200 status code is returned with an error string (200 was chosen so that the page wouldn't reload). The post request is processed by a JavaScript function in "login_errors.js", which flashes an error message on the screen when a 200 response is received from the form submit. If nothing goes wrong, the log in process returns a 302 repsonse and the user is redirected to "/home".

## Home
The homepage is a very simple page which boils down to a banner menu at the top and three buttons underneath to redirect the user to their respective pages. The diagonal divide of the central button was achieved by superimposing it over the other two buttons and then using the CSS clip-path polygon technique. Each button has a dark filter overlay with letters cut out to display the title - on hover, the filter div fades away, making the button section appear brighter.

Log out from home             |
:-------------------------:|
<img src="/readme_pics/Logout.gif" />  |

#### The menu
The menu at the top of the home page is present on all of the Gig Chad pages other than the index. The HTML of this is in the "menu.html" file which all of the pages featuring the menu extend. The two buttons on the menu merely redirect the user to other routes in "app.py" - the "Gig Chad" button takes the user to the home page (making it the key navigational button throughout the app) and the "Log Out" button simply redirects the user to the "/logout" route which clears the user session.

## Preferences
The preferences page is the next page which the user will encounter (both the "upcoming" and "find gigs" pages redirect to preferences if the user doesn't have a preference entry in the database). On entry to the page, if the user doesn't have a preference entry in the database, a new one is created. Here the user can enter a postcode (so that events are relevant to their local area), select genres they want to see in the search results and remove artists from their favourites and hidden lists. On loading the page, the "entrance_pop.js" JavaScript script is run to add some animation.

Accessing preferences from home             |
:-------------------------:|
<img src="/readme_pics/Preferences.gif" />  |

#### Postcode update
The update poscode section is a simple form submit which posts an input postcode to the "/preferences" route. Once recieved, the entered text is passed to an update function. This uses the aforementioned postcode API to check whether the entered postcode is valid - if it is, it updates the user preference in the database to the input postcode and returns true. If it isn't valid, it returns false. Depending on this return value, a status 200 response will be sent with either a "failure" message or the accepted postcode (which is then set as the placeholder for the text input). A div above the postcode title the flashes either "invalid" or "updated" depending on failure or success.

#### Genre selection
On clicking the "my genres" button, the genres forms scale is adjusted from 0 to 1, allowing it to zoom into existence (this is also how the other forms have their zoom effect). Clicking the button also populates the form. It does this by first deleting all rows in all of the forms on page to ensure that there are no duplicate genre entries. It then sends a fetch request to the server which returns a dictionary of all genres and whether they are a preference of the user (all genre preferences for a user are saved as a string under the preferences table in the database). On receiving this, the client creates a HTML fragment which will be inserted into the genre form and adds all genres stored in the database to it as individual items with tickboxes. Those which are already user preferences are automatically ticked. The user can then tick and untick preferences depending on personal taste to their hearts content before submitting the form using the save button. This will post it to the server which will run through which genres are ticked and which aren't, adding any ticked items to the users entry in the preference table.

#### Favourites/hidden
The final two options on the preferences page are very much similar to each other in function - the favouites column shows any artist which the user has selected to be a favourite while the hidden column shows artist which the user wants to hide. They both work similarly to the genre form although a bit more simply - data only need to be found from the user preferences and then returned. Any artists which are unticked by the user when the form is submitted will be removed from either the users list of favourites or hidden artists.

## Find gigs
The find gigs page is used to display search results found as a result of the preferences entered by the user. Events can then be saved for future reference and artists can be saved as favourites or hidden if the user doesn't want to see them.

Accessing find gigs from home             |
:-------------------------:|
<img src="/readme_pics/Find gigs.gif" />  |

#### Initial search
On loading the "find_gigs" page, the server immediately ensures that the user has a preference table entry. Once confirmed, the server fetches from the database all cities near to the user, as well as the whitelisted and blacklisted artists (referred to earlier as favourite and hidden) and the genre preferences of the user. A SQL search based on these criteria is then carried to return a list of events. This is then sorted into a dictionary, the key being the date and the value being a list of events taking place on that date (this had to be nested within another dictionary to prevent the loss of order so now looks more like dict = {index : {date : [list of events]}}).

After this search has been carried out, the client sends a fetch request to the server which responds by sending the search result in JSON form. The client, on receival, goes through the events and, for each date, adds a date div to display event date before adding an event card for every event (in a similar fashion to the genre selection form). Each of these cards displays information about the gig and artist as well as containing several buttons: one to add to add artist to favourites; one to add artist to hidden list and one to save the event.

##### Finding close cities
The other search conditions are quite easy to find as they are already stored within the database. However, finding cities close to the user postcode is more difficult. First, the user postcode is entered into the postcode API to find its longitude and latitude. Once this is complete, the haversine formula is used to compare the distances between the postcode and the postcodes of all the cities in the database. If they are under 50 miles away, they are accepted. A list of the accepted cities within the radius is returned.

#### Event display
Now that all of the events have been added to the page, the user can scroll through the container div to find any event which they take a shine to. They can then click the save button on the event which posts the unique id value of the event to the server, allowing it to add this value to the list of the users saved events in the preferences table. This is similar to the functionality of the "add to favourites" and "add to hidden" buttons only they use artist as the identifyer. When added to the favourite or hidden list, the page will refresh as the search re-runs. This is so that any events (even outside the search radius) for a favourite artist will be included in the results and so that no events of a hidden artist are displayed.

## Upcoming
The "upcoming" page works near identically to the "find_gigs" page. On page load, events which are saved in a users preferences are searched for in the events table and returned from the database before being sorted in the same manner as the "find_gigs" page events. They are then displayed in the same way, albeit in a single column. The only additions are some extra event detail on the event card and a "Discard Event" button which removes the selected event from the users saved events.

Accessing upcoming from home             |
:-------------------------:|
<img src="/readme_pics/Upcoming.gif" />  |
