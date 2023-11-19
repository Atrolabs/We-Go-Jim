document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form');

    form.addEventListener('submit', function (event) {
        event.preventDefault();

        let userRole;
        if (document.getElementById('isTrainer').checked) {
            userRole = 'Trainer';
        } else if (document.getElementById('isStudent').checked) {
            userRole = 'Student';
        }

        // Create a form data object from the form element
        const formData = new FormData(form);

        // Convert the form data object to a JSON object
        const jsonData = Object.fromEntries(formData.entries());

        // Send JSON data to the server
        fetch('/submit', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(jsonData),
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
