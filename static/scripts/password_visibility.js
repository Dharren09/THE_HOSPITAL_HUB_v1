const passwordInput = document.querySelector('#password');
const confirmPasswordInput = document.querySelector('#confirmPassword');
const passwordToggleBtn = document.querySelector('#password-toggle-btn');
const confirmPassToggleBtn = document.querySelector('#confirm-password-toggle-btn');

function togglePasswordVisibility(input, toggleBtn) {
  if (input.type === "password") {
    input.type = "text";
    toggleBtn.textContent = "Hide";
  } else {
    input.type = "password";
    toggleBtn.textContent = "Show";
  }
}

passwordToggleBtn.addEventListener('click', function() {
  togglePasswordVisibility(passwordInput, passwordToggleBtn);
});

confirmPassToggleBtn.addEventListener('click', function() {
  togglePasswordVisibility(confirmPasswordInput, confirmPassToggleBtn);
});