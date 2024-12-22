from extensions import db
from datetime import datetime, date
from sqlalchemy import event

class Student(db.Model):
    __tablename__ = 'Student'
    
    student_xnumber = db.Column(db.String(9), primary_key=True)
    stormcard_id = db.Column(db.String(8), unique=True, nullable=False)
    library_id = db.Column(db.String(14), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    college = db.Column(db.String(100), nullable=False)
    major = db.Column(db.String(50), nullable=False)
    gpa = db.Column(db.Numeric(3,2), nullable=False)
    gender = db.Column(db.String(6), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    date_of_admission = db.Column(db.Date, nullable=False)
    year_of_graduation = db.Column(db.Date, nullable=False)
    
    enrollments = db.relationship('Enrollment', 
                                backref='student', 
                                lazy=True, 
                                cascade='all, delete-orphan',
                                passive_deletes=True)

    __table_args__ = (
        db.CheckConstraint(
            "college IN ('St. John''s College of Liberal Arts and Sciences', 'The School of Education', "
            "'The Peter J. Tobin College of Business', 'College of Pharmacy and Health Sciences', "
            "'The Lesley H. and William L. Collins College of Professional Studies', 'St. John''s School of Law')",
            name='chk_college'
        ),
        db.CheckConstraint(
            "REGEXP_LIKE(email, '^[a-z]+\\.[a-z]+[0-9]{2}@my\\.stjohns\\.edu$')",
            name='chk_email_format'
        ),
        db.CheckConstraint(
            "gender IN ('Male', 'Female')",
            name='chk_gender'
        ),
        db.CheckConstraint(
            "gpa >= 0.00 AND gpa <= 4.00",
            name='chk_gpa'
        ),
        db.CheckConstraint(
            "REGEXP_LIKE(phone_number, '^\\+?[0-9]{10,14}$')",
            name='chk_phone_format'
        ),
        db.CheckConstraint(
            "REGEXP_LIKE(stormcard_id, '^[0-9]{8}$')",
            name='chk_stormcard_id'
        ),
        db.CheckConstraint(
            "REGEXP_LIKE(student_xnumber, '^X[0-9]{8}$')",
            name='chk_student_xnumber'
        ),
        db.CheckConstraint(
            "year_of_graduation > date_of_admission "
            "AND year_of_graduation <= DATE_ADD(date_of_admission, INTERVAL 8 YEAR)",
            name='chk_year_graduation'
        )
    )

@event.listens_for(Student, 'before_insert')
def check_student_dates(mapper, connection, target):
    if target.date_of_birth > date.today():
        raise ValueError('Date of birth cannot be in the future.')
    if target.date_of_admission > date.today():
        raise ValueError('Date of admission cannot be in the future.')

class Instructor(db.Model):
    __tablename__ = 'Instructor'
    
    instructor_xnumber = db.Column(db.String(9), primary_key=True)
    stormcard_id = db.Column(db.String(8), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    college = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    gender = db.Column(db.String(6), nullable=False)
    phone_number = db.Column(db.String(15), unique=True, nullable=False)
    date_of_hire = db.Column(db.Date, nullable=False)
    salary = db.Column(db.Numeric(10,2), nullable=False, default=50000.00)
    
    courses = db.relationship('Course', 
                            backref='instructor', 
                            lazy=True,
                            cascade='save-update')
    
    sections = db.relationship('Section', 
                             backref='instructor', 
                             lazy=True,
                             cascade='save-update')

@event.listens_for(Instructor, 'before_insert')
def check_instructor_dates(mapper, connection, target):
    if target.date_of_birth > date.today():
        raise ValueError('Date of birth cannot be in the future.')
    if target.date_of_hire > date.today():
        raise ValueError('Date of hire cannot be in the future.')
    if target.date_of_hire <= target.date_of_birth:
        raise ValueError('Date of hire must be after the date of birth.')

class Course(db.Model):
    __tablename__ = 'Course'
    
    crn_number = db.Column(db.Integer, primary_key=True)
    course_title = db.Column(db.String(100), unique=True, nullable=False)
    course_description = db.Column(db.String(255), nullable=False)
    instructor_xnumber = db.Column(db.String(9), 
                                 db.ForeignKey('Instructor.instructor_xnumber', 
                                             ondelete='RESTRICT',
                                             onupdate='CASCADE'), 
                                 nullable=False)
    credits = db.Column(db.Integer, nullable=False)
    department = db.Column(db.String(100), nullable=False)
    course_number = db.Column(db.String(10))
    
    sections = db.relationship('Section', 
                             backref='course', 
                             lazy=True, 
                             cascade='all, delete-orphan',
                             passive_deletes=True)

    __table_args__ = (
        db.CheckConstraint(
            "(crn_number BETWEEN 70000 AND 79999) OR "  # Fall courses
            "(crn_number BETWEEN 10000 AND 19999)",     # Spring courses
            name='chk_crn_term'
        ),
        db.CheckConstraint(
            "credits BETWEEN 1 AND 4",
            name='chk_credits'
        )
    )

class Section(db.Model):
    __tablename__ = 'Section'
    
    section_id = db.Column(db.Integer, primary_key=True)
    crn_number = db.Column(db.Integer, 
                          db.ForeignKey('Course.crn_number',
                                      ondelete='CASCADE',
                                      onupdate='CASCADE'), 
                          primary_key=True)
    instructor_xnumber = db.Column(db.String(9), 
                                 db.ForeignKey('Instructor.instructor_xnumber',
                                             ondelete='RESTRICT',
                                             onupdate='CASCADE'), 
                                 nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    term = db.Column(db.String(10), nullable=False)
    building_name = db.Column(db.String(50))
    room_number = db.Column(db.String(10))
    max_capacity = db.Column(db.Integer, nullable=False)
    current_enrollment = db.Column(db.Integer, nullable=False, default=0)
    is_online = db.Column(db.Boolean, nullable=False, default=False)
    
    enrollments = db.relationship('Enrollment', 
                                backref='section', 
                                lazy=True, 
                                cascade='all, delete-orphan',
                                passive_deletes=True)

    __table_args__ = (
        db.CheckConstraint(
            "(building_name IN ('D''Angelo Center', 'Hollis Hall', 'Marillac Hall', 'Bent Hall', "
            "'St. Albert''s Hall', 'St. Augustine Hall', 'St. John''s Hall', 'Sullivan Hall') "
            "OR (is_online = TRUE))",
            name='chk_building_name'
        ),
        db.CheckConstraint(
            "start_date <= end_date",
            name='chk_dates'
        ),
        db.CheckConstraint(
            "(REGEXP_LIKE(room_number, '^[A-Z0-9]{1,10}$') OR (is_online = TRUE))",
            name='chk_room_number'
        ),
        db.CheckConstraint(
            "max_capacity > 0",
            name='section_chk_1'
        )
    )

@event.listens_for(Section, 'before_insert')
@event.listens_for(Section, 'before_update')
def validate_section_crn(mapper, connection, target):
    if target.term == 'Fall' and not (70000 <= target.crn_number <= 79999):
        raise ValueError("Fall courses must have CRN numbers between 70000-79999")
    elif target.term == 'Spring' and not (10000 <= target.crn_number <= 19999):
        raise ValueError("Spring courses must have CRN numbers between 10000-19999")

class Enrollment(db.Model):
    __tablename__ = 'Enrollment'
    
    student_xnumber = db.Column(db.String(9), 
                               db.ForeignKey('Student.student_xnumber',
                                           ondelete='CASCADE',
                                           onupdate='CASCADE'), 
                               primary_key=True)
    section_id = db.Column(db.Integer, primary_key=True)
    crn_number = db.Column(db.Integer, primary_key=True)
    grade = db.Column(db.String(2))
    enrollment_date = db.Column(db.Date, nullable=False)
    
    __table_args__ = (
        db.ForeignKeyConstraint(
            ['section_id', 'crn_number'],
            ['Section.section_id', 'Section.crn_number'],
            ondelete='CASCADE',
            onupdate='CASCADE'
        ),
    ) 