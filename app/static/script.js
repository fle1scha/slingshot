const form = document.getElementById("form");
const formGroup = document.getElementById("form-group");
const formTitle = document.getElementById("form-title");
const successTitle = document.getElementById("success-title");
const formContainer = document.getElementById("form");
const responseMessage = document.getElementById("response-message");
const validationMessage = document.getElementById("validation-message");
const errorMessage = document.getElementById("error-message");
const nameInput = document.getElementById("name");
const phoneNumberInput = document.getElementById("phone_number");
var video = document.getElementById("background-video");
let loopInterval; // Variable to store the loop interval

// Event listener for closing the form
const closeFormButton = document.getElementById("close-form-button");
if (closeFormButton) {
  closeFormButton.addEventListener("click", function () {
    // Hide the form and show the previous content
    formContainer.style.display = "none";

    if (errorMessage) {
      errorMessage.style.display = "none";
    }

    var slingshotText = document.getElementById("slingshot-text");
    var slingshotDescription = document.getElementById("slingshot-description");
    var rerunButton = document.getElementById("rerun-button");

    // Show the rerun button
    if (rerunButton) {
      rerunButton.style.display = "flex";
    }

    // Restart the loop if it was stopped
    loopInterval = setInterval(function () {
      if (slingshotText.style.display === "none") {
        slingshotText.style.display = "block";
        slingshotDescription.style.display = "none";
      } else {
        slingshotText.style.display = "none";
        slingshotDescription.style.display = "block";
      }
    }, 5000); // Adjust interval timing as needed
  });
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const name = nameInput.value.trim();
  const phoneNumber = phoneNumberInput.value.trim();

  if (isValidName(name) && isValidPhoneNumber(phoneNumber)) {
    try {
      const response = await fetch("/", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: new URLSearchParams({ name, phone_number: phoneNumber }),
      });

      const data = await response.json();

      if (data.success) {
        formGroup.style.display = "none";
        successTitle.style.display = "block";
      } else {
        if (errorMessage) {
          errorMessage.textContent = data.error_message;
          errorMessage.style.display = "block";

          setTimeout(() => {
            if (errorMessage) {
              errorMessage.style.display = "none";
            }
          }, 1500);
        }
      }
    } catch (error) {
      if (errorMessage) {
        errorMessage.textContent =
          "An unexpected error occurred. Please try again later.";
        errorMessage.style.display = "block";

        setTimeout(() => {
          errorMessage.style.display = "none";
        }, 1500);
      }
    }
  } else {
    if (!isValidName(name)) {
      validationMessage.textContent = "Enter a valid name.";
      validationMessage.style.display = "block";
    } else {
      validationMessage.textContent = "Enter a 10-digit phone number.";
      validationMessage.style.display = "block";
    }

    setTimeout(() => {
      validationMessage.style.display = "none";
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
  var slingshotText = document.getElementById("slingshot-text");
  var slingshotDescription = document.getElementById("slingshot-description");
  var rerunButton = document.getElementById("rerun-button");

  // Hide the text when the button is clicked
  if (slingshotText) {
    slingshotText.style.display = "none";
  }

  if (slingshotDescription) {
    slingshotDescription.style.display = "none";
  }

  rerunButton.style.display = "none";
  formContainer.style.display = "flex";

  // Stop the interval when the sign-up form is open
  if (loopInterval) {
    clearInterval(loopInterval);
  }
}

// Show the text first, then the button after a delay
window.onload = function () {
  var slingshotText = document.getElementById("slingshot-text");
  var slingshotDescription = document.getElementById("slingshot-description");
  var rerunButton = document.getElementById("rerun-button");

  // Show 'rerun' button after the description
  setTimeout(function () {
    rerunButton.style.display = "flex";
  }, 5000);

  // Loop: toggle between 'slingshot' text and description every 5 seconds after the initial delay
  loopInterval = setInterval(function () {
    if (slingshotText.style.display === "none") {
      slingshotText.style.display = "block";
      slingshotDescription.style.display = "none";
    } else {
      slingshotText.style.display = "none";
      slingshotDescription.style.display = "block";
    }
  }, 5000); // Adjust interval timing as needed
};

let images = [];
let currentImageIndex = 0;

// Fetch images with a limit per request
async function fetchImages() {
  const response = await fetch(`/api/arenadata`);
  const newImages = await response.json();

  // Append new images to the existing list
  images = [...images, ...newImages];

  if (images.length > currentImageIndex) {
    displayNextImage();
  } else {
    console.error("No images returned from the API");
  }
}

// Display the next image
function displayNextImage() {
  if (currentImageIndex >= images.length) {
    console.log("No more images, fetching next batch");
    fetchImages();
    return;
  }

  const imgElement = document.createElement("img");
  imgElement.src = images[currentImageIndex].url; // Select the next image
  imgElement.classList.add("image");
  document.getElementById("image-container").appendChild(imgElement);

  // Fade in the image
  setTimeout(() => {
    imgElement.style.opacity = 1;
  }, 100);

  // Increment the image index
  currentImageIndex++;

  // Display the next image after a slight delay
  setTimeout(displayNextImage, 5000); // Adjust timing if needed, or remove the timeout for instant transition
}

// Start the image-fetching process when the page loads
fetchImages();
