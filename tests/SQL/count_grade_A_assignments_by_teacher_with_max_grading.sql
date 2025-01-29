-- Get the count of grade 'A' assignments for the teacher who has graded the most assignments
SELECT COUNT(*)
FROM assignments
WHERE grade = 'A' 
AND teacher_id = :teacher_id;
