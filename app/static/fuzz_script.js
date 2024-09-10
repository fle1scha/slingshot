const rerunButton = document.getElementById('rerun-button');
const staticTextBox = document.getElementById('static-text-box');
const eventDetailsBox = document.getElementById('event-details-box');

// Show the button immediately on window load
window.onload = function() {
    rerunButton.style.display = 'flex';
}

// Function to show event details
function showEventDetails() {
    rerunButton.style.display = 'none'; 
    staticTextBox.style.display = 'none';
    eventDetailsBox.style.display = 'flex'; 
}