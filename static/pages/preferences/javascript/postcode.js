let postcodeForm = document.querySelector(".postcodeForm");
let postcodeAlert = document.querySelector(".postcodeAlert");
let textInput = document.querySelector(".textInput");

// Returns alert back to size zero after time has passed
function allClear()
{
    setTimeout(function(){
        postcodeAlert.style.transform = "scale(0)";
    }, 1100)
}


// Expands the "Invalid" postcode alert before returning it back to normal
function triggerAlert()
{
    postcodeAlert.style.transform = "scale(1)";
    allClear();
}


function failureAlert()
{
    postcodeAlert.innerHTML = "Invalid";
    triggerAlert();
}


function successAlert()
{
    postcodeAlert.innerHTML = "Updated";
    triggerAlert();
}


// Listens to the postcode form an intercepts the submit to make a custom request
postcodeForm.addEventListener("submit", function(event) {
    event.preventDefault();
    var postcodeChange = new XMLHttpRequest();
    postcodeChange.open('POST', '/preferences', true);
    postcodeChange.onreadystatechange = function() {
        if (postcodeChange.readyState === 4 && postcodeChange.status === 200)
        {
            // Failure alert triggered if postcode not recognised
            if (postcodeChange.response == "failure")
            {
                failureAlert()
            }
            // Success alert triggered otherwise and placeholder is changed to new postcode
            else
            {
                textInput.placeholder = postcodeChange.response;
                textInput.value = "";
                successAlert();
            }
        }
    };
    postcodeChange.send(new FormData(postcodeForm));
});
