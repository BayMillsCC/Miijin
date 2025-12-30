
--CREATE DATABASE miijinprod;


\c miijinprod

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

CREATE ROLE miijin_app
WITH
    LOGIN
    PASSWORD 'SUPERSECRETPASSWORD'
    NOSUPERUSER
    NOCREATEDB
    NOCREATEROLE
    NOINHERIT;

GRANT CONNECT ON DATABASE miijinprod TO miijin_app;

GRANT USAGE ON SCHEMA miijinprod TO miijin_app;

GRANT
    SELECT,
    INSERT
ON TABLE
    miijinprod.studentlunchrecords,
    miijinprod.employeelunchrecords
TO miijin_app;

GRANT USAGE, SELECT
ON ALL SEQUENCES IN SCHEMA miijinprod
TO miijin_app;

ALTER DEFAULT PRIVILEGES IN SCHEMA miijinprod
GRANT SELECT, INSERT ON TABLES TO miijin_app;

ALTER DEFAULT PRIVILEGES IN SCHEMA miijinprod
GRANT USAGE, SELECT ON SEQUENCES TO miijin_app;

