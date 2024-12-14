USE `StJohnsUIS`;
DROP TABLE IF EXISTS Section;

CREATE TABLE Section (
    -- Section Table
    section_id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    crn_number INT NOT NULL, -- Match INT type
    instructor_xnumber VARCHAR(9) NOT NULL,
    student_xnumber VARCHAR(9) NOT NULL,
    section_name VARCHAR(50) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    term VARCHAR(10) NOT NULL,
    building_name VARCHAR(50) NOT NULL,
    room_number VARCHAR(10) NOT NULL,
    max_capacity INT NOT NULL CHECK (max_capacity > 0),
    current_enrollment INT NOT NULL DEFAULT 0,

    -- Constraints
    CONSTRAINT chk_section_name CHECK (LENGTH(TRIM(section_name)) > 0),
    CONSTRAINT chk_dates CHECK (start_date <= end_date),
    CONSTRAINT chk_building_name CHECK (
        building_name IN (
            'D''Angelo Center',
            'Hollis Hall',
            'Marillac Hall',
            'Bent Hall',
            'St. Albert''s Hall',
            'St. Augustine Hall',
            'St. John''s Hall',
            'Sullivan Hall'
        )
    ),
    CONSTRAINT chk_room_number CHECK (room_number REGEXP '^[A-Z0-9]{1,10}$'),

    -- Foreign Keys
    FOREIGN KEY (crn_number) REFERENCES Course(crn_number),
    FOREIGN KEY (instructor_xnumber) REFERENCES Instructor(instructor_xnumber),
    FOREIGN KEY (student_xnumber) REFERENCES Student(student_xnumber)
);