import { login } from "../services/authService.js";

window.handleLogin = async function () {
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  const result = await login(username, password);

  if (result.token) {
    window.location.href = "dashboard.html";
  } else {
    alert("Invalid credentials");
  }
};
