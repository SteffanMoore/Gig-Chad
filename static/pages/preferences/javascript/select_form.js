let genreMenu = document.querySelector("#genreFormBackground");
let favouriteMenu = document.querySelector("#favouriteFormBackground");
let hiddenMenu = document.querySelector("#hiddenFormBackground");


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


// Fetch request to get a dictionary of genres which are prefered and not prefered
function fetchGenres()
{
    return fetch('/preferences', {"method":"GET", "headers":{"type":"genre", "Content-Type":"application/json"}})
        .then(response => response.json())
        .then(data => {
            console.log(data);
            return(data);
        })
}


// Fetch request to get a list of favourite artists
function fetchFavourites()
{
    return fetch('/preferences', {"method":"GET", "headers":{"type":"favourite", "Content-Type":"application/json"}})
        .then(response => response.json())
        .then(data => {
            console.log(data);
            return(data);
        })
}


// Fetch request to get a list of artists the user has chosen to hide
function fetchHidden()
{
    return fetch('/preferences', {"method":"GET", "headers":{"type":"hidden", "Content-Type":"application/json"}})
        .then(response => response.json())
        .then(data => {
            console.log(data);
            return(data);
        })
}


// Uses the genre fetch request and then updates the genre form with the data
async function getGenres()
{
    let allRows = document.querySelectorAll(".formRow");
    let genreForm = document.querySelector("#genreForm");

    // Delete all rows currently displayed
    for (let deleteIndex = 0; deleteIndex < allRows.length; deleteIndex++)
    {
        allRows[deleteIndex].remove();
    }

    // Waits for the data to be retrieved before continuing
    let genreData = await fetchGenres();
    let genreNames = Object.keys(genreData);
    let genreNo = genreNames.length;

    // Runs through genres and adds them into the HTML genre form
    for (let keyIndex = 0; keyIndex < genreNo; keyIndex++)
    {
        console.log(genreNames[keyIndex]);
        if ((genreNo - 1 == keyIndex) && (genreNo % 2 != 0))
        {
            let HTMLStringList = [`<div class="formRow"><div class="formItem"><div class="genreName">${genreNames[keyIndex]}</div>`];

            // Determines whether to create a ticked or unticked checkbox depending on user preference
            if (genreData[genreNames[keyIndex - 1]] == 1)
            {
                newCheckbox = `<input type="checkbox" checked="checked" name="${genreNames[keyIndex]}"></div></div>`;
            }
            else
            {
                newCheckbox = `<input type="checkbox" name="${genreNames[keyIndex]}"></div></div>`;
            }

            HTMLStringList[1] = newCheckbox;

            // Converts HTML list into a string and creates a fragment with it to append the document
            let formRow = addHTML(HTMLStringList.join(``));
            genreForm.appendChild(formRow);
        }
        else
        {
            // On every even index two genres are added to the HTML form
            if (keyIndex % 2 != 0)
            {
                // Sets up the beginning bit of the new HTML string
                let HTMLStringList = [`<div class="formRow"><div class="formItem"><div class="genreName">${genreNames[keyIndex - 1]}</div>`];
                let firstCheckbox = ``;
                let secondCheckbox = ``;

                // Determines whether to create a ticked or unticked checkbox depending on user preference
                if (genreData[genreNames[keyIndex - 1]] == 1)
                {
                    firstCheckbox = `<input type="checkbox" name="${genreNames[keyIndex - 1]}" checked="checked">`;
                }
                else
                {
                    firstCheckbox = `<input type="checkbox" name="${genreNames[keyIndex - 1]}">`;
                }

                // Adds the HTML for the first genre item to the list
                HTMLStringList[1] = firstCheckbox;
                HTMLStringList[2] = `</div><div class="formItem"><div class="genreName">${genreNames[keyIndex]}</div>`;

                // Creates ticked/unticked box for the second genre
                if (genreData[genreNames[keyIndex]] == 1)
                {
                    secondCheckbox = `<input type="checkbox" name="${genreNames[keyIndex]}" checked="checked"></div></div>`;
                }
                else
                {
                    secondCheckbox = `<input type="checkbox" name="${genreNames[keyIndex]}"></div></div>`;
                }

                // Adds HTML for the second checkbox to the list
                HTMLStringList[3] = secondCheckbox;

                // Converts HTML list into a string and creates a fragment with it to append the document
                let formRow = addHTML(HTMLStringList.join(``));
                genreForm.appendChild(formRow);
            }
        }
    }
}


// Uses the favourite fetch request and then updates the favourite form with the data
async function getFavourites()
{
    let allRows = document.querySelectorAll(".formRow");
    let favouritesForm = document.querySelector("#favArtistForm");

    // Delete all rows currently displayed
    for (let deleteIndex = 0; deleteIndex < allRows.length; deleteIndex++)
    {
        allRows[deleteIndex].remove();
    }

    // Waits for the data to be retrieved before continuing
    let favouriteData = await fetchFavourites();
    let favouriteNo = favouriteData.length;

    for (let i = 0; i < favouriteNo; i++)
    {
        if (favouriteData[i] != "")
        {
            let newFavouriteRow = `<div class="formRow">
                                        <div class="formItem singleItemRow">
                                            <div class="artistName">${favouriteData[i]}</div>
                                            <input type="checkbox" name="${favouriteData[i]}" checked="checked">
                                        </div>
                                    </div>`;

            favouritesForm.appendChild(addHTML(newFavouriteRow));
        }
    }
}


// Uses the favourite fetch request and then updates the favourite form with the data
async function getHidden()
{
    let allRows = document.querySelectorAll(".formRow");
    let hiddenForm = document.querySelector("#hiddenForm");

    // Delete all rows currently displayed
    for (let deleteIndex = 0; deleteIndex < allRows.length; deleteIndex++)
    {
        allRows[deleteIndex].remove();
    }

    // Waits for the data to be retrieved before continuing
    let hiddenData = await fetchHidden();
    let hiddenNo = hiddenData.length;

    for (let i = 0; i < hiddenNo; i++)
    {
        if (hiddenData[i] != "")
        {
            let newHiddenRow = `<div class="formRow">
                                        <div class="formItem singleItemRow">
                                            <div class="artistName">${hiddenData[i]}</div>
                                            <input type="checkbox" name="${hiddenData[i]}" checked="checked">
                                        </div>
                                    </div>`;

            hiddenForm.appendChild(addHTML(newHiddenRow));
        }
    }
}


function waitForClose(menuOpen)
{
    if (open == false)
    {
        menuOpen.style.transform = "scale(1)";
    }
    else
    {
        setTimeout(function(){
            menuOpen.style.transform = "scale(1)";
        }, 500);
    }
}

function showGenre()
{
    getGenres();
    favouriteMenu.style.transform = "scale(0)";
    hiddenMenu.style.transform = "scale(0)";
    waitForClose(genreMenu);
    open = true;
}


function showFavourite()
{
    getFavourites();
    hiddenMenu.style.transform = "scale(0)";
    genreMenu.style.transform = "scale(0)";
    waitForClose(favouriteMenu);
    open = true;
}


function showHidden()
{
    getHidden();
    genreMenu.style.transform = "scale(0)";
    favouriteMenu.style.transform = "scale(0)";
    waitForClose(hiddenMenu);
    open = true;
}

let open = false;