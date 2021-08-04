const sign_in_btn = document.querySelector("#sign-in-btn");
const sign_up_btn = document.querySelector("#sign-up-btn");
const container = document.querySelector(".container");

sign_up_btn.addEventListener("click", () => {
  container.classList.add("sign-up-mode");
});

sign_in_btn.addEventListener("click", () => {
  container.classList.remove("sign-up-mode");
});


function toggleShowResetPassword() {
  const UserPassword = document.getElementById("update_password");
  if (UserPassword.type === "password") {
    UserPassword.type = "text";
  } else {
    UserPassword.type = "password";
  }
}

function toggleShowNewPassword() {
  const UserPassword = document.getElementById("new_password");
  if (UserPassword.type === "password") {
    UserPassword.type = "text";
  } else {
    UserPassword.type = "password";
  }
}


const rmCheck = document.getElementById("rememberMe"),
usernameInput = document.getElementById("user_username");

if (localStorage.checkbox && localStorage.checkbox !== "") {
rmCheck.setAttribute("checked", "checked");
usernameInput.value = localStorage.username;
} else {
rmCheck.removeAttribute("checked");
usernameInput.value = "";
}

function lsRememberMe() {
if (rmCheck.checked && usernameInput.value !== "") {
localStorage.username = usernameInput.value;
localStorage.checkbox = rmCheck.value;
} else {
localStorage.username = "";
localStorage.checkbox = "";
}
}

$(document).on('click', '.toggle-password', function() {

  $(this).toggleClass("fa-eye fa-eye-slash");
  
  var input = $("#password");
  input.attr('type') === 'password' ? input.attr('type','text') : input.attr('type','password')
});

$(document).on('click', '.toggle-confirm-password', function() {

  $(this).toggleClass("fa-eye fa-eye-slash");
  
  var input = $("#confirm_password");
  input.attr('type') === 'password' ? input.attr('type','text') : input.attr('type','password')
});

$(document).on('click', '.toggle-user-password', function() {

  $(this).toggleClass("fa-eye fa-eye-slash");
  
  var input = $("#user_password");
  input.attr('type') === 'password' ? input.attr('type','text') : input.attr('type','password')
});

$(document).ready(function() {
  $('.carousel').carousel({interval: 7000});
});