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

$('#homepage-login-form').on('submit', function() {

  if ($('#rememberMe').is(':checked')) {
      // save username and password
      localStorage.userName = $('#user_username').val();
      localStorage.password = $('#user_password').val();
      localStorage.checkBoxValidation = $('#rememberMe').val();
  } else {
      localStorage.userName = '';
      localStorage.password = '';
      localStorage.checkBoxValidation = '';
  }

  //Other form functions
});

function submit()
{
   var username = document.getElementById("user_username").value;
   localStorage.setItem( "username", username );
   return false;
}

window.onload = function()
{
   document.getElementById( "user_username" ).value = localStorage.getItem( "username" );
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