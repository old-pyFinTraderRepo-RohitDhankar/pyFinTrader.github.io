SELECT user.name, course.name
FROM `user`
INNER JOIN `course` on user.course = course.id;