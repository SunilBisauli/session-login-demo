document.addEventListener("DOMContentLoaded", function() {
    const loginForm = document.getElementById("loginForm");

    if (loginForm) {
        loginForm.addEventListener("submit", function(event) {
            const username = document.getElementById("username").value;
            const password = document.getElementById("password").value;

            // Basic validation to ensure no empty spaces are submitted
            if (username.trim() === "" || password.trim() === "") {
                alert("Please fill out both username and password fields.");
                event.preventDefault(); // Stops the form from submitting to Python
            }
        });
    }
});