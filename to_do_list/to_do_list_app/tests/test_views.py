from django.test import RequestFactory, TestCase
from to_do_list_app.models import User, Task, Project
from to_do_list_app.views import AddToDoList, EditToDoList, AddTask, EditTask


class GetRequestsTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        User.objects.create_user(username='test_user', password='12345')

    def test_unauth_home_request(self) -> None:
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)

    def test_auth_home_request(self) -> None:
        self.client.login(username='test_user', password='12345')
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_edit_urls_request(self) -> None:
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
    def setUpTestData(cls) -> None:
        pass

    def setUp(self) -> None:
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='test_user', password='12345')
        project = Project(name='Project', user=self.user)
        project.save()

    def test_view(self) -> None:
        request = self.factory.post("/add_to_do_list", {'name': 'test'})
        request.user = self.user
        response = AddToDoList.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Project.objects.get(name='test'))

    def test_task_create(self) -> None:
        request = self.factory.post("/add_task/1", {'task1': 'test'})
        request.user = self.user
        response = AddTask.as_view()(request, id=1)
        project = Project.objects.get(id=1)
        tasks = Task.objects.filter(project=project)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(tasks[0].name, 'test')

    def test_delete_project(self) -> None:
        request = self.factory.delete("/edit_todolist/1")
        request.user = self.user
        response = EditToDoList.as_view()(request, id=1)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Project.objects.all())

    def test_edit_project(self) -> None:
        request = self.factory.post("/edit_todolist/1", {'editProject1': 'new_name'})
        request.user = self.user
        response = EditToDoList.as_view()(request, id=1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Project.objects.all()[0].name, 'new_name')

    def test_delete_task(self) -> None:
        project = Project.objects.get(id=1)
        task = Task(project=project, user=self.user, name='test')
        task.save()
        request = self.factory.delete("/edit_task/1")
        request.user = self.user
        response = EditTask.as_view()(request, id=1)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Task.objects.filter(project=project))

    def test_up_task_priority(self) -> None:
        project = Project.objects.get(id=1)
        for i in range(5):
            task = Task(project=project, user=self.user, name=f'test{i}', priority=i)
            task.save()
        request = self.factory.post("/edit_task/3", {'upPriority3': 1})
        request.user = self.user
        response = EditTask.as_view()(request, id=3)
        self.assertEqual(response.status_code, 200)
        task4 = Task.objects.get(id=4)
        task3 = Task.objects.get(id=3)
        self.assertTrue(task3.priority > task4.priority)

    def test_low_task_priority(self) -> None:
        project = Project.objects.get(id=1)
        for i in range(5):
            task = Task(project=project, user=self.user, name=f'test{i}', priority=i)
            task.save()
        request = self.factory.post("/edit_task/3", {'downPriority3': 1})
        request.user = self.user
        response = EditTask.as_view()(request, id=3)
        self.assertEqual(response.status_code, 200)
        task2 = Task.objects.get(id=2)
        task3 = Task.objects.get(id=3)
        self.assertTrue(task3.priority < task2.priority)

    def test_edit_task(self) -> None:
        project = Project.objects.get(id=1)
        task = Task(project=project, user=self.user, name='test')
        task.save()
        request = self.factory.post("/edit_task/1", {'editTaskName1': 'new_name', 'editTaskDeadline1': '03/30/2030'})
        request.user = self.user
        response = EditTask.as_view()(request, id=1)
        task = Task.objects.get(id=1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(task.name, 'new_name')
        self.assertEqual(task.deadline.strftime('%Y-%m-%d'), '2030-03-30')
