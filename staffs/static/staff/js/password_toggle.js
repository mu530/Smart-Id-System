function passwordToggle(id) {
  let pwd_field = document.getElementById(id);
  let toggleIcon = document.getElementById(id + "_toggle");

  if (pwd_field.type === "password") {
    pwd_field.type = "text";
    toggleIcon.classList.remove("fa-eye-low-vision");
    toggleIcon.classList.add("fa-eye");
  } else {
    pwd_field.type = "password";
    toggleIcon.classList.remove("fa-eye");
    toggleIcon.classList.add("fa-eye-low-vision");
  }
}
