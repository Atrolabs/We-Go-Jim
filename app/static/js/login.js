document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form');
    const errorSection = document.getElementById('error-section'); // Add this line

    form.addEventListener('submit', function (event) {
        event.preventDefault();

        const formData = new FormData(form);
        const jsonData = Object.fromEntries(formData.entries());

        const xhr = new XMLHttpRequest();
        xhr.open('POST', '/login', true);
        xhr.setRequestHeader('Content-Type', 'application/json');

        xhr.onreadystatechange = function () {
            if (xhr.readyState === XMLHttpRequest.DONE) {
                if (xhr.status === 200) {
                    // Login successful, redirect to the dashboard
                    window.location.href = '/dashboard';
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

        xhr.onerror = function () {
            // Handle network errors or other issues
            console.error('XHR Error:', xhr.statusText);
        };

        xhr.send(JSON.stringify(jsonData));
    });
});
