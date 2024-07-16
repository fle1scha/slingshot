const form = document.getElementById('form');
const formGroup = document.getElementById('form-group');
const formTitle = document.getElementById('form-title');
const successTitle = document.getElementById('success-title');
const logoContainer = document.getElementById('logo');
const formContainer = document.getElementById('form');
const responseMessage = document.getElementById('response-message');
const validationMessage = document.getElementById('validation-message');
const errorMessage = document.getElementById('error-message');
const nameInput = document.getElementById('name');
const phoneNumberInput = document.getElementById('phone_number');

form.addEventListener('submit', async (event) => {
    event.preventDefault();

    const name = nameInput.value.trim();
    const phoneNumber = phoneNumberInput.value.trim();

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
                if (errorMessage) {
                    errorMessage.textContent = data.error_message;
                    errorMessage.style.display = 'block';

                    setTimeout(() => {
                        if (errorMessage) {
                            errorMessage.style.display = 'none';
                        }
                    }, 1500);
                }
            }
        } catch (error) {
            if (errorMessage) {
                errorMessage.textContent = 'an unexpected error occurred. Please try again later.';
                errorMessage.style.display = 'block';

                setTimeout(() => {
                    errorMessage.style.display = 'none';
                }, 1500);
            }
        }
    } else {
        if (!isValidName(name)) {
            validationMessage.textContent = 'enter a valid name.';
            validationMessage.style.display = 'block';
        } else {
            validationMessage.textContent = 'enter a 10-digit phone number.';
            validationMessage.style.display = 'block';
        }

        setTimeout(() => {
            validationMessage.style.display = 'none';
        }, 1500);
    }
});

function isValidPhoneNumber(phoneNumber) {
    const phoneNumberRegex = /^\d{10}$/;
    return phoneNumberRegex.test(phoneNumber);
}

function isValidName(name) {
    return name.length >= 3 && name.length < 51;
}

function showSignUp() {
    var video = document.getElementById('background-video');
    video.play();
    
    var rerunButton = document.getElementById('rerun-button');
    rerunButton.style.display = 'none';
    
    logoContainer.style.display = 'flex';
    formContainer.style.display = 'flex';
}

window.onload = function() {
    setTimeout(function() {
        var rerunButton = document.getElementById('rerun-button');
        rerunButton.style.display = 'flex'; 
    }, 2000);
};