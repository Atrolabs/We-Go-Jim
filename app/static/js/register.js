document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form');

    form.addEventListener('submit', function (event) {
        event.preventDefault();

        const userRole = document.getElementById('isTrainer').checked ? 'Trainer' : 'Student';

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
    checkboxes.forEach(id => {
        if (id !== checkboxId) {
            document.getElementById(id).checked = false;
        }
    });
}
