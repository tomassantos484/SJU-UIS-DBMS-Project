from extensions import db
from datetime import datetime

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
    
    enrollments = db.relationship('Enrollment', backref='student', lazy=True)

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
    
    courses = db.relationship('Course', backref='instructor', lazy=True)
    sections = db.relationship('Section', backref='instructor', lazy=True)

class Course(db.Model):
    __tablename__ = 'Course'
    
    crn_number = db.Column(db.Integer, primary_key=True)
    course_title = db.Column(db.String(100), unique=True, nullable=False)
    course_description = db.Column(db.String(255), nullable=False)
    instructor_xnumber = db.Column(db.String(9), db.ForeignKey('Instructor.instructor_xnumber'), nullable=False)
    credits = db.Column(db.Integer, nullable=False)
    department = db.Column(db.String(100), nullable=False)
    course_number = db.Column(db.String(10))
    
    sections = db.relationship('Section', backref='course', lazy=True)

class Section(db.Model):
    __tablename__ = 'Section'
    
    section_id = db.Column(db.Integer, primary_key=True)
    crn_number = db.Column(db.Integer, db.ForeignKey('Course.crn_number'), primary_key=True)
    instructor_xnumber = db.Column(db.String(9), db.ForeignKey('Instructor.instructor_xnumber'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    term = db.Column(db.String(10), nullable=False)
    building_name = db.Column(db.String(50))
    room_number = db.Column(db.String(10))
    max_capacity = db.Column(db.Integer, nullable=False)
    current_enrollment = db.Column(db.Integer, nullable=False, default=0)
    is_online = db.Column(db.Boolean, nullable=False, default=False)
    
    enrollments = db.relationship('Enrollment', backref='section', lazy=True)

class Enrollment(db.Model):
    __tablename__ = 'Enrollment'
    
    student_xnumber = db.Column(db.String(9), db.ForeignKey('Student.student_xnumber'), primary_key=True)
    section_id = db.Column(db.Integer, primary_key=True)
    crn_number = db.Column(db.Integer, primary_key=True)
    grade = db.Column(db.String(2))
    enrollment_date = db.Column(db.Date, nullable=False)
    
    __table_args__ = (
        db.ForeignKeyConstraint(
            ['section_id', 'crn_number'],
            ['Section.section_id', 'Section.crn_number']
        ),
    ) 