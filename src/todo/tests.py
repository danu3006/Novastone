from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Task


class TaskMethodTests(TestCase):

    def setUp(self):
        # Create two user objects
        user1 = User.objects.create(username='user1', password='user1')
        user2 = User.objects.create(username='user2', password='user2')

        # Create two task objects
        self.user1_task = Task.objects.create(id=1, name='Task 1', description='Test task one.', user=user1,
                                              status=False)
        self.user2_task = Task.objects.create(id=2, name='Task 2', description='Test task two.', user=user2,
                                              status=False)
        # Login as user1.
        self.client.login(username='user1', password='user')

    def test_user_edit_and_delete_another_user_task(self):
        """
        Test if 'user1' can edit or delete a task authored by 'user2'.
        """
        # Send POST request to edit  'other_user_task' to set 'status' to True
        # Send POST request to delete the 'other_user_task'. Then check 'status_code'.
        response_edit = self.client.patch(reverse('todo:task-update', kwargs={'pk': self.user2_task.pk}), {
            'status': True,
        })
        response_delete = self.client.delete(reverse('todo:task-delete', kwargs={'pk': self.user2_task.pk}))
        self.assertEqual(response_edit.status_code, 302)
        self.assertEqual(response_delete.status_code, 302)

        # Get up to date data about 'other_user_task' and check if the 'status' is still false.
        # At the same time if delete post is successful.
        self.user2_task.refresh_from_db()
        self.assertEqual(self.user2_task.status, False)

    def test_edit_status_undone_and_done_by_is_none(self):
        # Set 'status' to True and 'done_by' to user2
        self.user1_task.done_by = User.objects.get(pk=2)
        self.user1_task.status = True

        # Send POST request to set JUST 'status' to False.
        response = self.client.patch(reverse('todo:task-update', kwargs={'pk': self.user1_task.pk}), {
            'status': False,
        })

        # Check response code of POST
        self.assertEqual(response.status_code, 302)

        # Check the 'status' is False and 'done_by' is None
        self.user1_task.refresh_from_db()
        self.assertEqual(self.user1_task.status, False)
        self.assertEqual(self.user1_task.done_by, None)
