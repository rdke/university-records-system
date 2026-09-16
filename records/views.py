from django.forms import modelform_factory
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from .models import (
    Course,
    Department,
    Lecturer,
    Programme,
    ResearchProject,
    Staff,
    Student,
)
from .queries import (
    completed_course_grades,
    courses_with_lecturers,
    projects_with_leads,
    staff_with_departments,
    students_with_programmes,
)


ENTITIES = {
    'departments': (Department, 'Departments'),
    'programmes': (Programme, 'Programmes'),
    'lecturers': (Lecturer, 'Lecturers'),
    'students': (Student, 'Students'),
    'staff': (Staff, 'Staff'),
    'courses': (Course, 'Courses'),
    'projects': (ResearchProject, 'Research Projects'),
}

QUERY_OPTIONS = {
    'students': ('Students with programmes and advisors', students_with_programmes),
    'courses': ('Courses with departments and lecturers', courses_with_lecturers),
    'grades': ('Completed course grades', completed_course_grades),
    'projects': ('Research projects with leads and students', projects_with_leads),
    'staff': ('Staff grouped by department', staff_with_departments),
}


def get_entity(entity):
    try:
        return ENTITIES[entity]
    except KeyError as error:
        raise Http404 from error


def home(request):
    return render(request, 'records/home.html', {'entities': ENTITIES})


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


def entity_list(request, entity):
    model, title = get_entity(entity)
    return render(
        request,
        'records/entity_list.html',
        {'entity': entity, 'objects': model.objects.all(), 'title': title},
    )


def entity_create(request, entity):
    model, title = get_entity(entity)
    form_class = modelform_factory(model, fields='__all__')
    form = form_class(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('entity-list', entity=entity)
    return render(
        request,
        'records/entity_form.html',
        {'form': form, 'title': f'Add {model._meta.verbose_name}'},
    )


def entity_update(request, entity, pk):
    model, title = get_entity(entity)
    record = get_object_or_404(model, pk=pk)
    form_class = modelform_factory(model, fields='__all__')
    form = form_class(request.POST or None, instance=record)
    if form.is_valid():
        form.save()
        return redirect('entity-list', entity=entity)
    return render(
        request,
        'records/entity_form.html',
        {'form': form, 'title': f'Edit {model._meta.verbose_name}'},
    )


def entity_delete(request, entity, pk):
    model, title = get_entity(entity)
    record = get_object_or_404(model, pk=pk)
    if request.method == 'POST':
        record.delete()
        return redirect('entity-list', entity=entity)
    return render(
        request,
        'records/entity_confirm_delete.html',
        {'record': record, 'title': f'Delete {model._meta.verbose_name}'},
    )
