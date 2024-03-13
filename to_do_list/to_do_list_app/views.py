from django.views.generic.base import TemplateView, View
from .models import Project, Task
from django.shortcuts import redirect
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from datetime import date


class Home(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        user = self.request.user
        projects = Project.objects.filter(user=user).order_by('-created_at')
        projects_tasks = {}
        for p in projects:
            projects_tasks[p] = Task.objects.filter(project=p).order_by('-priority')
        context['projects'] = projects_tasks
        context['today'] = date.today()
        return context


class AddToDoList(View):
    """Creating project"""
    def post(self, request) -> JsonResponse:
        data = request.POST
        user = self.request.user
        project = Project(user=user, name=data['name'])
        project.save()
        html_resp = render_to_string('project_template.html', {'project': project}, request=request)
        return JsonResponse(html_resp, safe=False)

    '''Redirect user in case of get request'''
    @staticmethod
    def get(request) -> redirect:
        return redirect('/')


class EditToDoList(View):
    """Post request for edit name"""
    def post(self, request, **kwargs) -> HttpResponse:
        project = Project.objects.get(id=self.kwargs['id'])
        project.name = request.POST.get(f'editProject{kwargs["id"]}')
        project.save()
        html_resp = render_to_string('project_name_template.html', {'project': project}, request=request)
        return HttpResponse(html_resp)

    """Deleting project"""
    @staticmethod
    def delete(request, **kwargs):
        project = Project.objects.get(id=kwargs['id'])
        project.delete()
        html_resp = ''
        if not Project.objects.all():
            html_resp = render_to_string('message.html')
        return HttpResponse(html_resp)

    """Patch request to replace name with edit form"""
    @staticmethod
    def patch(request, **kwargs) -> HttpResponse:
        project = Project.objects.get(id=kwargs['id'])
        html_resp = render_to_string('edit_project_form.html', {'project': project}, request=request)
        return HttpResponse(html_resp)

    '''Redirect user in case of get request'''
    @staticmethod
    def get(request, **kwargs) -> redirect:
        return redirect('/')


class AddTask(View):
    """Creating task"""
    def post(self, request, **kwargs) -> HttpResponse:
        data = request.POST
        project = Project.objects.get(id=kwargs['id'])
        tasks = Task.objects.filter(project=project).order_by('-priority')
        user = self.request.user
        """Condition for correct priority set"""
        if tasks:
            task = Task(project=project, name=data[f'task{project.id}'], user=user,
                        priority=tasks[0].priority+1)  # new task gets higher priority than the highest that was before
        else:
            task = Task(project=project, name=data[f'task{project.id}'], user=user)
        task.save()
        tasks = Task.objects.filter(project=project).order_by('-priority')
        html_resp = render_to_string('tasks_after_add_delete.html', {'tasks': tasks, 'p': task.project,
                                                                     'today': date.today()}, request=request)
        return HttpResponse(html_resp)

    '''Redirect user in case of get request'''
    @staticmethod
    def get(request, **kwargs) -> redirect:
        return redirect('/')


class EditTask(View):
    """Deleting task"""
    @staticmethod
    def delete(request, **kwargs) -> HttpResponse:
        task = Task.objects.get(id=kwargs['id'])
        task.delete()
        tasks = Task.objects.filter(project=task.project).order_by('-priority')
        """If any tasks left - send them, else massage about no tasks left"""
        if tasks:
            html_resp = render_to_string('tasks_after_add_delete.html', {'tasks': tasks, 'p': task.project,
                                                                         'today': date.today()}, request=request)
        else:
            html_resp = '<h3 class="text-secondary text-center my-3">No tasks yet.</h3>'
        return HttpResponse(html_resp)

    """Patch request to change task status"""
    @staticmethod
    def patch(request, **kwargs) -> HttpResponse:
        task = Task.objects.get(id=kwargs['id'])
        task.status = not task.status
        task.save()
        tasks = Task.objects.filter(project=task.project).order_by('-priority')
        html_resp = render_to_string('tasks_after_add_delete.html', {'tasks': tasks, 'p': task.project,
                                                                     'today': date.today()}, request=request)
        return HttpResponse(html_resp)

    """Post request for task edit"""
    def post(self, request, **kwargs) -> HttpResponse:
        data = request.POST
        task = Task.objects.get(id=self.kwargs['id'])
        tasks = [i for i in Task.objects.filter(project=task.project).order_by('-priority')]
        """Condition to check which action has to be done"""
        if data.get(f'upPriority{kwargs["id"]}') and len(tasks) > 1:  # priority + 1
            task_up = tasks[tasks.index(task)-1]
            task.priority, task_up.priority = task_up.priority, task.priority
            task.save()
            task_up.save()
        elif data.get(f'downPriority{kwargs["id"]}') and len(tasks) > 1:  # priority - 1
            if tasks.index(task) == len(tasks) - 1:
                task_down = tasks[0]
            else:
                task_down = tasks[tasks.index(task)+1]
            task.priority, task_down.priority = task_down.priority, task.priority
            task.save()
            task_down.save()
        elif data.get(f'editTaskName{kwargs["id"]}'):  # edit name and deadline
            task.name = data.get(f'editTaskName{kwargs["id"]}')
            if data.get(f'editTaskDeadline{kwargs["id"]}'):  # make date match format needed by Django
                year = data.get(f'editTaskDeadline{kwargs["id"]}')[6:]
                month = data.get(f'editTaskDeadline{kwargs["id"]}')[:2]
                day = data.get(f'editTaskDeadline{kwargs["id"]}')[3:5]
                task.deadline = f'{year}-{month}-{day}'
            task.save()
        tasks = Task.objects.filter(project=task.project).order_by('-priority')
        html_resp = render_to_string('tasks_after_add_delete.html', {'tasks': tasks, 'p': task.project,
                                                                     'today': date.today()}, request=request)
        return HttpResponse(html_resp)

    """Request to replace task data with edit form"""
    @staticmethod
    def put(request, **kwargs) -> HttpResponse:
        task = Task.objects.get(id=kwargs['id'])
        html_resp = render_to_string('task_edit_form.html', {'task': task, 'p': task.project},
                                     request=request)
        return HttpResponse(html_resp)

    '''Redirect user in case of get request'''
    @staticmethod
    def get(request, **kwargs) -> redirect:
        return redirect('/')
