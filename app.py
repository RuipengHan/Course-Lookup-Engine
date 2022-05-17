# from nis import cat
from re import L
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import create_engine
# import pandas as pd
import string
import random
import datetime
user = 'root'
password = 'kimura'
host = '104.154.75.238'
port = 3306
database = 'production'
  
engine = create_engine("mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(user, password, host, port, database))
# engine = create_engine(url="mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(user, password, host, port, database))
engine.connect()

app = Flask(__name__)
# For generating random user names;
letters = string.ascii_lowercase
password = "abc123"
email = "example@email.com"
first_name = "Lucky"
last_name = "User"

# Insert
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        course_number = request.form['number']
        subject = request.form['subject']
        title = request.form['title']
        description = request.form['description']
        query = "INSERT INTO Courses (course_number, subject, title, description) VALUES ({0}, '{1}', '{2}', '{3}');".format(course_number, subject, title, description)
        engine.execute(query)
        return redirect('/')
    else:
        return render_template('index.html')

# Search
@app.route('/search',methods=["POST","GET"])
def search():
    if request.method == "POST":
        number = request.form["search number"]
        subject = request.form["search name"].upper()
        try:
            query = f"SELECT * FROM Courses where course_number = {number} and subject = '{subject}'"
            courses = engine.execute(query)
            return render_template("index.html", courses=courses)
        except:
            return "invalid search"
    else:
        return render_template("index.html")

# Delete
@app.route('/delete/<int:id>')
def delete(id):
    query = "DELETE FROM Courses WHERE id = {0};".format(id)
    engine.execute(query)
    return redirect('/')

# Update
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    query = f"SELECT * FROM Courses where id = {id};"
    courses = engine.execute(query)
    if request.method == 'POST':
        number = request.form["number"]
        subject = request.form["subject"]
        title = request.form["title"]
        description = request.form["description"]

        query = f"UPDATE Courses SET course_number = {number}, subject = '{subject}', title = '{title}', description = '{description}' WHERE id = {id};"
        courses = engine.execute(query)
        return redirect('/')
    else:
        return render_template('update.html', courses = courses, id = id)

# Advanced SQL -1
@app.route('/query1', methods=['GET', 'POST'])
def query1():
    query = "(select c.subject, course_number, com.comment \
            from Courses c join Comments com on com.id = c.id \
            where course_number=241 and subject = 'CS') \
            union(select c.subject, course_number, com.comment \
            from Courses c join Comments com on com.id = c.id \
            where course_number=233 and subject = 'CS');"
    comments = engine.execute(query)
    return render_template("result.html",comments = comments)

# Advanced SQL -2
@app.route('/query2',methods=["POST","GET"])
def query2():
    description = engine.execute("select c.subject,avg(r.overall_quality) as average_quality \
        from Courses c natural join Ratings r \
        group by c.subject \
        having avg(r.overall_quality) >= (select avg(r1.overall_quality) \
        from Courses c1 natural join Ratings r1 \
        group by c1.subject \
        having subject = 'CS') \
        order by avg(r.overall_quality) desc")
    return render_template("result2.html",comments = description)

# Generate a user id for a new user
def insert_user(user_name):
    new_user_query = f"INSERT INTO Users(user_name, password, email, first_name, last_name, college, department, major, graduation_class, sex) VALUES ('{user_name}', '{password}', '{email}', '{first_name}', '{last_name}', '', '', '', 2023, '');"
    engine.execute(new_user_query)
    new_user_record = engine.execute('SELECT COUNT(*) AS count FROM Users;')
    new_user_id = 1
    for i in new_user_record:
        new_user_id = i['count']
    print(f'The newly created user as the rater/commenter is {new_user_id}!')
    return new_user_id

# Rate a course
@app.route('/rate_course/<int:id>', methods=['GET', 'POST'])
def rate(id):
    query = f"SELECT * FROM Courses where id = {id};"
    courses = engine.execute(query)
    if request.method == 'POST':
        # Randomly generating a 10-character rater user name.
        user_name = ''.join(random.choice(letters) for i in range(10))
        # Insert a new user as the rater.
        rater_id = insert_user(user_name)

        # Get rating form's data:
        overall_quality = request.form['overall_quality']
        professor = request.form['professor']
        workload = request.form['workload']
        rubric = request.form['rubric']
        difficulty = request.form['difficulty']
        grade_Rceived = request.form['grade_Rceived']
        # Insert a new Ratings record
        query = f"INSERT INTO Ratings(course, rater, overall_quality, professor, workload, rubric, difficulty, grade_Rceived) VALUES({id}, {rater_id}, {overall_quality}, {professor}, {workload}, {rubric}, {difficulty}, '{grade_Rceived}');"
        print("INSERT NEW RATING SUCCESSFULLY!")
        courses = engine.execute(query)
        return redirect('/')
    else:
        return render_template('rate_course.html', courses = courses, id = id)

# View ratings of a course
@app.route('/view_rate/<int:id>', methods=['GET'])
def display_ratings(id):
    query = f"SELECT * FROM Courses where id = {id};"
    courses = engine.execute(query)
    if request.method=='GET':
        query1 = f"SELECT * FROM Ratings r INNER JOIN Users u ON r.rater = u.user_id where r.course = {id};"
        results = engine.execute(query1)
        query2 = f"CALL GetaverageRating1({id});"
        rates = engine.execute(query2)
        return render_template('view_rate.html', results=results, rates=rates, courses=courses, id=id)

# Comment a course
@app.route('/comment_course/<int:id>', methods=['GET', 'POST'])
def comment_course(id):
    query = f"SELECT * FROM Courses where id = {id};"
    courses = engine.execute(query)
    if request.method == 'POST':
        # Randomly generating a 10-character rater user name.
        user_name = ''.join(random.choice(letters) for i in range(10))
        # Insert a new user as the rater.
        rater_id = insert_user(user_name)
        current_time = datetime.datetime.utcnow()
        comment = request.form['comment']
        new_comment_query = f"INSERT INTO Comments(commenter, course, comment, comment_time, likes, dislikes, reply) VALUES({rater_id}, {id}, '{comment}', '{current_time}', 0, 0, NULL);"
        engine.execute(new_comment_query)
        print("NEW COMMENT SUCCESSFULLY ADDED!!!!")
        return redirect('/')
    else:
        return render_template('comment_course.html', courses = courses, id = id)

# View comments of a course
@app.route('/view_comments/<int:id>', methods=['GET'])
def view_comments(id):
    query = f"SELECT * FROM Courses where id = {id};"
    courses = engine.execute(query)
    if request.method=='GET':
        query = f"SELECT * FROM Comments c INNER JOIN Users u ON c.commenter = u.user_id where course = {id};"
        comments = engine.execute(query)
        return render_template('view_comments.html', comments=comments, courses=courses, id=id)


# View sections of a course
@app.route('/view_sections/<int:id>', methods=['GET'])
def view_sections(id):
    query = f"SELECT * FROM Courses where id = {id};"
    courses = engine.execute(query)
    if request.method=='GET':
        query = f"SELECT * FROM Sections s where course = {id};"
        sections = engine.execute(query)
        return render_template('view_sections.html', sections=sections, courses=courses, id=id)

if __name__ == "__main__":
    app.run(debug=True)