-- get all statuses, not repeating, alphabetically ordered

SELECT DISTINCT status 
FROM public.tasks
ORDER BY status;