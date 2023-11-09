function togglePassVisibility() {
  let input = document.getElementById("passwordInput");
  let img = document.getElementById("visibilityImg");
  if (input.type == "password") {
    input.type = "text";
    img.src = "static/images/hide.png";
  } else {
    input.type = "password";
    img.src = "static/images/view.png";
  }
}
