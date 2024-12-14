CREATE TABLE Instructor (
    -- Instructor Table
    instructor_xnumber VARCHAR(9) PRIMARY KEY NOT NULL,
    stormcard_id VARCHAR(8) UNIQUE NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    date_of_birth DATE NOT NULL,
    college VARCHAR(100) NOT NULL,
    department VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    gender VARCHAR(6) NOT NULL,
    phone_number VARCHAR(15) UNIQUE NOT NULL,
    date_of_hire DATE NOT NULL,

    -- Constraints

    -- Ensures the X-Number is exactly 9 characters, starting with 'X'
    CONSTRAINT chk_instructor_xnumber CHECK (instructor_xnumber REGEXP '^X[0-9]{8}$'),

    -- Ensures the date of birth is not in the future
    CONSTRAINT chk_instructor_dob CHECK (date_of_birth <= CURDATE()),

    -- Limits valid college names
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

    -- Ensures email matches a basic St. John's University format
    CONSTRAINT chk_instructor_email CHECK (
        email REGEXP '^[a-z]+\\.[a-z]+[0-9]{2}@stjohns\\.edu$'
    ),

    -- Ensures phone numbers follow a standard international format
    CONSTRAINT chk_phone_number CHECK (
        phone_number REGEXP '^\\+?[0-9]{10,15}$'
    ),

    -- Ensures the date of hire is not in the future
    CONSTRAINT chk_date_of_hire CHECK (date_of_hire <= CURDATE()),

    -- Ensures the date of hire is after the date of birth
    CONSTRAINT chk_hire_after_birth CHECK (date_of_hire > date_of_birth),

    -- Ensures gender is either 'Male' or 'Female'
    CONSTRAINT chk_gender CHECK (gender IN ('Male', 'Female'))
);
