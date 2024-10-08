// frontend/script.js
document.getElementById("registerForm")?.addEventListener("submit", async function(e) {
    e.preventDefault();
    
    const name = document.getElementById("name").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    const response = await fetch("http://127.0.0.1:5500/register", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ name, email, password })
    });

    if (response.ok) {
        alert("Registration successful!");
        window.location.href = "login.html";
    } else {
        alert("Registration failed. Please try again.");
    }
});

document.getElementById("loginForm")?.addEventListener("submit", async function(e) {
    e.preventDefault();

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    const response = await fetch("http://127.0.0.1:5500/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ email, password })
    });

    if (response.ok) {
        alert("Login successful!");
        // Redirect to another page or dashboard
    } else {
        alert("Login failed. Please check your credentials.");
    }
});