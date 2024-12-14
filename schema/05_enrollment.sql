CREATE TABLE Enrollment (
    -- Enrollment Table
    student_xnumber VARCHAR(9) NOT NULL,
    section_id INT NOT NULL,
    grade VARCHAR(2),
    enrollment_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    -- Constraints

    -- Ensures that a student can only be enrolled in a section once
    CONSTRAINT uq_student_section UNIQUE (student_xnumber, section_id),

    -- Ensures that the student X-number is in the correct format
    CONSTRAINT chk_enrollment_student_xnumber CHECK (student_xnumber REGEXP '^X[0-9]{8}$'),

    -- Ensures valid grade values
    CONSTRAINT chk_grade CHECK (grade IN ('A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D', 'D-', 'F')),

    -- Foreign Keys

    -- X-Number Foreign Key
    FOREIGN KEY (student_xnumber) REFERENCES Student(student_xnumber),

    -- Section ID Foreign Key
    FOREIGN KEY (section_id) REFERENCES Section(section_id)
);
