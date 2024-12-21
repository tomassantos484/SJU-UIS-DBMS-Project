USE `StJohnsUIS`;

DROP TABLE IF EXISTS Section;

CREATE TABLE Section (
    section_id INT NOT NULL,
    crn_number INT NOT NULL,
    instructor_xnumber VARCHAR(9) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    term VARCHAR(10) NOT NULL,
    building_name VARCHAR(50) DEFAULT NULL,
    room_number VARCHAR(10) DEFAULT NULL,
    max_capacity INT NOT NULL,
    current_enrollment INT NOT NULL DEFAULT 0,
    is_online TINYINT(1) NOT NULL DEFAULT 0,

    -- Primary Key
    PRIMARY KEY (section_id, crn_number),

    -- Indexes
    KEY crn_number (crn_number),
    KEY instructor_xnumber (instructor_xnumber),

    -- Foreign Keys
    CONSTRAINT section_ibfk_1 FOREIGN KEY (crn_number) REFERENCES Course (crn_number)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT section_ibfk_2 FOREIGN KEY (instructor_xnumber) REFERENCES Instructor (instructor_xnumber)
        ON DELETE RESTRICT ON UPDATE CASCADE,

    -- Constraints
    CONSTRAINT chk_building_name CHECK (
        (building_name IN (
            'D''Angelo Center', 'Hollis Hall', 'Marillac Hall', 'Bent Hall',
            'St. Albert''s Hall', 'St. Augustine Hall', 'St. John''s Hall', 'Sullivan Hall'
        ) OR (is_online = TRUE))
    ),
    CONSTRAINT chk_dates CHECK (start_date <= end_date),
    CONSTRAINT chk_room_number CHECK (
        (REGEXP_LIKE(room_number, '^[A-Z0-9]{1,10}$') OR (is_online = TRUE))
    ),
    CONSTRAINT section_chk_1 CHECK (max_capacity > 0)
);

DELIMITER $$

CREATE TRIGGER validate_crn_term
BEFORE INSERT ON Section
FOR EACH ROW
BEGIN
    IF (NEW.term = 'Fall' AND NEW.crn_number NOT LIKE '7%') OR 
       (NEW.term = 'Spring' AND NEW.crn_number NOT LIKE '1%') THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'CRN number does not match the term pattern.';
    END IF;
END$$

DELIMITER ;

-- Add cascade rules for Section deletion/updates
ALTER TABLE Enrollment
    ADD CONSTRAINT fk_enrollment_section
    FOREIGN KEY (section_id, crn_number) 
    REFERENCES Section(section_id, crn_number)
    ON DELETE CASCADE
    ON UPDATE CASCADE;
