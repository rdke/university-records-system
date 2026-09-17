from .models import Course, Enrollment, LecturerQualification, ResearchProject, Staff, Student


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


def enrolled_students():
    return (
        Student.objects.filter(graduation_status=Student.GraduationStatus.ENROLLED)
        .select_related('programme')
        .order_by('name')
    )


def pending_course_grades():
    return (
        Enrollment.objects.filter(grade__isnull=True)
        .select_related('student', 'course')
        .order_by('course__course_code', 'student__name')
    )


def courses_with_prerequisites():
    return Course.objects.prefetch_related('prerequisites').order_by('course_code')


def lecturer_qualifications():
    return LecturerQualification.objects.select_related('lecturer').order_by(
        'lecturer__name',
        'qualification',
    )


def funded_research_projects():
    return ResearchProject.objects.exclude(funding_source='').select_related(
        'lead_lecturer'
    ).order_by('title')