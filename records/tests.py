from django.test import TestCase
from django.urls import reverse

from .models import Department


class HomeViewTests(TestCase):
    def test_home_page_loads(self):
        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'University Records')


class DepartmentCrudTests(TestCase):
    def test_department_lifecycle(self):
        create_response = self.client.post(
            reverse('entity-create', args=['departments']),
            {'name': 'Computer Science', 'faculty': 'Science'},
        )
        department = Department.objects.get(name='Computer Science')
        self.assertRedirects(create_response, reverse('entity-list', args=['departments']))

        update_response = self.client.post(
            reverse('entity-update', args=['departments', department.pk]),
            {'name': 'Computing', 'faculty': 'Science'},
        )
        department.refresh_from_db()
        self.assertEqual(department.name, 'Computing')
        self.assertRedirects(update_response, reverse('entity-list', args=['departments']))

        delete_response = self.client.post(
            reverse('entity-delete', args=['departments', department.pk]),
        )
        self.assertFalse(Department.objects.exists())
        self.assertRedirects(delete_response, reverse('entity-list', args=['departments']))
