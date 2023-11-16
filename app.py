from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from login import login_required
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
import time
from ticketmaster import update_event_db, retrieve_server_update
from user_preferences import check_pref_exist, create_pref_entry, update_postcode, retrieve_genres, update_user_preferences, retrieve_postcode, retrieve_column
from distances import find_towns_in_radius
from sorting import sort_dates


# Updates the database with the ticketmaster API
update_event_db(100, 5)

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///gigchad_db.db")

#######################################################################
#                              Functions
#######################################################################

#populate_event_db(days=100, time_width=5)


#######################################################################
#                           APP PAGES
#######################################################################

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/", methods=["GET", "POST"])
def signed_out_home():
    """Home page when not logged in"""
    if session.get("user_id") is not None:
        return redirect("/home")
    elif request.method == "POST":
        form_name = request.form["formName"]

        # Handles data input from the login form
        if "loginInfo" in form_name:
            print("Login")

            # Ensures no form input remains blank
            if not request.form.get("username"):
                print("No username")
                return ("Enter your username to sign in", 200)
            elif not request.form.get("password"):
                print("No password")
                return ('Enter your password to sign in', 200)

            # Searches database and rejects user if incorrect username or password used
            user_search = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
            if len(user_search) != 1 or not check_password_hash(user_search[0]["password_hash"], request.form.get("password")):
                print("Incorrect username or password")
                return ('Your username or password is incorrect', 200)

            # Remember user identity by using a session
            session["user_id"] = user_search[0]["id"]
            return ("/home", 302)

        # Handles data input from the registration form
        elif "registerInfo" in form_name:
            print("Register")

            # Ensures no form input remains blank
            if not request.form.get("username"):
                print("No username")
                return ('Enter a username to register', 200)
            elif not request.form.get("password1"):
                print("Enter a password to register")
                return ('Enter a password to register', 200)
            elif not request.form.get("password2"):
                print("No password re-renter")
                return ('Enter the same password twice to confirm', 200)

            # Checks that the password confirmation matches the initially given password
            if request.form.get("password1") != request.form.get("password2"):
                print("Password and confirmation don't match")
                return ("Entered passwords don't match", 200)

            # Checks database for existing username and, if not found, inserts new user
            try:
                db.execute("INSERT INTO users (username, password_hash) VALUES(?, ?)", request.form.get("username"), generate_password_hash(request.form.get("password1")))
                print("New user created")

                # Remember user identity by using a session
                user_search = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
                session["user_id"] = user_search[0]["id"]

                return ("/home", 302)

            except ValueError:
                print("Username is already taken")
                return ('The entered username is already taken', 200)

        # Slips through the cracks on the POST method
        else:
            print("Nothing")
            return ('', 204)
    else:
        return (render_template("index.html"))


@app.route("/home", methods=["GET", "POST"])
@login_required
def home():
    if request.method == "POST":
        if "preferences" in request.form:
            return redirect("/preferences")
        elif "find gigs" in request.form:
            return redirect("/find_gigs")
        elif "upcoming" in request.form:
            print("well it takes the right path")
            return redirect("/upcoming")
    return render_template("home.html")


@app.route("/preferences", methods=["GET", "POST"])
@login_required
def preferences():
    # Checks that a preference entry already exists for this user and creates one if not
    if check_pref_exist(db, session.get("user_id")) == False:
        create_pref_entry(db, session.get("user_id"))

    if request.method == "GET":
        if request.headers.get("type") == "genre":
            return jsonify(retrieve_genres(db, session.get("user_id")))
        elif request.headers.get("type") == "favourite":
            return jsonify(retrieve_column(db, session.get("user_id"), 'whitelist'))
        elif request.headers.get("type") == "hidden":
            return jsonify(retrieve_column(db, session.get("user_id"), 'blacklist'))
    elif request.method == "POST":
        form_name = request.form["formName"]

        # Handles user updating their genre preferences
        if "genrePreferences" in form_name:
            favourite_genres = []
            city_list, genre_list = retrieve_server_update(db)

            for genre, presence in request.form.items():
                if presence == "on":
                    favourite_genres.append(genre)

            for genre in favourite_genres:
                if genre in genre_list:
                    genre_list.remove(genre)

            update_user_preferences(db, session.get("user_id"), add_genres=favourite_genres, remove_genres=genre_list)

        elif "favArtistPreferences" in form_name:
            remove_favourites = retrieve_column(db, session.get("user_id"), 'whitelist')
            for artist, presence in request.form.items():
                if presence == "on":
                    remove_favourites.remove(artist)

            update_user_preferences(db, session.get("user_id"), remove_whitelist=remove_favourites)

        elif "hiddenArtistPreferences" in form_name:
            remove_hidden = retrieve_column(db, session.get("user_id"), 'blacklist')
            for artist, presence in request.form.items():
                if presence == "on":
                    remove_hidden.remove(artist)

            update_user_preferences(db, session.get("user_id"), remove_blacklist=remove_hidden)

        elif "postcode" in form_name:
            input_postcode = request.form.get("postcode")
            if update_postcode(db, session.get("user_id"), input_postcode) == True:
                return (input_postcode, 200)
            else:
                return("failure", 200)

        return render_template("preferences.html")
    else:
        return render_template("preferences.html")
    return render_template("preferences.html")


@app.route("/find_gigs", methods=["GET", "POST"])
@login_required
def find_gigs():
    if check_pref_exist(db, session.get("user_id")) == False:
        return redirect("/preferences")

    user_postcode = retrieve_postcode(db, session.get("user_id"))

    if user_postcode != False:
        # User preference criteria used for search
        places_in_range = find_towns_in_radius(user_postcode, db, 50)
        user_genres = retrieve_column(db, session.get("user_id"), "genres")
        user_whitelist = retrieve_column(db, session.get("user_id"), "whitelist")
        user_blacklist = retrieve_column(db, session.get("user_id"), "blacklist")

        search_result = db.execute("""SELECT * FROM events WHERE ((city in (?) AND (genre in (?) OR subgenre in (?))) AND artist NOT IN (?)) OR artist in (?)""", places_in_range, user_genres, user_genres, user_blacklist, user_whitelist)
        sorted_results = sort_dates(search_result)
    else:
        sorted_results = False

    if request.method == "GET":
        if request.headers.get("type") == "events":
            return jsonify(sorted_results)
    elif request.method == "POST":
        if "save_event" in request.form:
            event_id = request.form["save_event"]
            update_user_preferences(db, session.get("user_id"), add_events=[event_id])
            return ('', 204)
        elif "whitelist" in request.form:
            whitelist_artist = request.form["whitelist"]
            update_user_preferences(db, session.get("user_id"), add_whitelist=[whitelist_artist])
            return redirect("/find_gigs")
        elif "blacklist" in request.form:
            print("we're here")
            blacklist_artist = request.form["blacklist"]
            update_user_preferences(db, session.get("user_id"), remove_whitelist=[blacklist_artist], add_blacklist=[blacklist_artist])
            return redirect("/find_gigs")

    return render_template("find_gigs.html")


@app.route("/upcoming", methods=["GET", "POST"])
@login_required
def upcoming():
    if check_pref_exist(db, session.get("user_id")) == False:
        return redirect("/preferences")

    user_postcode = retrieve_postcode(db, session.get("user_id"))

    if user_postcode != False:
        saved_events = retrieve_column(db, session.get("user_id"), "saved_events")
        search_result = db.execute("""SELECT * FROM events WHERE (event_id in (?))""", saved_events)
        sorted_results = sort_dates(search_result)
    else:
        sorted_results = False

    if request.method == "GET":
        if request.headers.get("type") == "events":
            return jsonify(sorted_results)
    elif request.method == "POST":
        if "discard_event" in request.form:
            event_id = request.form["discard_event"]
            update_user_preferences(db, session.get("user_id"), remove_events=[event_id])
            return redirect("/upcoming")

    return render_template("upcoming.html")

