BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "user" (
	"name"	VARCHAR(100) NOT NULL,
	"username"	VARCHAR(80) NOT NULL,
	"userID"	VARCHAR(6) NOT NULL,
	"password"	VARCHAR(80) NOT NULL,
	"email"	VARCHAR(120) NOT NULL,
	"experience"	INTEGER NOT NULL,
	"github"	VARCHAR(500),
	"picture"	BLOB,
	UNIQUE("username"),
	UNIQUE("email"),
	PRIMARY KEY("userID")
);
CREATE TABLE IF NOT EXISTS "project" (
	"name"	VARCHAR(100) NOT NULL,
	"projID"	VARCHAR(6) NOT NULL,
	"description"	VARCHAR(500) NOT NULL,
	"difficulty"	INTEGER NOT NULL,
	"github"	VARCHAR(500),
	"creatorID"	VARCHAR(6),
	FOREIGN KEY("creatorID") REFERENCES "user"("userID"),
	PRIMARY KEY("projID")
);
CREATE TABLE IF NOT EXISTS "interested_in" (
	"userID"	VARCHAR(6) NOT NULL,
	"areaOfInterest"	VARCHAR(80) NOT NULL,
	FOREIGN KEY("userID") REFERENCES "user"("userID"),
	PRIMARY KEY("userID","areaOfInterest")
);
CREATE TABLE IF NOT EXISTS "codes_in" (
	"userID"	VARCHAR(6) NOT NULL,
	"Language"	VARCHAR(80) NOT NULL,
	FOREIGN KEY("userID") REFERENCES "user"("userID"),
	PRIMARY KEY("userID","Language")
);
CREATE TABLE IF NOT EXISTS "workedOn" (
	"userID"	VARCHAR(6),
	"projID"	VARCHAR(6),
	FOREIGN KEY("projID") REFERENCES "project"("projID"),
	FOREIGN KEY("userID") REFERENCES "user"("userID")
);
CREATE TABLE IF NOT EXISTS "worksIn" (
	"userID"	VARCHAR(6),
	"projID"	VARCHAR(6),
	FOREIGN KEY("userID") REFERENCES "user"("userID"),
	FOREIGN KEY("projID") REFERENCES "project"("projID")
);
CREATE TABLE IF NOT EXISTS "proj_lang" (
	"projID"	VARCHAR(6) NOT NULL,
	"Language"	VARCHAR(80) NOT NULL,
	FOREIGN KEY("projID") REFERENCES "project"("projID"),
	PRIMARY KEY("projID","Language")
);
CREATE TABLE IF NOT EXISTS "project_areas" (
	"projID"	VARCHAR(6) NOT NULL,
	"areaOfInterest"	VARCHAR(80) NOT NULL,
	FOREIGN KEY("projID") REFERENCES "project"("projID"),
	PRIMARY KEY("projID","areaOfInterest")
);
CREATE TABLE IF NOT EXISTS "applied_to" (
	"userID"	VARCHAR(6) NOT NULL,
	"projID"	VARCHAR(6) NOT NULL,
	"pendingConfirmation"	BOOLEAN NOT NULL,
	"accepted"	BOOLEAN NOT NULL,
	FOREIGN KEY("projID") REFERENCES "project"("projID"),
	FOREIGN KEY("userID") REFERENCES "user"("userID"),
	PRIMARY KEY("userID","projID")
);
INSERT INTO "user" VALUES ('Rohan','ro','U12345','ropass','rohanmitra8@gmail.com',4,'www.github.com',NULL);
INSERT INTO "user" VALUES ('Ali Soufi','AliWali','U11223','alipass','alisoufi7@gmail.com',2,'www.github.com',NULL);
INSERT INTO "user" VALUES ('Dara','DRaw','U11111','Dpass','dara7varam@gmail.com',1,'www.github.com',NULL);
INSERT INTO "user" VALUES ('Issa','isss','U82222','issapass','IssaNajjar@gmail.com',0,'www.github.com',NULL);
INSERT INTO "project" VALUES ('ML Sample Project','P84282','Quisque eget vehicula tortor. Pellentesque iaculis turpis magna, at rutrum felis scelerisque id. Sed pharetra enim eros, sit amet cursus metus laoreet vitae. Praesent nec mollis nulla, et pulvinar mi. Mauris porttitor, ligula ac blandit molestie, diam dui tempor augue, mollis condimentum nisi mauris eu mauris.',3,'www.github.com','U12345');
INSERT INTO "project" VALUES ('Programming in Games Project','P93882','Morbi mollis magna sit amet mauris rutrum malesuada. Integer tortor nisi, mollis sed vestibulum sit amet, consequat eu erat. ',1,'www.github.com','U11223');
INSERT INTO "project" VALUES ('WoWo Game Design Graphics','P98387','Maecenas diam augue, bibendum et commodo ac, convallis sed dui. Fusce fermentum enim non urna accumsan dictum. Proin tempor pharetra leo eu tincidunt.',5,'www.github.com','U11111');
INSERT INTO "project" VALUES ('Anime Neural Networks','P88772','Cras a enim vitae turpis finibus cursus sit amet non risus. Quisque nulla eros, luctus sed lorem eget, fringilla facilisis lectus. Mauris quis commodo mauris, eu tempor turpis.',2,'www.github.com','U11111');
INSERT INTO "project" VALUES ('Wonky Networking LMAOO','P56352','Curabitur ornare metus ut mauris bibendum vulputate. Maecenas ac condimentum libero. Nam magna nulla, scelerisque eu maximus euismod, imperdiet sit amet tortor.',2,'www.github.com','U11223');
INSERT INTO "project" VALUES ('UML Design for AI','P88372','Phasellus dictum maximus nisi, vitae interdum mi volutpat et. Vivamus placerat pretium metus vel tincidunt. Donec vestibulum tortor non porttitor ultrices.',4,'www.github.com','U12345');
INSERT INTO "project" VALUES ('Homework Help?!','P55442','enean convallis risus in massa imperdiet mattis. Sed sem nunc, consectetur id ipsum eu, sagittis scelerisque mi. Maecenas non imperdiet felis.',4,'www.github.com','U82222');
INSERT INTO "interested_in" VALUES ('U82222','Machine Learning');
INSERT INTO "interested_in" VALUES ('U11111','Artificial Intelligence');
INSERT INTO "interested_in" VALUES ('U11223','Back-End Development');
INSERT INTO "interested_in" VALUES ('U82222','Computer Networks');
INSERT INTO "interested_in" VALUES ('U12345','Computer Graphics');
INSERT INTO "interested_in" VALUES ('U11223','Computer Systems');
INSERT INTO "interested_in" VALUES ('U82222','Cybersecurity');
INSERT INTO "interested_in" VALUES ('U12345','Cryptography');
INSERT INTO "interested_in" VALUES ('U11111','Cloud Computing');
INSERT INTO "interested_in" VALUES ('U82222','Computer Human Interface');
INSERT INTO "interested_in" VALUES ('U11223','Data Science');
INSERT INTO "interested_in" VALUES ('U11111','Full-Stack Development');
INSERT INTO "interested_in" VALUES ('U82222','Front-End Development');
INSERT INTO "interested_in" VALUES ('U12345','Game Design');
INSERT INTO "interested_in" VALUES ('U11223','Information Security');
INSERT INTO "interested_in" VALUES ('U82222','Programming Languages');
INSERT INTO "interested_in" VALUES ('U12345','Mobile Application Design');
INSERT INTO "interested_in" VALUES ('U11223','Neural Networks');
INSERT INTO "interested_in" VALUES ('U82222','Software Engineering');
INSERT INTO "interested_in" VALUES ('U11111','Theory');
INSERT INTO "codes_in" VALUES ('U11111','C');
INSERT INTO "codes_in" VALUES ('U11223','C#');
INSERT INTO "codes_in" VALUES ('U82222','C++');
INSERT INTO "codes_in" VALUES ('U12345','Objective C');
INSERT INTO "codes_in" VALUES ('U11223','Erlang');
INSERT INTO "codes_in" VALUES ('U82222','Git');
INSERT INTO "codes_in" VALUES ('U12345','Go');
INSERT INTO "codes_in" VALUES ('U11111','Haskell');
INSERT INTO "codes_in" VALUES ('U82222','HTML');
INSERT INTO "codes_in" VALUES ('U11223','Java');
INSERT INTO "codes_in" VALUES ('U11111','Javascript');
INSERT INTO "codes_in" VALUES ('U82222','LaTeX');
INSERT INTO "codes_in" VALUES ('U12345','Lisp');
INSERT INTO "codes_in" VALUES ('U82222','ASP');
INSERT INTO "codes_in" VALUES ('U11223','MATLAB');
INSERT INTO "codes_in" VALUES ('U82222','Perl');
INSERT INTO "codes_in" VALUES ('U12345','PHP');
INSERT INTO "codes_in" VALUES ('U11223','Python');
INSERT INTO "codes_in" VALUES ('U82222','R');
INSERT INTO "codes_in" VALUES ('U11111','SQL');
INSERT INTO "workedOn" VALUES ('U12345','P84282');
INSERT INTO "workedOn" VALUES ('U11223','P93882');
INSERT INTO "workedOn" VALUES ('U11111','P84282');
INSERT INTO "workedOn" VALUES ('U11111','P98387');
INSERT INTO "workedOn" VALUES ('U82222','P56352');
INSERT INTO "workedOn" VALUES ('U82222','P88372');
INSERT INTO "workedOn" VALUES ('U82222','P55442');
INSERT INTO "worksIn" VALUES ('U12345','P93882');
INSERT INTO "worksIn" VALUES ('U12345','P98387');
INSERT INTO "worksIn" VALUES ('U12345','P88372');
INSERT INTO "worksIn" VALUES ('U12345','P55442');
INSERT INTO "worksIn" VALUES ('U12345','P56352');
INSERT INTO "project_areas" VALUES ('P84282','Machine Learning');
INSERT INTO "project_areas" VALUES ('P93882','Artificial Intelligence');
INSERT INTO "project_areas" VALUES ('P98387','Back-End Development');
INSERT INTO "project_areas" VALUES ('P84282','Computer Networks');
INSERT INTO "project_areas" VALUES ('P93882','Computer Graphics');
INSERT INTO "project_areas" VALUES ('P88772','Computer Systems');
INSERT INTO "project_areas" VALUES ('P84282','Cybersecurity');
INSERT INTO "project_areas" VALUES ('P98387','Cryptography');
INSERT INTO "project_areas" VALUES ('P56352','Cloud Computing');
INSERT INTO "project_areas" VALUES ('P88372','Computer Human Interface');
INSERT INTO "project_areas" VALUES ('P84282','Data Science');
INSERT INTO "project_areas" VALUES ('P55442','Theory');
COMMIT;
