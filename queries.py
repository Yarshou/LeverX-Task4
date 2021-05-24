QUERY_INITIAL = """
  CREATE TABLE Rooms(
    id INTEGER PRIMARY KEY,
    name VARCHAR(20)
);

CREATE TABLE Students(
    id INTEGER PRIMARY KEY,
    birthday datetime,
    name VARCHAR(100),
    room INTEGER,
    sex VARCHAR(1),
    FOREIGN KEY (room)  REFERENCES rooms (id)
    );
"""

# This query selects the number of students for each room
QUERY_1 = """SELECT rooms.id, rooms.name, COUNT(students.id) AS students
        FROM rooms JOIN students ON rooms.id = students.room
        GROUP BY rooms.id, rooms.name;"""

# This query selects 5 rooms that have the smallest average student age
QUERY_2 = """SELECT id, name FROM (SELECT rooms.id, rooms.name, AVG(now() - students.birthday) AS age
        FROM rooms JOIN students ON rooms.id = students.room
        GROUP BY rooms.id, rooms.name
        ORDER BY age ASC
        LIMIT 5) AS tmp;"""

# This query selects 5 rooms with the largest age difference between students
QUERY_3 = """SELECT id, name FROM (SELECT id, name, MAX(age)
        FROM (SELECT rooms.id AS id, rooms.name AS name, MAX(students.birthday) - MIN(students.birthday) AS age
        FROM rooms JOIN students ON rooms.id = students.room
        GROUP BY rooms.id, rooms.name) AS nothing
        GROUP BY id, NAME
        ORDER BY age DESC
        LIMIT 5) AS tmp;"""

# This query selects rooms with students of different sexes
QUERY_4 = """SELECT DISTINCT rooms.id, students.sex as "sex1", tmp.sex as "sex2" FROM students
        JOIN rooms ON students.room = rooms.id
        JOIN (SELECT sex, rooms.id FROM students JOIN rooms ON students.room = rooms.id ) AS tmp ON tmp.id = rooms.id
        WHERE students.sex = 'M' AND tmp.sex = 'F';"""

# Index is created for the student's date of birth, as this is the most commonly used field.
# For fields such as id in the Rooms table and the room field in the Student table, indexes
# are created by default. That is why theres no need in creating indexes for those fields.
QUERY_FOR_INDEX = "CREATE INDEX birthday ON students(birthday);"
