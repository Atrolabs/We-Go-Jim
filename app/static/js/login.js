document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form');

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
                    console.log(response);
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
