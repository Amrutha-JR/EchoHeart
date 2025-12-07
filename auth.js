document.addEventListener("DOMContentLoaded", function () {
  const signupForm = document.getElementById("signupForm");
  const loginForm  = document.getElementById("loginForm");
  const message = document.getElementById("message");

  // ===== Sign Up =====
  if (signupForm) {
    signupForm.addEventListener("submit", function (e) {
      e.preventDefault();
      const username = document.getElementById("signupUsername").value.trim();
      const password = document.getElementById("signupPassword").value.trim();

      if (!username || !password) {
        message.textContent = "❌ Please fill all fields!";
        message.style.color = "red";
        return;
      }

      let users = JSON.parse(localStorage.getItem("users")) || {};

      if (users[username]) {
        message.textContent = "⚠️ Username already exists!";
        message.style.color = "red";
      } else {
        users[username] = { password: password, fingerprint: null };
        localStorage.setItem("users", JSON.stringify(users));
        message.textContent = "✅ Sign up successful! Redirecting to login...";
        message.style.color = "green";

        setTimeout(() => { window.location.href = "login.html"; }, 1500);
      }
    });
  }

  // ===== Login =====
  if (loginForm) {
    loginForm.addEventListener("submit", function (e) {
      e.preventDefault();
      const username = document.getElementById("loginUsername").value.trim();
      const password = document.getElementById("loginPassword").value.trim();

      let users = JSON.parse(localStorage.getItem("users")) || {};

      if (users[username] && users[username].password === password) {
        localStorage.setItem("currentUser", username); // track logged-in user
        message.textContent = "✅ Login successful! Redirecting...";
        message.style.color = "green";

        setTimeout(() => { window.location.href = "minor.html"; }, 1000);
      } else {
        message.textContent = "❌ Invalid username or password!";
        message.style.color = "red";
      }
    });
  }
});
