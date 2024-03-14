-- get the list of project names having more than 10 tasks in status 'completed'. Order by project_id

SELECT COUNT(public.projects.name) as done_tasks,  public.projects.name
FROM public.projects
INNER JOIN public.tasks ON public.tasks.project_id = public.projects.id
WHERE public.tasks.status = 'completed'  
GROUP BY public.projects.name, public.projects.id
HAVING COUNT(*) > 10
ORDER BY public.projects.id;