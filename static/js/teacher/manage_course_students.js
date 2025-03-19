// Function to close modal
function closeCustomModal(modalId) {
    // Remove modal display class
    document.getElementById(modalId).classList.remove('show');
    document.getElementById(modalId).style.display = 'none';
    
    // Remove modal-open class and inline style from body
    document.body.classList.remove('modal-open');
    document.body.style.overflow = '';
    
    // Remove background overlay
    const backdrops = document.getElementsByClassName('modal-backdrop');
    if (backdrops.length > 0) {
        Array.from(backdrops).forEach(backdrop => {
            backdrop.parentNode.removeChild(backdrop);
        });
    }
}

$(document).ready(function() {
    // Get course ID from the URL or data attribute
    const courseId = document.querySelector('meta[name="course-id"]').getAttribute('content');
    
    // Fix add student button click issue
    $('.header-actions button[data-bs-target="#addStudentModal"]').on('click', function(e) {
        e.preventDefault();
        e.stopPropagation();
        
        // Manually open modal
        const modal = document.getElementById('addStudentModal');
        modal.classList.add('show');
        modal.style.display = 'block';
        document.body.classList.add('modal-open');
        document.body.style.overflow = 'hidden';
        
        // Add background overlay
        const backdrop = document.createElement('div');
        backdrop.className = 'modal-backdrop fade show';
        document.body.appendChild(backdrop);
    });
    
    // Fix close button
    $('#addStudentModal .btn-close, #addStudentModal button[data-bs-dismiss="modal"]').on('click', function() {
        closeCustomModal('addStudentModal');
    });
    
    // Add GPA calculation function
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
    $('.grade-input').on('input', function() {
        const row = $(this).closest('tr');
        calculateGPA(row);
    });

    // Calculate all GPAs on page load
    $('tr[data-student-id]').each(function() {
        calculateGPA($(this));
    });

    // Load existing grades
    function loadStudentGrades(studentId) {
        $.get(`/grades/course/${courseId}/student/${studentId}/grades/`)
            .done(function(data) {
                const row = $(`tr[data-student-id="${studentId}"]`);
                row.find('input[name="final_exam"]').val(data.final_exam);
                row.find('input[name="assignments"]').val(data.assignments);
                row.find('input[name="regular_quiz"]').val(data.regular_quiz);
                row.find('input[name="attendance"]').val(data.attendance);
                
                // Calculate GPA after loading other grades
                calculateGPA(row);
            })
            .fail(function(xhr) {
                console.error('Failed to load grades:', xhr.responseText);
            });
    }

    // Load grades for all enrolled students
    $('.table tbody tr').each(function() {
        const studentId = $(this).data('student-id');
        loadStudentGrades(studentId);
    });

    // Add student to course
    $('#add-student-btn').click(function() {
        const studentId = $('#student-select').val();
        if (!studentId) {
            alert('Please select a student');
            return;
        }

        $.ajax({
            url: `/grades/course/${courseId}/student/${studentId}/add/`,
            method: 'POST',
            data: {
                'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val()
            },
            success: function(response) {
                if (response.status === 'success') {
                    location.reload();
                } else {
                    alert('Failed to add student: ' + response.message);
                }
            },
            error: function(xhr) {
                alert('Failed to add student, please try again');
            }
        });
    });

    // Remove student from course
    $('.remove-student').click(function() {
        if (!confirm('Are you sure you want to remove this student from the course?')) {
            return;
        }

        const row = $(this).closest('tr');
        const studentId = row.data('student-id');

        $.ajax({
            url: `/grades/course/${courseId}/student/${studentId}/remove/`,
            method: 'POST',
            data: {
                'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val()
            },
            success: function(response) {
                if (response.status === 'success') {
                    row.remove();
                } else {
                    alert('Failed to remove student: ' + response.message);
                }
            },
            error: function(xhr) {
                alert('Failed to remove student, please try again');
            }
        });
    });

    // Save grades
    $('.save-grades').click(function() {
        const row = $(this).closest('tr');
        const studentId = row.data('student-id');
        
        // Calculate GPA before saving
        calculateGPA(row);
        
        const gradeData = {
            'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
            'final_exam': row.find('input[name="final_exam"]').val(),
            'assignments': row.find('input[name="assignments"]').val(),
            'regular_quiz': row.find('input[name="regular_quiz"]').val(),
            'attendance': row.find('input[name="attendance"]').val(),
            'gpa': row.find('input[name="gpa"]').val()
        };

        // Get grade_id
        $.get(`/grades/course/${courseId}/student/${studentId}/grades/`)
            .done(function(data) {
                if (data.grade_id) {
                    $.ajax({
                        url: `/grades/grade/${data.grade_id}/update/`,
                        method: 'POST',
                        data: gradeData,
                        success: function(response) {
                            if (response.status === 'success') {
                                alert('Grades saved successfully');
                            } else {
                                alert('Failed to save grades: ' + response.message);
                            }
                        },
                        error: function(xhr) {
                            alert('Failed to save grades, please try again');
                        }
                    });
                }
            });
    });
}); 