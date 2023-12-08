document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('#workoutForm');
    const errorSection = document.getElementById('error-section');

    form.addEventListener('submit', async function (event) {
        event.preventDefault();

        try {
            const formData = new FormData(form);
            const jsonData = {
                user_sub: formData.get('user_sub'),
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
                // Workout added successfully, you can redirect or show a success message
                console.log('Workout added successfully');
            } else {
                const responseData = await response.json();
                console.log(responseData);
                errorSection.textContent = responseData.message;
                errorSection.style.display = 'block';
                errorSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        } catch (error) {
            console.error('An error occurred:', error);
            errorSection.textContent = 'An error occurred while processing the request.';
            errorSection.style.display = 'block';
            errorSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    });
});

function constructWorkoutPlan(formData) {
    const workoutPlan = [];

    // Loop through each day container
    document.querySelectorAll('.day-container').forEach(dayContainer => {
        const dayName = dayContainer.querySelector('[name="day_name"]').value.trim();

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

function addDay() {
    const workoutDays = document.getElementById('workoutDays');
    const dayContainer = document.createElement('div');
    dayContainer.className = 'day-container';

    const dayNameInput = document.createElement('input');
    dayNameInput.type = 'text';
    dayNameInput.className = 'form-control';
    dayNameInput.placeholder = 'Enter day name (e.g., Monday)';
    dayNameInput.name = 'day_name'; // Added name attribute
    dayContainer.appendChild(dayNameInput);

    const exercisesContainer = document.createElement('div');
    exercisesContainer.className = 'exercises-container';

    const addExerciseBtn = document.createElement('button');
    addExerciseBtn.type = 'button';
    addExerciseBtn.textContent = 'Add Exercise';
    addExerciseBtn.addEventListener('click', function () {
        addExercise(exercisesContainer, dayNameInput.value);
    });

    dayContainer.appendChild(exercisesContainer);
    dayContainer.appendChild(addExerciseBtn);

    workoutDays.appendChild(dayContainer);
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
        setInputsContainer.innerHTML = '';

        for (let i = 1; i <= numSets; i++) {
            const setContainer = document.createElement('div');
            setContainer.className = 'set-container';

            const repsInput = document.createElement('input');
            repsInput.type = 'number';
            repsInput.className = 'form-control';
            repsInput.placeholder = `Reps for Set ${i}`;
            repsInput.name = `reps_set_${dayName}_${i}`; // Include day name in reps_set name
            setContainer.appendChild(repsInput);

            const weightInput = document.createElement('input');
            weightInput.type = 'number';
            weightInput.className = 'form-control';
            weightInput.placeholder = `Weight for Set ${i}`;
            weightInput.name = `weight_set_${dayName}_${i}`; // Include day name in weight_set name
            setContainer.appendChild(weightInput);

            setInputsContainer.appendChild(setContainer);
        }
    });

    setsContainer.appendChild(setInputsContainer);
    exerciseContainer.appendChild(setsContainer);
    exercisesContainer.appendChild(exerciseContainer);
}
