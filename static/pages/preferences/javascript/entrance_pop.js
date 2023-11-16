let pageTitle = document.querySelector(".preferencesTitle");
let formContainer = document.querySelector(".preferenceContainer");

function showTitlePause()
{
    setTimeout(function(){
        pageTitle.style.fontSize = "3vw";
        pageTitle.style.transform = "translateY(-15vh) translateX(-30vw)";
        formContainer.style.transform = "translateY(-65vh)";
    }, 1000);
}


function enterPage()
{
    showTitlePause();
}

enterPage();