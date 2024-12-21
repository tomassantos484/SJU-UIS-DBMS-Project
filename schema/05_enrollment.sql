USE `StJohnsUIS`;

DROP TABLE IF EXISTS Enrollment;

CREATE TABLE Enrollment (
    student_xnumber VARCHAR(9) NOT NULL,
    section_id INT NOT NULL,
    crn_number INT NOT NULL,
    grade VARCHAR(2) DEFAULT NULL,
    enrollment_date DATE NOT NULL,
    
    PRIMARY KEY (student_xnumber, section_id, crn_number),
    KEY section_id (section_id, crn_number),

    CONSTRAINT fk_enrollment_student
    FOREIGN KEY (student_xnumber) 
    REFERENCES Student(student_xnumber)
    ON DELETE CASCADE    -- If student is deleted, remove their enrollments
    ON UPDATE CASCADE,   -- If student X-number changes, update enrollments
    
    CONSTRAINT fk_enrollment_section
    FOREIGN KEY (section_id, crn_number) 
    REFERENCES Section(section_id, crn_number)
    ON DELETE CASCADE    -- If section is deleted, remove related enrollments
    ON UPDATE CASCADE,   -- If section details change, update enrollments

    CONSTRAINT chk_grade CHECK (
        grade IN ('A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D', 'D-', 'F')
    )
);

DELIMITER $$

CREATE TRIGGER validate_student_xnumber
BEFORE INSERT ON Enrollment
FOR EACH ROW
BEGIN
    IF NEW.student_xnumber NOT REGEXP '^X[0-9]{8}$' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Invalid student_xnumber format.';
    END IF;
END$$

DELIMITER ;
