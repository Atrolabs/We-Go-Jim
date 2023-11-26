document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form');
    const errorSection = document.getElementById('error-section'); // Add this line

    form.addEventListener('submit', function (event) {
        event.preventDefault();

        const isStudentCheckbox = document.getElementById('isStudent');
        const isTrainerCheckbox = document.getElementById('isTrainer');

        // Check if at least one checkbox is checked
        if (!isStudentCheckbox.checked && !isTrainerCheckbox.checked) {
            alert('Please select at least one option.');
            return; // Prevent form submission if no checkbox is checked
        }

        const userRole = isTrainerCheckbox.checked ? 'Trainer' : 'Student';

        const formData = new FormData(form);
        const jsonData = Object.fromEntries(formData.entries());

        // Update the key for user role to match the server-side expectation
        jsonData.userRole = userRole;

        const xhr = new XMLHttpRequest();
        xhr.open('POST', '/register', true);
        xhr.setRequestHeader('Content-Type', 'application/json');

        xhr.onreadystatechange = function () {
            if (xhr.readyState === XMLHttpRequest.DONE) {
                if (xhr.status === 200) {
                    // Registration successful, redirect to the dashboard or login page
                    window.location.href = '/login'; // Redirect to login after registration
                } else {
                    // Handle other successful cases if needed
                    const response = JSON.parse(xhr.responseText);
                    // Display the error message in the error section
                    errorSection.textContent = response.message;

                    // Show the error section
                    errorSection.style.display = 'block'; // Show the error section

                    // You can also scroll to the error section for better visibility
                    errorSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
            }
        };

        xhr.send(JSON.stringify(jsonData));
    });
});

function toggleCheckboxes(checkboxId) {
    const checkboxes = ['isTrainer', 'isStudent'];
    const clickedCheckbox = document.getElementById(checkboxId);

    checkboxes.forEach(id => {
        const checkbox = document.getElementById(id);

        if (id !== checkboxId) {
            // If the clicked checkbox is checked, uncheck the other checkbox
            if (clickedCheckbox.checked) {
                checkbox.checked = false;
            } else {
                // If the clicked checkbox is unchecked, make sure at least one checkbox is checked
                if (!checkbox.checked && !clickedCheckbox.checked) {
                    clickedCheckbox.checked = true;
                }
            }
        }
    });
}

function login_redirect() {
    var destinationURL = '/login'
    
    history.pushState({}, '', destinationURL);

    window.history.pushState({}, '', destinationURL);
    
    window.location.href = destinationURL;
}
