// Get the form, form-group, and response-message elements
const form = document.getElementById('form');
const formGroup = document.getElementById('form-group');
const formTitle = document.getElementById('form-title');
const successTitle = document.getElementById('success-title');
const responseMessage = document.getElementById('response-message');
const validationMessage = document.getElementById('validation-message');
const errorMessage = document.getElementById('error-message');

// Add an event listener to the form's submit event
form.addEventListener('submit', async (event) => {
    event.preventDefault(); // Prevent the default form submission

    const phoneNumber = form.elements.phone_number.value;

    // Check if the phone number is valid
    if (isValidPhoneNumber(phoneNumber)) {
        try {
            const response = await fetch('/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: new URLSearchParams({ phone_number: phoneNumber })
            });

            const data = await response.json();

            if (response.ok) {
                // Hide the form and form-group
                formGroup.style.display = 'none';

                // Hide the form title and show the success title
                formTitle.style.display = 'none';
                successTitle.style.display = 'block';
            } else {
                // Display the error message
                errorMessage.textContent = data.error_message;
                errorMessage.style.display = 'block';

                // Clear the error message after 5 seconds
                setTimeout(() => {
                    errorMessage.style.display = 'none';
                }, 1500);
            }
        } catch (error) {
            // Display a generic error message for other errors
            errorMessage.textContent = 'error. please try again later.';
            errorMessage.style.display = 'block';

            // Clear the error message after 5 seconds
            setTimeout(() => {
                errorMessage.style.display = 'none';
            }, 1500);
        }
    } else {
        // Display the custom validation error message
        validationMessage.style.display = 'block';

        // Hide the validation message after 3 seconds
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