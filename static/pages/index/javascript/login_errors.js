
let loginForm = document.querySelector(".loginInfo")
let registerForm = document.querySelector(".registerInfo")
let loginAlertBox = document.querySelector(".loginFlash")
let registerAlertBox = document.querySelector(".registerFlash")

function resetLoginFlash()
{
    setTimeout(function(){
        loginAlertBox.style.fontSize = "0vw";
    }, 1750)
}

function resetRegFlash()
{
    setTimeout(function(){
        registerAlertBox.style.fontSize = "0vw";
    }, 1750)
}


loginForm.addEventListener("submit", function(event) {
    event.preventDefault();
    var loginRequest = new XMLHttpRequest();
    loginRequest.open('POST', '/', true);
    loginRequest.onreadystatechange = function() {
        if (loginRequest.readyState === 4 && loginRequest.status === 200)
        {
            loginAlertBox.textContent = loginRequest.response;
            loginAlertBox.style.fontSize = "1.5vw";
            resetLoginFlash();
        }
        else
        {
            if (loginRequest.readyState === 4 && loginRequest.status === 302)
            {
                window.location.href = '/home';
            }
        }
    };
    loginRequest.send(new FormData(loginForm));
});


registerForm.addEventListener("submit", function(event) {
    event.preventDefault();
    var regRequest = new XMLHttpRequest();
    regRequest.open('POST', '/', true);
    regRequest.onreadystatechange = function() {
        if (regRequest.readyState === 4 && regRequest.status === 200)
        {
            registerAlertBox.textContent = regRequest.response;
            registerAlertBox.style.fontSize = "1.5vw";
            resetRegFlash();
        }
        else
        {
            if (regRequest.readyState === 4 && regRequest.status === 302)
            {
                window.location.href = '/home';
            }
        }
    };
    regRequest.send(new FormData(registerForm));
});
