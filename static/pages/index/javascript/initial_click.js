let intialButtons = document.querySelector('#initialButtons');
let title = document.querySelector('.mainTitle');
let mainTextHolder = document.querySelector('.columnContainer');
let menuOverlay = document.querySelector('.menuBackground');
let menuContainer = document.querySelector(".menuSwapper");

function swapToRegister()
{
    menuContainer.style.transform = "translateX(-50%)";
}

function swapToLogin()
{
    menuContainer.style.transform = "translateX(0)";
}

function moveButtonsDown()
{
    mainTextHolder.style.pointerEvents = "none";
    initialButtons.style.paddingTop = '45vh';
    title.style.paddingTop = '5vh';
    menuOverlay.style.transform = "translateY(0%)";
}

/*
function moveMenuDown()
{
    backLeft1.animate(
        [
            {transform: "rotate(27deg) translateY(-50vh)",},
        ],
        {
            duration: 1000,
            iterations: 1,
        },
    );
}
*/

function openLoginMenu()
{
    moveButtonsDown();
}

function openRegisterMenu()
{
    swapToRegister();
    moveButtonsDown();
}