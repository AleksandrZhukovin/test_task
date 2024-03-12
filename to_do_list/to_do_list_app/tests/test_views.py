from django.test import RequestFactory, TestCase
from to_do_list_app.models import User, Task, Project
from to_do_list_app.views import Home


class GetRequestsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='test_user', password='12345')

    def test_unauth_home_request(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)

    def test_auth_home_request(self):
        self.client.login(username='test_user', password='12345')
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_edit_urls_request(self):
        response_0 = self.client.get('/add_to_do_list')
        response_1 = self.client.get('/edit_todolist/1')
        response_2 = self.client.get('/add_task/1')
        response_3 = self.client.get('/edit_task/1')
        self.assertEqual(response_0.status_code, 301)
        self.assertEqual(response_1.status_code, 301)
        self.assertEqual(response_2.status_code, 301)
        self.assertEqual(response_3.status_code, 301)


class DataSendRequestsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='test_user', password='12345')
        project = Project(name='Project1', user=user)
        project.save()
        # for i in range(10):
        #     task = Task(user=user, project=project, name=f'task{i}')
        #     task.save()

    def setUp(self) -> None:
        self.client.login(username='test_user', password='12345')
        response = self.client.post('/add_task/1', {'task1': 'test'}, follow=True)
        project = Project.objects.get(id=1)
        tasks = Task.objects.filter(project=project)
        print(tasks, response.status_code)


    def test_task_create(self):
        self.client.login(username='test_user', password='12345')
        response = self.client.post('/add_task/1', {'task1': 'test'}, follow=True)
        project = Project.objects.get(id=1)
        tasks = Task.objects.filter(project=project)
        # print(tasks, response.status_code)
        self.assertTrue(bool(project))