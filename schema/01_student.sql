CREATE TABLE Student (
    student_xnumber VARCHAR(9) NOT NULL,
    stormcard_id VARCHAR(8) NOT NULL,
    library_id VARCHAR(14) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    date_of_birth DATE NOT NULL,
    college VARCHAR(100) NOT NULL,
    major VARCHAR(50) NOT NULL,
    gpa DECIMAL(3,2) NOT NULL,
    gender VARCHAR(6) NOT NULL,
    email VARCHAR(100) NOT NULL,
    phone_number VARCHAR(15) NOT NULL,
    date_of_admission DATE NOT NULL,
    year_of_graduation DATE NOT NULL,
    PRIMARY KEY (student_xnumber),
    UNIQUE KEY stormcard_id (stormcard_id),
    UNIQUE KEY library_id (library_id),
    UNIQUE KEY email (email),
    CONSTRAINT chk_college CHECK (
        college IN (
            'St. John''s College of Liberal Arts and Sciences',
            'The School of Education',
            'The Peter J. Tobin College of Business',
            'College of Pharmacy and Health Sciences',
            'The Lesley H. and William L. Collins College of Professional Studies',
            'St. John''s School of Law'
        )
    ),
    CONSTRAINT chk_email_format CHECK (
        REGEXP_LIKE(email, '^[a-z]+\.[a-z]+[0-9]{2}@my\.stjohns\.edu$')
    ),
    CONSTRAINT chk_gender CHECK (
        gender IN ('Male', 'Female')
    ),
    CONSTRAINT chk_gpa CHECK (
        gpa >= 0.00 AND gpa <= 4.00
    ),
    CONSTRAINT chk_phone_format CHECK (
        REGEXP_LIKE(phone_number, '^\+?[0-9]{10,14}$')
    ),
    CONSTRAINT chk_stormcard_id CHECK (
        REGEXP_LIKE(stormcard_id, '^[0-9]{8}$')
    ),
    CONSTRAINT chk_student_xnumber CHECK (
        REGEXP_LIKE(student_xnumber, '^X[0-9]{8}$')
    ),
    CONSTRAINT chk_year_graduation CHECK (
        year_of_graduation > date_of_admission
        AND year_of_graduation <= DATE_ADD(date_of_admission, INTERVAL 8 YEAR)
    )
);

DELIMITER $$

CREATE TRIGGER trg_check_dob_before_insert
BEFORE INSERT ON Student
FOR EACH ROW
BEGIN
    IF NEW.date_of_birth > CURDATE() THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Date of birth cannot be in the future.';
    END IF;
END$$

DELIMITER ;

DELIMITER $$

CREATE TRIGGER trg_check_date_of_admission_before_insert
BEFORE INSERT ON Student
FOR EACH ROW
BEGIN
    IF NEW.date_of_admission > CURDATE() THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Date of admission cannot be in the future.';
    END IF;
END$$

DELIMITER ;

-- Add cascade rules for Student deletion/updates
ALTER TABLE Enrollment
    ADD CONSTRAINT fk_enrollment_student
    FOREIGN KEY (student_xnumber) 
    REFERENCES Student(student_xnumber)
    ON DELETE CASCADE
    ON UPDATE CASCADE;
