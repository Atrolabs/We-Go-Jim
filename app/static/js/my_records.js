const exerciseNameMapping = {
    'benchPress': 'Bench Press',
    'deadlift': 'Deadlift',
    'squats': 'Squats'
};

document.addEventListener('DOMContentLoaded', function () {
    const formGroups = document.querySelectorAll('.form-group');
    const errorSection = document.getElementById('error-section');

    // Initially hide the error section
    // errorSection.style.display = 'none'; ADD STYLE

    formGroups.forEach((group) => {
        const button = group.querySelector('button');
        const input = group.querySelector('input');
        const exerciseId = group.querySelector('label').getAttribute('for');
        const exerciseName = exerciseNameMapping[exerciseId];

        button.addEventListener('click', async function (event) {
            event.preventDefault();

            try {
                const newRecord = input.value;
                const jsonData = {
                    exercise_name: exerciseName,
                    new_record: newRecord
                };

                const response = await fetch('/my-records', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(jsonData),
                });

                if (response.ok) {
                    // Record added successfully, redirect to /
                    window.location.href = '/my-records';
                } else {
                    const responseData = await response.json();
                    console.log(responseData);
                    errorSection.textContent = responseData.message;
                    // errorSection.style.display = 'block'; // Show the error section ADD STYLE
                    errorSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
            } catch (error) {
                console.error('An error occurred:', error);
                errorSection.textContent = 'An error occurred while processing the request.';
                // errorSection.style.display = 'block'; // Show the error section ADD STYLE
                errorSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });
});

function validateInput(input) {
    // Prevent negative values
    if (input.value < 0) {
        input.value = 0;
    }
}
