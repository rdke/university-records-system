from django.forms import modelform_factory
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from .models import Course, Department, Lecturer, Programme, ResearchProject, Staff, Student


ENTITIES = {
    'departments': (Department, 'Departments'),
    'programmes': (Programme, 'Programmes'),
    'lecturers': (Lecturer, 'Lecturers'),
    'students': (Student, 'Students'),
    'staff': (Staff, 'Staff'),
    'courses': (Course, 'Courses'),
    'projects': (ResearchProject, 'Research Projects'),
}


def get_entity(entity):
    try:
        return ENTITIES[entity]
    except KeyError as error:
        raise Http404 from error


def home(request):
    return render(request, 'records/home.html', {'entities': ENTITIES})


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
