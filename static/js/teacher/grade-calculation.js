// GPA calculation function
function calculateGPA(row) {
    // Get values from all input fields
    const finalExam = parseFloat(row.find('input[name="final_exam"]').val()) || 0;
    const assignments = parseFloat(row.find('input[name="assignments"]').val()) || 0;
    const regularQuiz = parseFloat(row.find('input[name="regular_quiz"]').val()) || 0;
    const attendance = parseFloat(row.find('input[name="attendance"]').val()) || 0;
    
    // Calculate simple average
    const average = (finalExam + assignments + regularQuiz + attendance) / 4;
    
    // Round to 2 decimal places
    const formattedAverage = average.toFixed(2);
    
    // Update both the display and hidden input
    const studentId = row.data('student-id');
    row.find('#gpa-display-' + studentId).text(formattedAverage);
    row.find('#gpa-' + studentId).val(formattedAverage);
    
    return formattedAverage;
}

// Update grade fields to calculate GPA when they change
$(document).ready(function() {
    $('.grade-input').on('input', function() {
        const row = $(this).closest('tr');
        calculateGPA(row);
    });

    // Calculate all GPAs on page load
    $('tr[data-student-id]').each(function() {
        calculateGPA($(this));
    });
}); 