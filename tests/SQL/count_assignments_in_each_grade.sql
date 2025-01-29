SELECT grade, COUNT(*)
FROM assignments
WHERE state = 'GRADED'
GROUP BY grade;