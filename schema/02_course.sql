CREATE TABLE Course (
    -- Course Table
    crn_number INT PRIMARY KEY NOT NULL,
    course_title VARCHAR(100) NOT NULL UNIQUE,
    course_description VARCHAR(255) NOT NULL,
    instructor_xnumber VARCHAR(9) NOT NULL,
    credits TINYINT NOT NULL CHECK (credits BETWEEN 1 AND 5),
    department VARCHAR(100) NOT NULL,

    -- Constraints
    CONSTRAINT chk_crn_number CHECK (crn_number BETWEEN 10000 AND 99999),

    -- Foreign Key for Instructor
    CONSTRAINT fk_instructor FOREIGN KEY (instructor_xnumber) 
    REFERENCES Instructor(instructor_xnumber)
);

-- Indexes
CREATE INDEX idx_course_title ON Course(course_title);
CREATE INDEX idx_instructor_xnumber ON Course(instructor_xnumber);
CREATE INDEX idx_department ON Course(department);
