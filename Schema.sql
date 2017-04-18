-- Made some changes to Users and UserPermissions to get them to work.
-- Adnan Dossaji
CREATE TABLE IF NOT EXISTS Users (
  id           INTEGER         PRIMARY KEY,
  name         VARCHAR(100)            UNIQUE NOT NULL,
  email        VARCHAR(320)    UNIQUE NOT NULL,
  password     VARCHAR(100)            NOT NULL,
  perms        INTEGER         NOT NULL,
  active       BOOLEAN         NOT NULL,

  CONSTRAINT fk_perms FOREIGN KEY (perms) REFERENCES UserPermissions (id)
);

CREATE TABLE IF NOT EXISTS UserPermissions
(
  id              INTEGER     UNIQUE NOT NULL,
  alias           VARCHAR(100)        UNIQUE NOT NULL,
  whatIf          BOOLEAN     NOT NULL,
  search          BOOLEAN     NOT NULL,
  edit_user       BOOLEAN     NOT NULL,
  edit_course     BOOLEAN     NOT NULL,

  CONSTRAINT pk_id PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS Searches
(
    search_id               INTEGER UNIQUE NOT NULL,
    search_name             VARCHAR(100)    NOT NULL,
    search_start_date       VARCHAR(100)    NOT NULL,
    search_amount_courses   INTEGER NOT NULL,
    search_delivery         VARCHAR(100)    NOT NULL,
    search_consentration    VARCHAR(100)    NOT NULL,
    user_id                 VARCHAR(100)    NOT NULL,

    CONSTRAINT pk_search_id PRIMARY KEY (search_id),
    CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

CREATE TABLE IF NOT EXISTS Courses
(
    course_id                       INTEGER UNIQUE NOT NULL,
    course_name                     VARCHAR(100)    UNIQUE NOT NULL,
    course_prereq                   VARCHAR(100),
    course_credits                  INTEGER NOT NULL,
    course_description              VARCHAR(100),
    course_sylybus                  VARCHAR(100),
    course_quarter_offered          VARCHAR(100)    NOT NULL,
    course_delivery_method          VARCHAR(100)    NOT NULL,

    CONSTRAINT pk_course_id PRIMARY KEY (course_id)
);

CREATE TABLE IF NOT EXISTS CoursesTaken
(

   course_id     INTEGER          UNIQUE NOT NULL,
   user_id       INTEGER          UNIQUE NOT NULL,
   course_status CHARACTER(1)     NOT NULL,

   CONSTRAINT pk_taken_id PRIMARY KEY (course_id, user_id),
   CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES Users(user_id),
   CONSTRAINT fk_course_id FOREIGN KEY (course_id) REFERENCES Courses(course_id)
)

CREATE TABLE IF NOT EXISTS Degrees
(
    degree_id               INTEGER    UNIQUE NOT NULL,
    degree_major            VARCHAR(100)    UNIQUE NOT NULL,
    degree_concentration    VARCHAR(100)    NOT NULL,

    CONSTRAINT pk_degree_id PRIMARY KEY (degree_id),
    CONSTRAINT fk_ FOREIGN KEY (consentration_name) REFERENCES Courses(course_consentration)
);

CREATE TABLE IF NOT EXISTS DegreeCourse
(

   degree_id       INTEGER          UNIQUE NOT NULL,
   course_id       INTEGER          UNIQUE NOT NULL,

   CONSTRAINT pk_degree_course_id PRIMARY KEY (degree_id, course_id),
   CONSTRAINT fk_degree_id FOREIGN KEY (degree_id) REFERENCES Degrees(degree_id),
   CONSTRAINT fk_course_id FOREIGN KEY (course_id) REFERENCES Courses(course_id)
)
