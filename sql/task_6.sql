-- get the list of tasks with duplicate names. Order alphabetically

SELECT name
FROM public.tasks
GROUP BY name
HAVING COUNT(name) > 1;