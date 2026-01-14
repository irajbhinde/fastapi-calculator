function isValidEmail(email) {
  return /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email);
}

document.addEventListener("DOMContentLoaded", () => {
  const registerForm = document.getElementById("register-form");
  const loginForm = document.getElementById("login-form");

  // ---------- REGISTER HANDLER ----------
  if (registerForm) {
    const usernameInput = document.getElementById("reg-username");
    const emailInput = document.getElementById("reg-email");
    const passwordInput = document.getElementById("reg-password");
    const confirmInput = document.getElementById("reg-confirm");
    const errorEl = document.getElementById("register-error");
    const successEl = document.getElementById("register-success");

    registerForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      errorEl.textContent = "";
      successEl.textContent = "";

      const username = usernameInput.value.trim();
      const email = emailInput.value.trim();
      const password = passwordInput.value;
      const confirm = confirmInput.value;

      // Client-side checks
      if (!isValidEmail(email)) {
        errorEl.textContent = "Please enter a valid email.";
        return;
      }
      if (password.length < 8) {
        errorEl.textContent = "Password must be at least 8 characters.";
        return;
      }
      if (password !== confirm) {
        errorEl.textContent = "Passwords do not match.";
        return;
      }

      try {
        const resp = await fetch("/register", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ username, email, password }),
        });

        if (!resp.ok) {
          const data = await resp.json().catch(() => ({}));
          errorEl.textContent =
            data.detail || "Registration failed. Please try again.";
          return;
        }

        const data = await resp.json();
        window.localStorage.setItem("access_token", data.access_token);

        // 👇 This must contain "Registration successful" for the tests:
        successEl.textContent =
          "Registration successful! Token stored in localStorage.";
      } catch (err) {
        console.error(err);
        errorEl.textContent = "Network error. Please try again.";
      }
    });
  }

  // ---------- LOGIN HANDLER ----------
if (loginForm) {
  const identifierInput = document.getElementById("login-identifier");
  const passwordInput = document.getElementById("login-password");
  const errorEl = document.getElementById("login-error");
  const successEl = document.getElementById("login-success");

  loginForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    errorEl.textContent = "";
    successEl.textContent = "";

    const identifier = identifierInput.value.trim();
    const password = passwordInput.value;

    if (!identifier || !password) {
      errorEl.textContent = "Please fill in both fields.";
      return;
    }
    if (!isValidEmail(identifier)) {
      errorEl.textContent = "Please enter a valid email.";
      return;
    }

    try {
      const resp = await fetch("/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          email: identifier,   // 👈 must be "email"
          password: password,  // 👈 and "password"
        }),
      });

      if (!resp.ok) {
        errorEl.textContent = "Invalid credentials";
        return;
      }

      const data = await resp.json();
      window.localStorage.setItem("access_token", data.access_token);
      successEl.textContent =
        "Login successful! Token stored in localStorage.";
        console.log("UI LOGIN SUCCESS TEXT:", successEl.textContent);
    } catch (err) {
      console.error(err);
      errorEl.textContent = "Network error. Please try again.";
    }
  });
}
});
