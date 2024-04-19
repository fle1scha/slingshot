// Get the form, form-group, and response-message elements
const form = document.getElementById('form');
const formGroup = document.getElementById('form-group');
const formTitle = document.getElementById('form-title');
const successTitle = document.getElementById('success-title');
const logoContainer = document.getElementById('logo-container')
const responseMessage = document.getElementById('response-message');
const validationMessage = document.getElementById('validation-message');
const errorMessage = document.getElementById('error-message');
const nameInput = document.getElementById('name');
const phoneNumberInput = document.getElementById('phone_number');

// Add an event listener to the form's submit event
form.addEventListener('submit', async (event) => {
    event.preventDefault(); // Prevent the default form submission

    const name = nameInput.value.trim();
    const phoneNumber = phoneNumberInput.value.trim();

    // Check if the name and phone number are valid
    if (isValidName(name) && isValidPhoneNumber(phoneNumber)) {
        try {
            const response = await fetch('/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: new URLSearchParams({ name, phone_number: phoneNumber })
            });

            const data = await response.json();

            if (data.success) {
                logoContainer.style.display = 'none';
                formGroup.style.display = 'none';
                successTitle.style.display = 'block';
            } else {
                // Display the error message
                if (errorMessage) {
                    errorMessage.textContent = data.error_message;
                    errorMessage.style.display = 'block';

                    // Clear the error message after 1.5 seconds
                    setTimeout(() => {
                        if (errorMessage) {
                            errorMessage.style.display = 'none';
                        }
                    }, 1500);
                }
            }
        } catch (error) {
            // Display a generic error message for other errors
            if (errorMessage) {
                errorMessage.textContent = 'An unexpected error occurred. Please try again later.';
                errorMessage.style.display = 'block';

                // Clear the error message after 1.5 seconds
                setTimeout(() => {
                    errorMessage.style.display = 'none';
                }, 1500);
            }
        }
    } else {
        // Display the custom validation error messages
        if (!isValidName(name)) {
            validationMessage.textContent = 'Enter a valid name.';
            validationMessage.style.display = 'block';
        } else {
            validationMessage.textContent = 'Enter a 10-digit phone number.';
            validationMessage.style.display = 'block';
        }

        // Hide the validation message after 1.5 seconds
        setTimeout(() => {
            validationMessage.style.display = 'none';
        }, 1500);
    }
});

function isValidPhoneNumber(phoneNumber) {
    // Validate the phone number format
    const phoneNumberRegex = /^\d{10}$/;
    return phoneNumberRegex.test(phoneNumber);
}

function isValidName(name) {
    // Validate the name (not empty)
    return name.length >= 3 && name.length < 51;
}