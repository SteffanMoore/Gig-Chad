let pageTitle = document.querySelector(".pageTitle");
let eventList = document.querySelector(".eventList");

function showTitlePause()
{
    setTimeout(function(){
        pageTitle.style.fontSize = "3vw";
        pageTitle.style.transform = "translateY(-9vh)";
        eventList.style.transform = "translateY(-70vh)";
    }, 1000);
}

function enterPage()
{
    showTitlePause();
}

enterPage();
