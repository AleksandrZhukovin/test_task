-- get the tasks for al projects having the name beginning with "N" letter

SELECT public.projects.name, public.tasks.name
FROM public.projects
INNER JOIN public.tasks 
ON public.tasks.project_id = public.projects.id
WHERE public.projects.name LIKE 'N%';