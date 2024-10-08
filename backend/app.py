from flask import Flask, request, jsonify, render_template
import mysql.connector
import bcrypt
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Connect to the MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Sushant@123",  # Replace with your actual password
    database="online_exam"
)
cursor = db.cursor()

# Home route for landing page
@app.route('/')
def home():
    return render_template('index.html')

# Route to render registration page
@app.route('/register')
def render_register():
    return render_template('register.html')

# Route to render login page
@app.route('/login')
def render_login():
    return render_template('login.html')

# Route to render create exam page
@app.route('/create_exam')
def render_create_exam():
    return render_template('create_exam.html')

# Route to render add question page
@app.route('/add_question')
def render_add_question():
    return render_template('add_question.html')

# Route to render exam submission page
@app.route('/submit_exam')
def render_submit_exam():
    return render_template('submit_exam.html')

# Route to render view results page
@app.route('/view_results')
def render_view_results():
    return render_template('view_results.html')

# API route to register a student
@app.route('/api/register', methods=['POST'])
def register_student():
    data = request.json
    hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
    
    # Insert the new student into the Students table
    sql = "INSERT INTO Students (name, email, password) VALUES (%s, %s, %s)"
    cursor.execute(sql, (data['name'], data['email'], hashed_password))
    db.commit()
    
    return jsonify({"message": "Student registered successfully"}), 201

# API route to login a student
@app.route('/api/login', methods=['POST'])
def login_student():
    data = request.json
    sql = "SELECT * FROM Students WHERE email = %s"
    cursor.execute(sql, (data['email'],))
    user = cursor.fetchone()

    if not user:
        return jsonify({"message": "User not found"}), 404

    if bcrypt.checkpw(data['password'].encode('utf-8'), user[3].encode('utf-8')):
        return jsonify({"message": "Login successful"})
    else:
        return jsonify({"message": "Invalid password"}), 401

# API route to create a new exam (admin functionality)
@app.route('/api/create_exam', methods=['POST'])
def create_exam():
    data = request.json
    
    # Insert the new exam into the Exams table
    sql = "INSERT INTO Exams (exam_name, total_marks, duration) VALUES (%s, %s, %s)"
    cursor.execute(sql, (data['exam_name'], data['total_marks'], data['duration']))
    db.commit()
    
    return jsonify({"message": "Exam created successfully"}), 201

# API route to add questions to an exam (admin functionality)
@app.route('/api/add_question', methods=['POST'])
def add_question():
    data = request.json
    
    # Insert the new question into the Questions table
    sql = '''INSERT INTO Questions (exam_id, question_text, option_a, option_b, option_c, option_d, correct_option) 
             VALUES (%s, %s, %s, %s, %s, %s, %s)'''
    cursor.execute(sql, (
        data['exam_id'], data['question_text'], data['option_a'], data['option_b'], 
        data['option_c'], data['option_d'], data['correct_option']
    ))
    db.commit()
    
    return jsonify({"message": "Question added successfully"}), 201

# API route for students to take the exam (submit answers)
@app.route('/api/submit_exam', methods=['POST'])
def submit_exam():
    data = request.json
    student_id = data['student_id']
    exam_id = data['exam_id']
    student_answers = data['answers']  # This is expected to be a dictionary {question_id: answer}

    # Fetch the correct answers from the Questions table
    sql = "SELECT question_id, correct_option FROM Questions WHERE exam_id = %s"
    cursor.execute(sql, (exam_id,))
    correct_answers = cursor.fetchall()

    # Calculate the score
    total_marks = 0
    marks_obtained = 0

    for question in correct_answers:
        question_id = question[0]
        correct_option = question[1]

        total_marks += 1  # Assuming each question carries 1 mark
        if student_answers.get(str(question_id)) == correct_option:
            marks_obtained += 1

    # Store the result in the Results table
    sql = '''INSERT INTO Results (student_id, exam_id, marks_obtained, total_marks) 
             VALUES (%s, %s, %s, %s)'''
    cursor.execute(sql, (student_id, exam_id, marks_obtained, total_marks))
    db.commit()

    return jsonify({
        "message": "Exam submitted successfully",
        "marks_obtained": marks_obtained,
        "total_marks": total_marks
    }), 201

# API route to view results for a student
@app.route('/api/view_results/<int:student_id>', methods=['GET'])
def view_results(student_id):
    sql = "SELECT * FROM Results WHERE student_id = %s"
    cursor.execute(sql, (student_id,))
    results = cursor.fetchall()

    results_list = []
    for result in results:
        result_data = {
            'exam_id': result[2],
            'marks_obtained': result[3],
            'total_marks': result[4],
            'exam_date': result[5]
        }
        results_list.append(result_data)

    return jsonify({"results": results_list}), 200

if __name__ == "__main__":
    app.run(debug=True, port=5002)