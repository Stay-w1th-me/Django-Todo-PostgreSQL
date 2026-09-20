from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Task


class TaskTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="StrongTest123!"
        )

        self.other_user = User.objects.create_user(
            username="otheruser",
            password="StrongTest123!"
        )

        self.task = Task.objects.create(
            user=self.user,
            title="Test task",
            description="Test description"
        )

    def test_user_can_see_own_task(self):
        self.client.login(
            username="testuser",
            password="StrongTest123!"
        )

        response = self.client.get(reverse("task_list"))

        self.assertContains(response, "Test task")

    def test_user_cannot_see_other_users_task(self):
        self.client.login(
            username="otheruser",
            password="StrongTest123!"
        )

        response = self.client.get(reverse("task_list"))

        self.assertNotContains(response, "Test task")

    def test_user_can_toggle_own_task(self):
        self.client.login(
            username="testuser",
            password="StrongTest123!"
        )

        self.client.post(
            reverse("toggle_task", args=[self.task.id])
        )

        self.task.refresh_from_db()

        self.assertTrue(self.task.completed)