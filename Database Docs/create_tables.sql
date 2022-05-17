CREATE TABLE Users(
   user_id INT AUTO_INCREMENT PRIMARY KEY,
   user_name VARCHAR(40) NOT NULL,
   password VARCHAR(255) NOT NULL,
   email VARCHAR(255) NOT NULL,
   first_name VARCHAR(255) NOT NULL,
   last_name VARCHAR(255) NOT NULL,
   college VARCHAR(255),
   department VARCHAR(40),
   major VARCHAR(40),
   graduation_class INT,
   sex CHAR
);


CREATE TABLE Courses(
   id INT AUTO_INCREMENT PRIMARY KEY,
   course_number INT NOT NULL,
   subject VARCHAR(40),
   title VARCHAR(1024) NOT NULL,
   description TEXT
);


CREATE TABLE Sections(
   crn INT,
   course INT,
   students_count INT,
   average_gpa REAL,
   year INT,
   semester VARCHAR(255),
   professor VARCHAR(255),
   PRIMARY KEY(crn, course),
   FOREIGN KEY(course) REFERENCES Courses(id) ON DELETE CASCADE ON UPDATE CASCADE
);


CREATE TABLE Comments(
   id INT AUTO_INCREMENT PRIMARY KEY,
   commenter INT NOT NULL,
   course INT NOT NULL,
   comment VARCHAR(2048) NOT NULL,
   comment_time DATETIME,
   likes INT,
   dislikes INT,
   reply INT,
   FOREIGN KEY (commenter) REFERENCES Users(user_id) ON DELETE CASCADE ON UPDATE CASCADE,
   FOREIGN KEY (course) REFERENCES Courses(id) ON DELETE CASCADE ON UPDATE CASCADE,
   FOREIGN KEY (reply) REFERENCES Comments(id) ON DELETE CASCADE ON UPDATE CASCADE
);


CREATE TABLE Ratings(
   id INT AUTO_INCREMENT PRIMARY KEY,
   course INT NOT NULL,
   rater INT NOT NULL,
   overall_quality INT NOT NULL,
   professor INT NOT NULL,
   workload INT NOT NULL,
   rubric INT NOT NULL,
   difficulty INT NOT NULL,
   grade_Rceived CHAR NOT NULL,
   FOREIGN KEY (course) REFERENCES Courses(id) ON DELETE CASCADE ON UPDATE CASCADE,
   FOREIGN KEY (rater) REFERENCES Users(user_id) ON DELETE CASCADE ON UPDATE CASCADE
);


CREATE TABLE Likes(
   user INT,
   comment INT,
   isLike BOOLEAN,
   time DATETIME,
   PRIMARY KEY (user, comment),
   FOREIGN KEY (user) REFERENCES Users(user_id) ON DELETE CASCADE ON UPDATE CASCADE,
   FOREIGN KEY (comment) REFERENCES Comments(id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Enrollments(
    student INT,
    crn INT,
    course_id INT,
    grade CHAR,
    credits INT,
    PRIMARY KEY (student, crn, course_id),
    FOREIGN KEY (student) REFERENCES Users(user_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (crn) REFERENCES Sections(crn) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (course_id) REFERENCES Sections(course) ON DELETE CASCADE ON UPDATE CASCADE
);