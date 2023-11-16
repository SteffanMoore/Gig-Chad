// Creates an HTML fragment to be added to an HTML document
function addHTML(string)
{
    let newHTML = document.createDocumentFragment();
    let newDiv = document.createElement('div');
    newDiv.innerHTML = string;

    while (newDiv.firstChild)
    {
        newHTML.appendChild(newDiv.firstChild);
    }

    return newHTML;
}


// Fetches events to display on the find gigs page
function fetchEvents()
{
    return fetch('/upcoming', {"method":"GET", "headers":{"type":"events", "Content-Type":"application/json"}})
        .then(response => response.json())
        .then(data => {
            console.log(data);
            return(data);
        })
}


async function populateEvents()
{
    let eventDisplayList = document.querySelector(".scrollContent");
    let eventData = await fetchEvents();
    let eventDates = Object.keys(eventData);

    for (let i = 0; i < eventDates.length; i++)
    {
        let currentDate = Object.keys(eventData[eventDates[i]])[0];
        let currentEvents = eventData[eventDates[i]][currentDate];

        // Add current date div to page
        HTMLDateString = `<div class="dateSpacer">${currentDate}</div>`;

        let formRow = addHTML(HTMLDateString);
        eventDisplayList.appendChild(formRow);

        let numberOfEvents = currentEvents.length;
        for (let j = 0; j < numberOfEvents; j++)
        {
            // Add row with only one event
            let event = currentEvents[j];
            let id = event['event_id'];
            let name = event['event_name'];
            let artist = event['artist'];
            let venue = event['venue'];
            let city = event['city'];
            let genre = event['genre'];
            let subgenre = event['subgenre'];
            let postcode = event['postcode'];
            let price = event['price_range'];

            let HTMLSingleEventString = `<div class="eventRow">
                                            <div class="event leftEvent">
                                                <div>
                                                <div class="eventName">${name}</div>
                                                    <div class="eventInfoContainer">
                                                        <div class="eventArtistContainer">
                                                            <div class="eventArtist">${artist}</div>
                                                            <form class="addArtist" action="/find_gigs" method="post">
                                                                <button class="addArtistButton" name="whitelist" value="${artist}">&#9734;</button>
                                                            </form>
                                                            <form class="removeArtist" action="/find_gigs" method="post">
                                                                <button class="removeArtistButton" name="blacklist" value="${artist}">&#128938;</button>
                                                            </form>
                                                        </div>
                                                        <div class="eventCity">${city}</div>
                                                    </div>
                                                    <form class="eventButtonContainer" action="/find_gigs" method="post">
                                                        <div class="eventPrice">${price}</div>
                                                        <button class="saveEventButton" name="save_event" value="${id}">Save Event</button>
                                                        <div class="eventPostcode">${postcode}</div>
                                                    </form>
                                                </div>
                                            </div>
                                        </div>`;

            let HTMLEventString = `<div class="eventRow">
                                    <div class="event">
                                        <div>
                                            <div class="eventName">${name}</div>
                                            <div class="eventInfoContainer">
                                                <div class="eventArtistContainer">
                                                    <div class="eventArtist">${artist}</div>
                                                    <form class="addArtist" action="/upcoming" method="post">
                                                        <button class="addArtistButton" name="whitelist" value="insert_artist_name">&#9734;</button>
                                                    </form>
                                                </div>
                                                <div class="eventGenresContainer">
                                                    <div class="eventGenres">${genre}</div>
                                                    <div class="eventGenres">${subgenre}</div>
                                                </div>
                                                <div class="eventPrice">${price}</div>
                                                <div class="eventLocation">
                                                    <div class="eventLocationDetails">${venue}</div>
                                                    <div class="eventLocationDetails">${city}</div>
                                                    <div class="eventLocationDetails">${postcode}</div>
                                                </div>
                                            </div>
                                            <form class="eventButtonContainer" action="/upcoming" method="post">
                                                <button class="discardEventButton" name="discard_event" value="${id}">Discard Event</button>
                                            </form>
                                        </div>
                                    </div>
                                </div>`;

            let formRow = addHTML(HTMLEventString);
            eventDisplayList.appendChild(formRow);
        }

    }
}

populateEvents();