from django.shortcuts import render
from .queries import (
    completed_course_grades,
    courses_with_lecturers,
    courses_with_prerequisites,
    enrolled_students,
    funded_research_projects,
    lecturer_qualifications,
    pending_course_grades,
    projects_with_leads,
    staff_with_departments,
    students_with_programmes,
)


QUERY_OPTIONS = {
    'students': ('Students with programmes and advisors', students_with_programmes),
    'courses': ('Courses with departments and lecturers', courses_with_lecturers),
    'grades': ('Completed course grades', completed_course_grades),
    'projects': ('Research projects with leads and students', projects_with_leads),
    'staff': ('Staff grouped by department', staff_with_departments),
    'enrolled': ('Enrolled students by programme', enrolled_students),
    'pending-grades': ('Course enrollments with pending grades', pending_course_grades),
    'prerequisites': ('Courses with prerequisites', courses_with_prerequisites),
    'qualifications': ('Lecturer qualifications', lecturer_qualifications),
    'funding': ('Funded research projects', funded_research_projects),
}


def home(request):
    return render(request, 'records/home.html')


def database_queries(request):
    selected = request.GET.get('query')
    results = None
    title = None
    if selected in QUERY_OPTIONS:
        title, query = QUERY_OPTIONS[selected]
        results = query()
    return render(
        request,
        'records/queries.html',
        {
            'options': QUERY_OPTIONS,
            'results': results,
            'selected': selected,
            'title': title,
        },
    )
