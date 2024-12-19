USE `StJohnsUIS`;

DROP TABLE IF EXISTS Course;

CREATE TABLE Course (
    crn_number INT NOT NULL,
    course_title VARCHAR(100) NOT NULL,
    course_description VARCHAR(255) NOT NULL,
    instructor_xnumber VARCHAR(9) NOT NULL,
    credits TINYINT NOT NULL,
    department VARCHAR(100) NOT NULL,
    course_number VARCHAR(10) DEFAULT NULL,

    -- Primary Key
    PRIMARY KEY (crn_number),

    -- Unique Constraint
    UNIQUE (course_title),

    -- Indexes
    KEY idx_course_title (course_title),
    KEY idx_instructor_xnumber (instructor_xnumber),
    KEY idx_department (department),

    -- Foreign Key
    FOREIGN KEY (instructor_xnumber) REFERENCES Instructor(instructor_xnumber),

    -- Check Constraints
    CONSTRAINT chk_crn_number CHECK (crn_number BETWEEN 10000 AND 99999),
    CONSTRAINT chk_credits CHECK (credits BETWEEN 1 AND 5)
) 
ENGINE=InnoDB 
DEFAULT CHARSET=utf8mb4 
COLLATE=utf8mb4_0900_ai_ci;
