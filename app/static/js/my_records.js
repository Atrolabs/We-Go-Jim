function validateInput(input) {
    // Prevent negative values
    if (input.value < 0) {
        input.value = 0;
    }
}