-- get the list of al projects containing the 'a' letter in the middle of the name, and show the tasks count near each project. 
-- Mention that there can exist projects without tasks and tasks with project_id= NULL

SELECT public.projects.name, COUNT(public.tasks.name) as tasks_amount
FROM public.projects
INNER JOIN public.tasks 
ON public.tasks.project_id = public.projects.id
WHERE public.projects.name LIKE '%a%'
GROUP BY public.projects.name;