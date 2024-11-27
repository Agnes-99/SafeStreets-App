document.addEventListener('DOMContentLoaded', function() {

    var form = document.getElementById("Registration-form");

    
    form.addEventListener("submit", function(event) {
        event.preventDefault(); 
        
        document.querySelectorAll(".error").forEach(function(el) {
            el.textContent = "";
        });
        document.querySelector(".response-failure").textContent = "";

        // Gather form data
        var firstname = document.getElementById('firstname').value.trim();
        var surname = document.getElementById('surname').value.trim();
        var username = document.getElementById('username').value.trim();
        var cellnumber = document.getElementById('cellnumber').value.trim();
        var email = document.getElementById('email').value.trim();
        var password = document.getElementById('password').value.trim();

        var isValid = true;

        // Validate username
        if (!/^[a-zA-Z0-9_]{3,20}$/.test(username)) {
            var usernameError = document.getElementById("username-error");
            if (usernameError) {
                usernameError.textContent = "Username must be 3-20 characters long and contain only letters, numbers, and underscores.";
            }
            isValid = false;
        }

        // Validate cellphone number
        if (!/^\d{10}$/.test(cellnumber)) {
            var cellnumberError = document.getElementById("cellnumber-error");
            if (cellnumberError) {
                cellnumberError.textContent = "Cellphone number must be exactly 10 digits long.";
            }
            isValid = false;
        }

        // Validate email
        if (!/^[\w\.-]+@[\w\.-]+\.\w+$/.test(email)) {
            var emailError = document.getElementById("email-error");
            if (emailError) {
                emailError.textContent = "Invalid email address";
            }
            isValid = false;
        }

        // Validate password
        if (password.length < 6) {
            var passwordError = document.getElementById("password-error");
            if (passwordError) {
                passwordError.textContent = "Password must be at least 6 characters long.";
            }
            isValid = false;
        }

        if (!isValid) {
            return; 
        }else{
            form.submit();
        }
    });
});
