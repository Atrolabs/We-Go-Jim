document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('#workoutForm');
    const errorSection = document.getElementById('error-section');

    // Initially hide the error section
    errorSection.style.display = 'none';

    form.addEventListener('submit', async function (event) {
        event.preventDefault();

        try {
            const formData = new FormData(form);
            const jsonData = {
                email: formData.get('email'),
                workout_plan: constructWorkoutPlan(formData)
            };

            const response = await fetch('/add-workout', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(jsonData),
            });

            if (response.ok) {
                // Workout added successfully, redirect to /
                window.location.href = '/';
            } else {
                const responseData = await response.json();
                console.log(responseData);
                errorSection.textContent = responseData.message;
                errorSection.style.display = 'block'; // Show the error section
                errorSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        } catch (error) {
            console.error('An error occurred:', error);
            errorSection.textContent = 'An error occurred while processing the request.';
            errorSection.style.display = 'block'; // Show the error section
            errorSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    });

    // Initialize with fixed days of the week
    const daysOfWeek = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];

    daysOfWeek.forEach(day => {
        addDay(day);
    });
});

function constructWorkoutPlan(formData) {
    const workoutPlan = [];

    // Loop through each day container
    document.querySelectorAll('.day-container').forEach(dayContainer => {
        const dayName = dayContainer.querySelector('label').textContent.trim();

        // Skip if day name is empty
        if (!dayName) {
            return;
        }

        const exercises = [];

        // Loop through each exercise container within the day
        dayContainer.querySelectorAll('.exercise-container').forEach(exerciseContainer => {
            const exerciseName = exerciseContainer.querySelector('[name^="exercise_"]').value.trim();
            const numSets = parseInt(exerciseContainer.querySelector('[name^="num_sets_"]').value);

            const sets = [];

            // Loop through each set within the exercise
            for (let i = 1; i <= numSets; i++) {
                const reps = parseInt(exerciseContainer.querySelector(`[name^="reps_set_${dayName}_${i}"]`).value);
                const weight = parseFloat(exerciseContainer.querySelector(`[name^="weight_set_${dayName}_${i}"]`).value);

                sets.push({ number: i, reps, weight });
            }

            exercises.push({ name: exerciseName, sets });
        });

        workoutPlan.push({ day_name: dayName, exercises });
    });

    return workoutPlan;
}

function addDay(dayName) {
    const workoutDays = document.getElementById('workoutDays');
    const dayContainer = document.createElement('div');
    dayContainer.className = 'day-container';

    const dayNameLabel = document.createElement('label');
    dayNameLabel.textContent = dayName;
    dayContainer.appendChild(dayNameLabel);

    const exercisesContainer = document.createElement('div');
    exercisesContainer.className = 'exercises-container';

    workoutDays.appendChild(dayContainer);

    const addExerciseBtn = document.createElement('button');
    addExerciseBtn.type = 'button';
    addExerciseBtn.textContent = 'Add Exercise';
    addExerciseBtn.addEventListener('click', function () {
        addExercise(exercisesContainer, dayName);
    });

    dayContainer.appendChild(exercisesContainer);
    dayContainer.appendChild(addExerciseBtn);
}

function addExercise(exercisesContainer, dayName) {
    const exerciseContainer = document.createElement('div');
    exerciseContainer.className = 'exercise-container';

    const exerciseNameInput = document.createElement('input');
    exerciseNameInput.type = 'text';
    exerciseNameInput.className = 'form-control';
    exerciseNameInput.placeholder = 'Enter exercise name';
    exerciseNameInput.name = `exercise_${dayName}`; // Include day name in exercise name
    exerciseContainer.appendChild(exerciseNameInput);

    const setsContainer = document.createElement('div');
    const numSetsInput = document.createElement('input');
    numSetsInput.type = 'number';
    numSetsInput.className = 'form-control';
    numSetsInput.placeholder = 'Number of sets';
    numSetsInput.name = `num_sets_${dayName}`; // Include day name in num_sets name
    setsContainer.appendChild(numSetsInput);

    const setInputsContainer = document.createElement('div');

    numSetsInput.addEventListener('input', function () {
        const numSets = parseInt(numSetsInput.value);

        if (numSets < 0) {
            // Display an error or handle the invalid input here
            numSetsInput.value = 0; // Set a default value or handle it as appropriate
        }

        setInputsContainer.innerHTML = '';

        for (let i = 1; i <= numSets; i++) {
            const setContainer = document.createElement('div');
            setContainer.className = 'set-container';

            const repsInput = document.createElement('input');
            repsInput.type = 'number';
            repsInput.className = 'form-control';
            repsInput.placeholder = `Reps for Set ${i}`;
            repsInput.name = `reps_set_${dayName}_${i}`; // Include day name in reps_set name
            repsInput.addEventListener('input', function () {
                if (repsInput.value < 0) {
                    // Display an error or handle the invalid input here
                    repsInput.value = 0; // Set a default value or handle it as appropriate
                }
            });
            setContainer.appendChild(repsInput);

            const weightInput = document.createElement('input');
            weightInput.type = 'number';
            weightInput.className = 'form-control';
            weightInput.placeholder = `Weight for Set ${i}`;
            weightInput.name = `weight_set_${dayName}_${i}`; // Include day name in weight_set name
            weightInput.step = 0.5;
            weightInput.addEventListener('input', function () {
                if (weightInput.value < 0) {
                    // Display an error or handle the invalid input here
                    weightInput.value = 0; // Set a default value or handle it as appropriate
                }
            });
            setContainer.appendChild(weightInput);

            setInputsContainer.appendChild(setContainer);
        }
    });

    setsContainer.appendChild(setInputsContainer);
    exerciseContainer.appendChild(setsContainer);
    exercisesContainer.appendChild(exerciseContainer);
}
