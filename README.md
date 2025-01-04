# **SJU-UIS-DBMS-Project**

## **Introduction**
The **SJU-UIS-DBMS Project** is a graduate-level initiative designed to create a robust and well-structured database schema that mimics the real-world **St. John's University Information System (UIS)**. This mini-world experiment applies foundational database management principles such as normalization, constraints, and relational design to manage student, faculty, and academic records effectively.

The project implements a clean, scalable system that reduces redundancy and improves data integrity, offering a practical application of database concepts. The database is built to streamline academic data management, ensuring accuracy, consistency, and scalability while reinforcing the core principles taught in the **Database Management Systems (DBMS)** course.

<img width="1052" alt="image" src="https://github.com/user-attachments/assets/8f7c3f5a-c45e-44dc-9db7-adbdcecceb32" />

---

## **Technology Stack**
The system is built with the following technologies, selected for their reliability, scalability, and suitability for a university database system:

### **Database Management System**: **MySQL**
- Robust support for relational databases, constraints, and normalization.
- Handles complex relationships and ensures data integrity.

### **Backend**: **Python Flask & SQLAlchemy**
- Flask provides a lightweight and flexible web framework.
- SQLAlchemy allows efficient database interactions with an Object-Relational Mapping (ORM) approach.

### **Frontend**: **HTML/CSS**
- Clean and responsive design prioritizing accessibility and usability.
- Consistent styling reflects St. John’s brand identity.

### **Web Deployment**: **Railway**
- Simplifies deployment with environment variable management and seamless database integration.
- Enhances scalability and reliability.

---

## **Database Schema Design**
The schema features five interconnected tables designed to handle critical academic operations:

1. **Student**: Manages student records, including personal information, college, major, and academic details.
2. **Instructor**: Manages faculty records, including personal information, college, department, and salary.
3. **Course**: Stores academic offerings, linking to instructors and departments.
4. **Section**: Represents specific instances of courses offered each term, including location and enrollment limits.
5. **Enrollment**: Tracks student enrollments in course sections, including grades.

### **Key Features**:
- **Normalization**: Achieves 1NF, 2NF, and 3NF to reduce redundancy and ensure efficient storage.
- **Constraints**: Implements primary and foreign keys, unique constraints, and validation checks to maintain data integrity.
- **Indexes**: Optimizes query performance with indexes on frequently accessed fields.
- **Relationships**: Supports many-to-many connections between students and courses through the `Enrollment` table.
- **Student Search**: Look up students by X-number and view their personal and academic details.
- **Faculty Management**: Explore faculty records, including salary and department.
- **Dynamic Enrollment**: Manage student enrollments and track course participation.
- **Section Management**: Handle course offerings with capacity and scheduling constraints.

---

## **Future Improvements**
This project lays a strong foundation but also leaves room for enhancements, including:
- **Role-Based Access Control**: Implement a user management system with distinct views for students, faculty, and administrators.
- **Prerequisite System**: Add course prerequisites for more realistic academic operations.
- **Cloud Migration**: Upgrade to a more robust cloud platform like AWS or Google Cloud SQL.
- **Modern Frontend Frameworks**: Enhance the user interface with React.js, Next.js, or Tailwind CSS.
- **Waitlist Management**: Add support for section waitlists and cross-listed courses.

---

## **Getting Started**

### **Clone the Repository**:
```bash
git clone https://github.com/yourusername/SJU-UIS-DBMS-Project.git
cd SJU-UIS-DBMS-Project
```

### **Set Up the Environment**:
Install Python dependencies:

```
pip install -r requirements.txt
```
### **Set up the database connection in .env**:
```
env
DB_URI=mysql+pymysql://username:password@hostname/dbname
```
### **Run the Application**:
```
flask run
```
### **Access the Application**:

Open ```http://127.0.0.1:5000``` in your browser.

### **License**
This project is licensed under the MIT License. See the MITLicense file for details.
