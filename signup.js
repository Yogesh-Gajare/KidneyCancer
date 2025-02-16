document.addEventListener("DOMContentLoaded", function () {
    const signupForm = document.getElementById("signup-form");

    if (signupForm) {
        signupForm.addEventListener("submit", function (event) {
            event.preventDefault(); // Prevent the default form submission

            // Perform any validation or additional logic here if necessary

            // Redirect to the dataset.html page
            window.location.href = "login.html";
        });
    }
});
