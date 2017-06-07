PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE user_role (
	id INTEGER NOT NULL, 
	name VARCHAR(120) NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (id)
);
INSERT INTO "user_role" VALUES(1,'Admin');
INSERT INTO "user_role" VALUES(2,'Faculty');
INSERT INTO "user_role" VALUES(3,'Student');
CREATE TABLE course_type (
	id INTEGER NOT NULL, 
	name VARCHAR(120) NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (id)
);
CREATE TABLE course (
	id INTEGER NOT NULL, 
	subject VARCHAR(100) NOT NULL, 
	course_number INTEGER NOT NULL, 
	prereq VARCHAR(400) NOT NULL, 
	credits INTEGER NOT NULL, 
	day_of_week VARCHAR(100), 
	description VARCHAR(700), 
	quarter_offered VARCHAR(100) NOT NULL, 
	delivery_method INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (id)
);
CREATE TABLE term (
	id INTEGER NOT NULL, 
	name VARCHAR(120) NOT NULL, 
	year INTEGER NOT NULL, 
	offered VARCHAR(120) NOT NULL, 
	PRIMARY KEY (id, year), 
	UNIQUE (id), 
	UNIQUE (year)
);
CREATE TABLE user (
	id INTEGER NOT NULL, 
	name VARCHAR(120) NOT NULL, 
	email VARCHAR(120) NOT NULL, 
	password VARCHAR(30) NOT NULL, 
	role_id INTEGER NOT NULL, 
	active INTEGER NOT NULL, 
	program VARCHAR(120) NOT NULL, 
	concentration VARCHAR(120) NOT NULL, 
	start_term VARCHAR(10) NOT NULL, 
	start_year INTEGER NOT NULL, 
	delivery_type INTEGER NOT NULL, 
	classes_per_term INTEGER NOT NULL, 
	taken VARCHAR(120) NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (id), 
	UNIQUE (email), 
	FOREIGN KEY(role_id) REFERENCES user_role (id)
);
INSERT INTO "user" VALUES(1,'admin','admin@gmail.com','102137',1,0,'Information Systems','Software and Systems Development','Autumn',2017,'In-Class Only',1,'{}');
INSERT INTO "user" VALUES(2,'change','change@gmail.com','102137',3,0,'Information Systems','Software and Systems Development','Autumn',2017,'In-Class Only',1,'{}');
INSERT INTO "user" VALUES(3,'onemore','onemore@gmail.com','102137',2,0,'Computer Science','Multimedia','Spring',2017,'In-Class Only',1,'{}');
CREATE TABLE alembic_version (
	version_num VARCHAR(32) NOT NULL, 
	CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);
COMMIT;
