function login() {
  const username = $("#username").val();
  const password = $("#password").val();

  if (!username || !password) {
    $("#message")
      .text("Please enter both username and password")
      .css("color", "red")
      .removeClass("d-none");
    return;
  }

  $.ajax({
    url: "/check-user",
    type: "POST",
    contentType: "application/json",
    data: JSON.stringify({ username, password }),
    success: function (response) {
      if (response.success === true) {
        $("#message")
          .text(response.message)
          .css("color", "green")
          .removeClass("d-none");

        setTimeout(() => {
          window.location.href = response.redirect;
        }, 500);
      } else {
        $("#message")
          .text(response.message)
          .css("color", "red")
          .removeClass("d-none");
      }
    },
    error: function (xhr) {
      let message = "An error occurred";
      if (xhr.responseJSON && xhr.responseJSON.message) {
        message = xhr.responseJSON.message;
      }
      $("#message").text(message).css("color", "red").removeClass("d-none");
    },
  });
}

function register() {
  const username = $("#username").val();
  const password = $("#password").val();
  const confirmPassword = $("#confirm_password").val();

  $("#message").text("").removeClass("d-block").addClass("d-none");

  if (!username || !password || !confirmPassword) {
    $("#message")
      .text("Please fill in all fields")
      .removeClass("d-none")
      .addClass("d-block")
      .css("color", "red");
    return;
  }

  if (password !== confirmPassword) {
    $("#message")
      .text("Passwords do not match")
      .removeClass("d-none")
      .addClass("d-block")
      .css("color", "red");
    return;
  }

  $.ajax({
    url: "/register",
    type: "POST",
    contentType: "application/json",
    data: JSON.stringify({ username, password }),
    success: function (response) {
      if (response.success) {
        alert(response.message);
        window.location.href = "/";
      } else {
        $("#message")
          .text(response.message)
          .removeClass("d-none")
          .addClass("d-block")
          .css("color", "red");
      }
    },
    error: function (xhr) {
      let message = "Registration failed";
      if (xhr.responseJSON && xhr.responseJSON.message) {
        message = xhr.responseJSON.message;
      }
      $("#message")
        .text(message)
        .removeClass("d-none")
        .addClass("d-block")
        .css("color", "red");
    },
  });
}

function clearRegisterForm() {
  $("#reg_username").val("");
  $("#reg_password").val("");
  $("#confirm_password").val("");
  $("#register_message").text("");
}
