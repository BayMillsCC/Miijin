CREATE SCHEMA IF NOT EXISTS miijinprod;

CREATE TABLE IF NOT EXISTS miijinprod.studentlunchrecords
(
    studentlunchid INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    studentid      INTEGER NOT NULL,
    timeidscanned  TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS miijinprod.employeelunchrecords
(
    employeelunchid INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    employeeid      INTEGER NOT NULL,
    timeidscanned   TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_studentlunch_time
ON miijinprod.studentlunchrecords (timeidscanned);

CREATE INDEX IF NOT EXISTS idx_studentlunch_student
ON miijinprod.studentlunchrecords (studentid);

CREATE INDEX IF NOT EXISTS idx_employeelunch_time
ON miijinprod.employeelunchrecords (timeidscanned);

CREATE INDEX IF NOT EXISTS idx_employeelunch_employee
ON miijinprod.employeelunchrecords (employeeid);
