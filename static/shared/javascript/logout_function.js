let logoutMenu = document.querySelector(".menu");
let logoutButton = document.querySelector(".logoutButton");
let title = document.querySelector(".appTitle");

function animationPause()
{
    setTimeout(function(){
        window.location.href = '/logout';
    }, 3000);
}

function appLogout()
{
    logoutMenu.style.height = "130vh";
    logoutMenu.style.width = "130vw";
    logoutButton.style.transform = "translateY(110vh)";
    title.style.transform = "translateY(40vh)";
    title.style.fontSize = "7vw";
    animationPause();
}