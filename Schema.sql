-- Made some changes to Users and UserPermissions to get them to work.
-- Adnan Dossaji
CREATE TABLE Users (
  id           INTEGER         AUTO INCREMENT UNIQUE NOT NULL,
  name         TEXT            UNIQUE NOT NULL,
  email        VARCHAR(320)    UNIQUE NOT NULL,
  password     TEXT            NOT NULL,
  perms        INTEGER         NOT NULL,
  active       BOOLEAN         NOT NULL,

  CONSTRAINT pk_id PRIMARY KEY (id),
  CONSTRAINT fk_perms FOREIGN KEY (perms) REFERENCES UserPermissions (id)
);

CREATE TABLE UserPermissions
(
  id              INTEGER     UNIQUE NOT NULL,
  alias           TEXT        UNIQUE NOT NULL,
  whatIf          BOOLEAN     NOT NULL,
  search          BOOLEAN     NOT NULL,
  edit_user       BOOLEAN     NOT NULL,
  edit_course     BOOLEAN     NOT NULL,

  CONSTRAINT pk_id PRIMARY KEY (id)
);

INSERT INTO UserPermissions (perms_id, perms_alias, perms_create, perms_delete)
VALUES
  (0, 'sysadmin',    1, 1, 1, 1),
  (1, 'staff',       1, 1, 0, 0),
  (2, 'student',     1, 0, 0, 0);

CREATE TABLE Searches
(
    search_id               INTEGER UNIQUE NOT NULL,
    search_name             TEXT    NOT NULL,
    search_start_date       TEXT    NOT NULL,
    search_amount_courses   INTEGER NOT NULL,
    search_delivery         TEXT    NOT NULL,
    search_consentration    TEXT    NOT NULL,
    user_id                 TEXT    NOT NULL,

    CONSTRAINT pk_search_id PRIMARY KEY (search_id),
    CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

CREATE TABLE Courses
(
    course_id                       INTEGER UNIQUE NOT NULL,
    course_name                     TEXT    UNIQUE NOT NULL,
    course_prereq                   TEXT,
    course_credits                  INTEGER NOT NULL,
    course_description              TEXT,
    course_sylybus                  TEXT,
    course_quarter_offered          TEXT    NOT NULL,
    course_delivery_method          TEXT    NOT NULL,

    CONSTRAINT pk_course_id PRIMARY KEY (course_id)
);

CREATE TABLE CoursesTaken
(

   course_id     INTEGER          UNIQUE NOT NULL,
   user_id       INTEGER          UNIQUE NOT NULL,
   course_status CHARACTER(1)     NOT NULL,

   CONSTRAINT pk_taken_id PRIMARY KEY (course_id, user_id),
   CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES Users(user_id),
   CONSTRAINT fk_course_id FOREIGN KEY (course_id) REFERENCES Courses(course_id)
)

CREATE TABLE Degrees
(
    degree_id               INTEGER    UNIQUE NOT NULL,
    degree_major            TEXT    UNIQUE NOT NULL,
    degree_concentration    TEXT    NOT NULL,

    CONSTRAINT pk_degree_id PRIMARY KEY (degree_id),
    CONSTRAINT fk_ FOREIGN KEY (consentration_name) REFERENCES Courses(course_consentration)
);

CREATE TABLE DegreeCourse
(

   degree_id       INTEGER          UNIQUE NOT NULL,
   course_id       INTEGER          UNIQUE NOT NULL,

   CONSTRAINT pk_degree_course_id PRIMARY KEY (degree_id, course_id),
   CONSTRAINT fk_degree_id FOREIGN KEY (degree_id) REFERENCES Degrees(degree_id),
   CONSTRAINT fk_course_id FOREIGN KEY (course_id) REFERENCES Courses(course_id)
)
