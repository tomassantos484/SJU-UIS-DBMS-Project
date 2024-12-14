USE `StJohnsUIS`;
DROP TABLE IF EXISTS Student;

CREATE TABLE Student (
    student_xnumber VARCHAR(9) PRIMARY KEY NOT NULL,
    stormcard_id VARCHAR(8) UNIQUE NOT NULL,
    library_id VARCHAR(14) UNIQUE NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    date_of_birth DATE NOT NULL,
    college VARCHAR(100) NOT NULL,
    major VARCHAR(50) NOT NULL,
    gpa DECIMAL(3,2) NOT NULL,
    gender VARCHAR(6) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone_number VARCHAR(15) NOT NULL,
    date_of_admission DATE NOT NULL,
    year_of_graduation DATE NOT NULL,

    -- Constraints

    -- Ensures the X-Number is exactly 9 digits
    CONSTRAINT chk_student_xnumber CHECK (student_xnumber REGEXP '^X[0-9]{8}$'),

    -- Ensures the Stormcard ID is exactly 8 digits
    CONSTRAINT chk_stormcard_id CHECK (stormcard_id REGEXP '^[0-9]{8}$'),

    -- Ensures the GPA is between 0.0 and 4.0 (inclusive)
    CONSTRAINT chk_gpa CHECK (gpa >= 0.00 AND gpa <= 4.00),

    -- Ensures the date of birth is not in the future
    CONSTRAINT chk_dob CHECK (date_of_birth <= CURDATE()),

    -- Ensures gender is either 'Male' or 'Female'
    CONSTRAINT chk_gender CHECK (gender IN ('Male', 'Female')),

    -- Ensures email addresses are unique and follow the St. John's format
    CONSTRAINT chk_email_format CHECK (
        email REGEXP '^[a-z]+\\.[a-z]+[0-9]{2}@my\\.stjohns\\.edu$'
    ),

    -- Ensures phone numbers are unique and follow the correct format
    CONSTRAINT chk_phone_format CHECK (phone_number REGEXP '^\\+?[0-9]{10,14}$'),

    -- Ensures the admission date is not in the future
    CONSTRAINT chk_date_of_admission CHECK (date_of_admission <= CURDATE()),

    -- Ensures graduation year is after admission year and within 8 years
    CONSTRAINT chk_year_graduation CHECK (
        year_of_graduation > date_of_admission AND 
        year_of_graduation <= DATE_ADD(date_of_admission, INTERVAL 8 YEAR)
    ),

    -- Limits college choices to the specified list of schools
    CONSTRAINT chk_college CHECK (
        college IN (
            'St. John''s College of Liberal Arts and Sciences', 
            'The School of Education', 
            'The Peter J. Tobin College of Business', 
            'College of Pharmacy and Health Sciences', 
            'The Lesley H. and William L. Collins College of Professional Studies', 
            'St. John''s School of Law'
        )
    )
);