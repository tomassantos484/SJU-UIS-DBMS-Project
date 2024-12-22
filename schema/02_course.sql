USE `StJohnsUIS`;

DROP TABLE IF EXISTS Course;

CREATE TABLE Course (
    crn_number INT NOT NULL,
    course_number VARCHAR(10) NOT NULL,
    course_title VARCHAR(100) NOT NULL,
    course_description VARCHAR(255) NOT NULL,
    instructor_xnumber VARCHAR(9) NOT NULL,
    credits TINYINT NOT NULL,
    department VARCHAR(100) NOT NULL,
    PRIMARY KEY (crn_number),
    
    -- Foreign Keys
    CONSTRAINT fk_course_instructor 
    FOREIGN KEY (instructor_xnumber) 
    REFERENCES Instructor(instructor_xnumber)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,

    -- Constraints
    CONSTRAINT chk_crn_term CHECK (
        (crn_number BETWEEN 70000 AND 79999) OR  -- Fall courses
        (crn_number BETWEEN 10000 AND 19999)     -- Spring courses
    ),
    CONSTRAINT chk_credits CHECK (credits BETWEEN 1 AND 4)
);
