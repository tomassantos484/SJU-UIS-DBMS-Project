USE `StJohnsUIS`;

DROP TABLE IF EXISTS Instructor;

CREATE TABLE Instructor (
    instructor_xnumber VARCHAR(9) NOT NULL,
    stormcard_id VARCHAR(8) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    date_of_birth DATE NOT NULL,
    college VARCHAR(100) NOT NULL,
    department VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    gender VARCHAR(6) NOT NULL,
    phone_number VARCHAR(15) NOT NULL,
    date_of_hire DATE NOT NULL,
    salary DECIMAL(10, 2) NOT NULL DEFAULT 50000.00,
    PRIMARY KEY (instructor_xnumber),
    UNIQUE (stormcard_id),
    UNIQUE (email),
    UNIQUE (phone_number),
    
    -- When an instructor's college changes, update related records
    CONSTRAINT fk_instructor_college
    FOREIGN KEY (college) 
    REFERENCES College(college_name)
    ON DELETE RESTRICT    -- Prevent deletion of college with active instructors
    ON UPDATE CASCADE,    -- If college name changes, update instructor records
    
    -- When an instructor's department changes, update related records
    CONSTRAINT fk_instructor_department
    FOREIGN KEY (department) 
    REFERENCES Department(department_name)
    ON DELETE RESTRICT    -- Prevent deletion of department with active instructors
    ON UPDATE CASCADE,    -- If department name changes, update instructor records

    CONSTRAINT chk_instructor_college CHECK (
        college IN (
            'St. John''s College of Liberal Arts and Sciences',
            'The School of Education',
            'The Peter J. Tobin College of Business',
            'College of Pharmacy and Health Sciences',
            'The Lesley H. and William L. Collins College of Professional Studies',
            'St. John''s School of Law'
        )
    ),
    CONSTRAINT chk_instructor_email CHECK (
        REGEXP_LIKE(email, '^[a-z]{1,7}[a-z]@stjohns\\.edu$')
    ),
    CONSTRAINT chk_instructor_gender CHECK (
        gender IN ('Male', 'Female')
    ),
    CONSTRAINT chk_instructor_xnumber CHECK (
        REGEXP_LIKE(instructor_xnumber, '^X[0-9]{8}$')
    ),
    CONSTRAINT chk_phone_number CHECK (
        REGEXP_LIKE(phone_number, '^\\+?[0-9]{10,15}$')
    ),
    CONSTRAINT instructor_chk_salary CHECK (
        salary >= 0 AND salary <= 500000
    )
);


DELIMITER $$

CREATE TRIGGER trg_check_instructor_dob_before_insert
BEFORE INSERT ON Instructor
FOR EACH ROW
BEGIN
    IF NEW.date_of_birth > CURDATE() THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Date of birth cannot be in the future.';
    END IF;
END$$

DELIMITER ;

DELIMITER $$

CREATE TRIGGER trg_check_instructor_date_of_hire_before_insert
BEFORE INSERT ON Instructor
FOR EACH ROW
BEGIN
    IF NEW.date_of_hire > CURDATE() THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Date of hire cannot be in the future.';
    END IF;
END$$

DELIMITER ;

DELIMITER $$

CREATE TRIGGER trg_check_instructor_hire_after_birth_before_insert
BEFORE INSERT ON Instructor
FOR EACH ROW
BEGIN
    IF NEW.date_of_hire <= NEW.date_of_birth THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Date of hire must be after the date of birth.';
    END IF;
END$$

DELIMITER ;
