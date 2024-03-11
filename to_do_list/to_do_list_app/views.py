from django.views.generic.base import TemplateView, View
from .models import Project, Task
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string


class Home(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        user = self.request.user
        projects = Project.objects.filter(user=user).order_by('-created_at')
        projects_tasks = {}
        for p in projects:
            projects_tasks[p] = Task.objects.filter(project=p).order_by('priority')
        context['projects'] = projects_tasks
        return context


class AddToDoList(View):
    def post(self, request) -> JsonResponse:
        data = request.POST
        user = self.request.user
        project = Project(user=user, name=data['name'])
        project.save()
        html_resp = render_to_string('project_template.html', {'project': project})
        return JsonResponse(html_resp, safe=False)


class EditToDoList(View):
    def post(self, request, **kwargs) -> HttpResponse:
        project = Project.objects.get(id=self.kwargs['id'])
        project.name = request.POST.get(f'editProject{kwargs["id"]}')
        project.save()
        html_resp = render_to_string('project_name_template.html', {'project': project}, request=request)
        return HttpResponse(html_resp)

    def delete(self, request, **kwargs):
        project = Project.objects.get(id=kwargs['id'])
        project.delete()
        projects = Project.objects.filter(user=self.request.user).order_by('-created_at')
        html_resp = render_to_string('projects_after_delete.html', {'projects': projects}, request=request)
        return HttpResponse(html_resp)

    def patch(self, request, **kwargs) -> HttpResponse:
        project = Project.objects.get(id=kwargs['id'])
        html_resp = render_to_string('edit_project_form.html', {'project': project}, request=request)
        return HttpResponse(html_resp)


class AddTask(View):
    def post(self, request, **kwargs) -> HttpResponse:
        data = request.POST
        project = Project.objects.get(id=kwargs['id'])
        tasks = Task.objects.filter(project=project).order_by('priority')
        user = self.request.user
        if tasks:
            task = Task(project=project, name=data[f'task{project.id}'], user=user,
                        priority=tasks.reverse()[0].priority+1)
        else:
            task = Task(project=project, name=data[f'task{project.id}'], user=user)
        task.save()
        html_resp = render_to_string('task_template.html', {'task': task})
        return HttpResponse(html_resp)
