// Default credentials
const defaultUsername = "admin";
const defaultPassword = "12345";

// Get the login form element
const loginForm = document.getElementById('login-form');

// Add an event listener for form submission
loginForm.addEventListener('submit', function (event) {
    event.preventDefault(); // Prevent the default form submission

    // Retrieve user input
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    // Validate user input against default credentials
    if (username === defaultUsername && password === defaultPassword) {
        alert('Login successful! Redirecting to dataset page...');
        window.location.href = 'dataset.html'; // Redirect to dataset.html
    } else {
        alert('Invalid username or password. Please try again.');
    }
});
