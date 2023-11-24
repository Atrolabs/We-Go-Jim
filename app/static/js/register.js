document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form');

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

        fetch('/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(jsonData),  // Send the updated JSON data
        })
        .then(response => response.json())
        .then(data => console.log(data))
        .catch(error => console.error('Error:', error));
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
