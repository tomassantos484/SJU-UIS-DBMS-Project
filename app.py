from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from extensions import db
from models import Student, Instructor, Course, Section, Enrollment
import secrets

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Database configuration
database_url = os.getenv('DATABASE_URL')

if database_url and database_url.startswith("mysql://"):
    database_url = database_url.replace("mysql://", "mysql+mysqlconnector://", 1)
else:
    # Fallback to local database
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_host = os.getenv('DB_HOST')
    db_name = os.getenv('DB_NAME')
    database_url = f"mysql+mysqlconnector://{db_user}:{db_password}@{db_host}/{db_name}"

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-default-secret-key-here')

db.init_app(app)  # Initialize db with app

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/students')
def students():
    students = Student.query.all()
    return render_template('students.html', students=students)

@app.route('/courses')
def courses():
    courses = Course.query.all()
    return render_template('courses.html', courses=courses)

@app.route('/instructors')
def instructors():
    instructors = Instructor.query.all()
    return render_template('instructors.html', instructors=instructors)

@app.route('/enrollments')
def enrollments():
    enrollments = Enrollment.query.all()
    return render_template('enrollments.html', enrollments=enrollments)

@app.route('/students/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        try:
            # Print form data for debugging
            print("Form data:", request.form)
            
            new_student = Student(
                student_xnumber=request.form['student_xnumber'],
                stormcard_id=request.form['stormcard_id'],
                library_id=request.form['library_id'],
                first_name=request.form['first_name'],
                last_name=request.form['last_name'],
                date_of_birth=request.form['date_of_birth'],
                college=request.form['college'],
                major=request.form['major'],
                gpa=float(request.form['gpa']),
                gender=request.form['gender'],
                email=request.form['email'],
                phone_number=request.form['phone_number'],
                date_of_admission=request.form['date_of_admission'],
                year_of_graduation=request.form['year_of_graduation']
            )
            db.session.add(new_student)
            db.session.commit()
            flash('Student added successfully!', 'success')
            return redirect(url_for('students'))
        except Exception as e:
            db.session.rollback()
            print("Error:", str(e))  # Print error for debugging
            flash(f'Error adding student: {str(e)}', 'error')
            return render_template('add_student.html')  # Return to form with error
    
    return render_template('add_student.html')

@app.route('/students/<student_xnumber>')
def view_student(student_xnumber):
    student = Student.query.get_or_404(student_xnumber)
    return render_template('view_student.html', student=student)

@app.route('/students/<student_xnumber>/edit', methods=['GET', 'POST'])
def edit_student(student_xnumber):
    student = Student.query.get_or_404(student_xnumber)
    
    if request.method == 'POST':
        try:
            student.stormcard_id = request.form['stormcard_id']
            student.library_id = request.form['library_id']
            student.first_name = request.form['first_name']
            student.last_name = request.form['last_name']
            student.date_of_birth = request.form['date_of_birth']
            student.college = request.form['college']
            student.major = request.form['major']
            student.gpa = float(request.form['gpa'])
            student.gender = request.form['gender']
            student.email = request.form['email']
            student.phone_number = request.form['phone_number']
            student.date_of_admission = request.form['date_of_admission']
            student.year_of_graduation = request.form['year_of_graduation']
            
            db.session.commit()
            flash('Student updated successfully!', 'success')
            return redirect(url_for('view_student', student_xnumber=student.student_xnumber))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating student: {str(e)}', 'error')
            return redirect(url_for('edit_student', student_xnumber=student_xnumber))
    
    return render_template('edit_student.html', student=student)

@app.route('/students/<student_xnumber>/delete', methods=['POST'])
def delete_student(student_xnumber):
    student = Student.query.get_or_404(student_xnumber)
    try:
        db.session.delete(student)
        db.session.commit()
        flash('Student deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting student: {str(e)}', 'error')
    
    return redirect(url_for('students'))

@app.route('/instructors/add', methods=['GET', 'POST'])
def add_instructor():
    if request.method == 'POST':
        try:
            new_instructor = Instructor(
                instructor_xnumber=request.form['instructor_xnumber'],
                stormcard_id=request.form['stormcard_id'],
                first_name=request.form['first_name'],
                last_name=request.form['last_name'],
                date_of_birth=request.form['date_of_birth'],
                college=request.form['college'],
                department=request.form['department'],
                email=request.form['email'],
                gender=request.form['gender'],
                phone_number=request.form['phone_number'],
                date_of_hire=request.form['date_of_hire'],
                salary=float(request.form['salary'])
            )
            db.session.add(new_instructor)
            db.session.commit()
            flash('Instructor added successfully!', 'success')
            return redirect(url_for('instructors'))
        except Exception as e:
            db.session.rollback()
            print("Error:", str(e))
            flash(f'Error adding instructor: {str(e)}', 'error')
            return render_template('add_instructor.html')
    
    return render_template('add_instructor.html')

@app.route('/instructors/<instructor_xnumber>')
def view_instructor(instructor_xnumber):
    instructor = Instructor.query.get_or_404(instructor_xnumber)
    return render_template('view_instructor.html', instructor=instructor)

@app.route('/instructors/<instructor_xnumber>/edit', methods=['GET', 'POST'])
def edit_instructor(instructor_xnumber):
    instructor = Instructor.query.get_or_404(instructor_xnumber)
    
    if request.method == 'POST':
        try:
            instructor.stormcard_id = request.form['stormcard_id']
            instructor.first_name = request.form['first_name']
            instructor.last_name = request.form['last_name']
            instructor.date_of_birth = request.form['date_of_birth']
            instructor.college = request.form['college']
            instructor.department = request.form['department']
            instructor.email = request.form['email']
            instructor.gender = request.form['gender']
            instructor.phone_number = request.form['phone_number']
            instructor.date_of_hire = request.form['date_of_hire']
            instructor.salary = float(request.form['salary'])
            
            db.session.commit()
            flash('Instructor updated successfully!', 'success')
            return redirect(url_for('view_instructor', instructor_xnumber=instructor.instructor_xnumber))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating instructor: {str(e)}', 'error')
            return redirect(url_for('edit_instructor', instructor_xnumber=instructor_xnumber))
    
    return render_template('edit_instructor.html', instructor=instructor)

@app.route('/instructors/<instructor_xnumber>/delete', methods=['POST'])
def delete_instructor(instructor_xnumber):
    instructor = Instructor.query.get_or_404(instructor_xnumber)
    try:
        db.session.delete(instructor)
        db.session.commit()
        flash('Instructor deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting instructor: {str(e)}', 'error')
    
    return redirect(url_for('instructors'))

@app.route('/courses/add', methods=['GET', 'POST'])
def add_course():
    if request.method == 'POST':
        try:
            new_course = Course(
                crn_number=request.form['crn_number'],
                course_title=request.form['course_title'],
                course_description=request.form['course_description'],
                instructor_xnumber=request.form['instructor_xnumber'],
                credits=int(request.form['credits']),
                department=request.form['department'],
                course_number=request.form['course_number']
            )
            db.session.add(new_course)
            db.session.commit()
            flash('Course added successfully!', 'success')
            return redirect(url_for('courses'))
        except Exception as e:
            db.session.rollback()
            print("Error:", str(e))
            flash(f'Error adding course: {str(e)}', 'error')
            return render_template('add_course.html', instructors=Instructor.query.all())
    
    return render_template('add_course.html', instructors=Instructor.query.all())

@app.route('/courses/<int:crn_number>')
def view_course(crn_number):
    course = Course.query.get_or_404(crn_number)
    return render_template('view_course.html', course=course)

@app.route('/courses/<int:crn_number>/edit', methods=['GET', 'POST'])
def edit_course(crn_number):
    course = Course.query.get_or_404(crn_number)
    
    if request.method == 'POST':
        try:
            course.course_title = request.form['course_title']
            course.course_description = request.form['course_description']
            course.instructor_xnumber = request.form['instructor_xnumber']
            course.credits = int(request.form['credits'])
            course.department = request.form['department']
            course.course_number = request.form['course_number']
            
            db.session.commit()
            flash('Course updated successfully!', 'success')
            return redirect(url_for('view_course', crn_number=course.crn_number))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating course: {str(e)}', 'error')
            return redirect(url_for('edit_course', crn_number=crn_number))
    
    return render_template('edit_course.html', course=course, instructors=Instructor.query.all())

@app.route('/courses/<int:crn_number>/delete', methods=['POST'])
def delete_course(crn_number):
    course = Course.query.get_or_404(crn_number)
    try:
        db.session.delete(course)
        db.session.commit()
        flash('Course deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting course: {str(e)}', 'error')
    
    return redirect(url_for('courses'))

@app.route('/enrollments/add', methods=['GET', 'POST'])
def add_enrollment():
    if request.method == 'POST':
        try:
            new_enrollment = Enrollment(
                student_xnumber=request.form['student_xnumber'],
                section_id=request.form['section_id'],
                crn_number=request.form['crn_number'],
                grade=request.form['grade'] if request.form['grade'] else None,
                enrollment_date=request.form['enrollment_date']
            )
            db.session.add(new_enrollment)
            db.session.commit()
            flash('Enrollment added successfully!', 'success')
            return redirect(url_for('enrollments'))
        except Exception as e:
            db.session.rollback()
            print("Error:", str(e))
            flash(f'Error adding enrollment: {str(e)}', 'error')
            return render_template('add_enrollment.html', 
                                students=Student.query.all(),
                                sections=Section.query.all())
    
    return render_template('add_enrollment.html', 
                         students=Student.query.all(),
                         sections=Section.query.all())

@app.route('/enrollments/<student_xnumber>/<int:section_id>/<int:crn_number>')
def view_enrollment(student_xnumber, section_id, crn_number):
    enrollment = Enrollment.query.get_or_404((student_xnumber, section_id, crn_number))
    return render_template('view_enrollment.html', enrollment=enrollment)

@app.route('/enrollments/<student_xnumber>/<int:section_id>/<int:crn_number>/edit', methods=['GET', 'POST'])
def edit_enrollment(student_xnumber, section_id, crn_number):
    enrollment = Enrollment.query.get_or_404((student_xnumber, section_id, crn_number))
    
    if request.method == 'POST':
        try:
            enrollment.grade = request.form['grade'] if request.form['grade'] else None
            enrollment.enrollment_date = request.form['enrollment_date']
            
            db.session.commit()
            flash('Enrollment updated successfully!', 'success')
            return redirect(url_for('view_enrollment', 
                                  student_xnumber=enrollment.student_xnumber,
                                  section_id=enrollment.section_id,
                                  crn_number=enrollment.crn_number))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating enrollment: {str(e)}', 'error')
            return redirect(url_for('edit_enrollment',
                                  student_xnumber=student_xnumber,
                                  section_id=section_id,
                                  crn_number=crn_number))
    
    return render_template('edit_enrollment.html', 
                         enrollment=enrollment,
                         students=Student.query.all(),
                         sections=Section.query.all())

@app.route('/enrollments/<student_xnumber>/<int:section_id>/<int:crn_number>/delete', methods=['POST'])
def delete_enrollment(student_xnumber, section_id, crn_number):
    enrollment = Enrollment.query.get_or_404((student_xnumber, section_id, crn_number))
    try:
        db.session.delete(enrollment)
        db.session.commit()
        flash('Enrollment deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting enrollment: {str(e)}', 'error')
    
    return redirect(url_for('enrollments'))

@app.cli.command("init-db")
def init_db():
    """Initialize the database."""
    with app.app_context():
        db.create_all()
        print("Database initialized!")

if __name__ == '__main__':
    app.run(debug=True)