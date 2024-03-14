-- get the count of all tasks in each project, order by tasks count descending

SELECT public.projects.name, COUNT(public.tasks.name) as task_amount
FROM public.projects
INNER JOIN public.tasks 
ON public.tasks.project_id = public.projects.id
GROUP BY public.projects.name
ORDER BY task_amount DESC;