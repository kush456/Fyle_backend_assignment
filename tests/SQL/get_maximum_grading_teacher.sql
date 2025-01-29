SELECT teacher_id
FROM assignments 
WHERE state = 'GRADED'
GROUP BY teacher_id
ORDER BY COUNT(*) DESC
LIMIT 1;