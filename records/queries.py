from .models import Course, Enrollment, ResearchProject, Staff, Student


def students_with_programmes():
    return Student.objects.select_related('programme', 'advisor').order_by('name')


def courses_with_lecturers():
    return (
        Course.objects.select_related('department')
        .prefetch_related('lecturers')
        .order_by('course_code')
    )


def completed_course_grades():
    return (
        Enrollment.objects.filter(grade__isnull=False)
        .select_related('student', 'course')
        .order_by('student__name')
    )


def projects_with_leads():
    return (
        ResearchProject.objects.select_related('lead_lecturer')
        .prefetch_related('students')
        .order_by('title')
    )


def staff_with_departments():
    return Staff.objects.select_related('department').order_by(
        'department__name',
        'name',
    )