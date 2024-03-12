from django.test import RequestFactory, TestCase
from to_do_list_app.models import User, Task, Project
from to_do_list_app.views import Home
from django.contrib.auth import login


class ProjectTaskTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='test_user', password='12345')
        project = Project(name='Project1', user=user)
        project.save()
        for i in range(10):
            task = Task(user=user, project=project, name=f'task{i}')
            task.save()
