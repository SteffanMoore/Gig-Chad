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
    return fetch('/find_gigs', {"method":"GET", "headers":{"type":"events", "Content-Type":"application/json"}})
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
            if ((j + 1 == numberOfEvents) && (numberOfEvents % 2 != 0))
            {
                // Add row with only one event
                let event = currentEvents[j];
                let id = event['event_id'];
                let name = event['event_name'];
                let artist = event['artist'];
                let city = event['city'];
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

                let formRow = addHTML(HTMLSingleEventString);
                eventDisplayList.appendChild(formRow);
            }
            else
            {
                if (j % 2 != 0)
                {
                    // Add row with two events
                    let eventOne = currentEvents[j - 1];
                    let idOne = eventOne['event_id'];
                    let nameOne = eventOne['event_name'];
                    let artistOne = eventOne['artist'];
                    let cityOne = eventOne['city'];
                    let postcodeOne = eventOne['postcode'];
                    let priceOne = eventOne['price_range'];

                    let eventTwo = currentEvents[j];
                    let idTwo = eventTwo['event_id'];
                    let nameTwo = eventTwo['event_name'];
                    let artistTwo = eventTwo['artist'];
                    let cityTwo = eventTwo['city'];
                    let postcodeTwo = eventTwo['postcode'];
                    let priceTwo = eventTwo['price_range'];

                    let HTMLDoubleEventString = `<div class="eventRow">
                                                    <div class="event leftEvent">
                                                        <div>
                                                            <div class="eventName">${nameOne}</div>
                                                            <div class="eventInfoContainer">
                                                                <div class="eventArtistContainer">
                                                                    <div class="eventArtist">${artistOne}</div>
                                                                    <form class="addArtist" action="/find_gigs" method="post">
                                                                        <button class="addArtistButton" name="whitelist" value="${artistOne}">&#9734;</button>
                                                                    </form>
                                                                    <form class="removeArtist" action="/find_gigs" method="post">
                                                                        <button class="removeArtistButton" name="blacklist" value="${artistOne}">&#128938;</button>
                                                                    </form>
                                                                </div>
                                                                <div class="eventCity">${cityOne}</div>
                                                            </div>
                                                            <form class="eventButtonContainer" action="/find_gigs" method="post">
                                                                <div class="eventPrice">${priceOne}</div>
                                                                <button class="saveEventButton" name="save_event" value="${idOne}">Save Event</button>
                                                                <div class="eventPostcode">${postcodeOne}</div>
                                                            </form>
                                                        </div>
                                                    </div>
                                                    <div class="event rightEvent">
                                                        <div>
                                                            <div class="eventName">${nameTwo}</div>
                                                            <div class="eventInfoContainer">
                                                                <div class="eventArtistContainer">
                                                                    <div class="eventArtist">${artistTwo}</div>
                                                                    <form class="addArtist" action="/find_gigs" method="post">
                                                                        <button class="addArtistButton" name="whitelist" value="${artistTwo}">&#9734;</button>
                                                                    </form>
                                                                    <form class="removeArtist" action="/find_gigs" method="post">
                                                                        <button class="removeArtistButton" name="blacklist" value="${artistTwo}">&#128938;</button>
                                                                    </form>
                                                                </div>
                                                                <div class="eventCity">${cityTwo}</div>
                                                            </div>
                                                            <form class="eventButtonContainer" action="/find_gigs" method="post">
                                                                <div class="eventPrice">${priceTwo}</div>
                                                                <button class="saveEventButton" name="save_event" value="${idTwo}">Save Event</button>
                                                                <div class="eventPostcode">${postcodeTwo}</div>
                                                            </form>
                                                        </div>
                                                    </div>
                                                </div>`;

                    let formRow = addHTML(HTMLDoubleEventString);
                    eventDisplayList.appendChild(formRow);
                }
            }
        }

    }
}

populateEvents();