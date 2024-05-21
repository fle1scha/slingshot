document.addEventListener('DOMContentLoaded', (event) => {
    const tshirtBoxes = document.querySelectorAll('.tshirt-box');
    const tshirtContainer = document.getElementById('tshirt-container');
    const formGroup = document.getElementById('form-group');
    const form = document.getElementById('form');
    const nameInput = document.getElementById('name');
    const phoneNumberInput = document.getElementById('phone_number');
    const shirtSizeSelect = document.getElementById('shirt_size');
    const successTitle = document.getElementById('success-title');
    const backButton = document.getElementById('back-button');
    const validationMessage = document.getElementById('validation-message');
    const errorMessage = document.getElementById('error-message');
    const merchText = document.getElementById('merch-text');
    const tshirtTypeInput = document.getElementById('tshirt_type');

    function resetMessages() {
        validationMessage.style.display = 'none';
        validationMessage.textContent = '';
        errorMessage.style.display = 'none';
        errorMessage.textContent = '';
    }

    function toggleImages(box) {
        const tshirtImage1 = box.querySelector('.tshirt-image:nth-child(1)');
        const tshirtImage2 = box.querySelector('.tshirt-image:nth-child(2)');
        setInterval(() => {
            if (tshirtImage1.style.display === 'none') {
                tshirtImage1.style.display = 'block';
                tshirtImage2.style.display = 'none';
            } else {
                tshirtImage1.style.display = 'none';
                tshirtImage2.style.display = 'block';
            }
        }, 2000); // Switch every 2 seconds
    }

    tshirtBoxes.forEach((box, index) => {
        toggleImages(box);

        box.addEventListener('click', () => {
            tshirtContainer.style.display = 'none';
            formGroup.style.display = 'block';
            merchText.style.display = 'none';
            resetMessages();

            // Set the t-shirt type
            tshirtTypeInput.value = index === 0 ? '\'38R\'' : '\'dragon won\'t sit still\'';
        });
    });

    backButton.addEventListener('click', () => {
        tshirtContainer.style.display = 'flex';
        formGroup.style.display = 'none';
        merchText.style.display = 'block';
        nameInput.value = '';
        phoneNumberInput.value = '';
        shirtSizeSelect.value = '';
        resetMessages();
    });

    form.addEventListener('submit', async (event) => {
        event.preventDefault();

        const name = nameInput.value.trim();
        const phoneNumber = phoneNumberInput.value.trim();
        const shirtSize = shirtSizeSelect.value;

        if (isValidName(name) && isValidPhoneNumber(phoneNumber) && shirtSize !== '') {
            try {
                const response = await fetch('/merch', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded'
                    },
                    body: new URLSearchParams({ name, phone_number: phoneNumber, shirt_size: shirtSize, tshirt_type: tshirtTypeInput.value })
                });

                const data = await response.json();

                if (data.success) {
                    formGroup.style.display = 'none';
                    successTitle.style.display = 'block';
                } else {
                    displayErrorMessage(data.error_message);
                }
            } catch (error) {
                displayErrorMessage('An unexpected error occurred. Please try again later.');
            }
        } else {
            displayValidationMessage(name, phoneNumber, shirtSize);
        }
    });

    function isValidPhoneNumber(phoneNumber) {
        const phoneNumberRegex = /^\d{10}$/;
        return phoneNumberRegex.test(phoneNumber);
    }

    function isValidName(name) {
        return name.length >= 3 && name.length < 51;
    }

    function displayValidationMessage(name, phoneNumber, shirtSize) {
        if (!isValidName(name)) {
            validationMessage.textContent = 'Enter a valid name.';
        } else if (!isValidPhoneNumber(phoneNumber)) {
            validationMessage.textContent = 'Enter a 10-digit phone number.';
        } else {
            validationMessage.textContent = 'Please select a shirt size.';
        }

        // Display and hide the validation message
        validationMessage.style.display = 'block';
        setTimeout(() => {
            validationMessage.style.display = 'none';
        }, 1500);
    }

    function displayErrorMessage(message) {
        if (errorMessage) {
            errorMessage.textContent = message;
            errorMessage.style.display = 'block';
            setTimeout(() => {
                errorMessage.style.display = 'none';
            }, 1000);
        }
    }
});