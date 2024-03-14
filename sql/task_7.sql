-- get the list of tasks having several exact matches of both name and status, from the project 'Delivery’. Order by matches count

SELECT COUNT(public.tasks.name) as matches_count, public.tasks.name
FROM public.tasks
INNER JOIN public.projects ON public.tasks.project_id = public.projects.id
WHERE public.projects.name = 'Delivery' and (public.tasks.name, public.tasks.status) IN 
(SELECT public.tasks.name, public.tasks.status
FROM public.tasks
GROUP BY public.tasks.name, public.tasks.status
HAVING COUNT(*) >= 2)
GROUP BY public.tasks.name
ORDER BY matches_count;