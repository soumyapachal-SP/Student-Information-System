from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from models import db, User, Student, Teacher, Grade
from config import Config

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize the db
db.init_app(app)

# Create the tables before the first request
@app.before_first_request
def create_tables():
    with app.app_context():
        db.create_all()

@app.route('/')
def index():
    return render_template('login.html')

# Login route for admin, teacher, and student
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        user = User.query.filter_by(username=username, role=role).first()

        if user:
            return redirect(url_for(f'{role}_dashboard', user_id=user.id))  # Redirect based on role
        else:
            flash('Invalid credentials', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html')

# Admin Dashboard
@app.route('/admin_dashboard/<int:user_id>')
def admin_dashboard(user_id):
    return render_template('admin_dashboard.html', user_id=user_id)

# Teacher Dashboard
@app.route('/teacher_dashboard/<int:user_id>')
def teacher_dashboard(user_id):
    teacher = Teacher.query.get(user_id)
    return render_template('teacher_dashboard.html', teacher=teacher)

# Student Dashboard
@app.route('/student_dashboard/<int:user_id>')
def student_dashboard(user_id):
    student = Student.query.get(user_id)
    grades = Grade.query.filter_by(student_id=user_id).all()
    return render_template('student_dashboard.html', student=student, grades=grades)

# Enroll new student or teacher (Admin only)
@app.route('/enroll', methods=['POST', 'GET'])
def enroll():
    if request.method == 'POST':
        role = request.form['role']
        name = request.form['name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        user = User(username=username, email=email, role=role)
        db.session.add(user)
        db.session.commit()

        if role == 'student':
            student = Student(name=name)
            db.session.add(student)
            db.session.commit()
        elif role == 'teacher':
            teacher = Teacher(name=name)
            db.session.add(teacher)
            db.session.commit()

        flash('New user enrolled!', 'success')
        return redirect(url_for('admin_dashboard', user_id=user.id))
    return render_template('enroll.html')

if __name__ == '__main__':
    app.run(debug=True)
