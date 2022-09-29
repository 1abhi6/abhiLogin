from flask import Flask, render_template, request, redirect, session
import mysql.connector
import os


app = Flask(__name__)

app.secret_key = os.urandom(24)

conn = mysql.connector.connect(
    host="remotemysql.com", user="VyeewT1aHc", password="x5Eh7C7OWH", database="VyeewT1aHc")
cursor = conn.cursor()


@app.route('/')
def home():
    if 'userId' in session:
        return render_template('index.html')
    else:
        return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/home')
def index():
    if 'userId' in session:
        return render_template('index.html')
    else:
        return redirect('/')

# For login validation


@app.route('/loginValidation', methods=['POST'])
def loginValidation():
    email = request.form.get('email')
    password = request.form.get('password')
    cursor.execute("""
        SELECT * FROM `users`
        WHERE `Email` LIKE '{}' AND `Password` LIKE '{}'
        """.format(email, password))
    users = cursor.fetchall()
    if len(users) > 0:
        session['userId'] = users[0][0]
        return redirect('/home')
    else:
        return redirect('/')

# For registration


@app.route('/registerUser', methods=['POST'])
def registerUser():
    name = request.form.get('uname')
    email = request.form.get('uemail')
    password = request.form.get('upassword')

    cursor.execute("""
    INSERT INTO `users`(
        `userId`,`Name`,`Email`,`Password`
    )VALUES
    (NULL,'{}','{}','{}')
    """.format(name, email, password))
    conn.commit()

    cursor.execute("""
    SELECT * FROM `users` 
    WHERE `Email` LIKE '{}'
    """.format(email))
    myUser = cursor.fetchall()
    session['userId'] = myUser[0][0]
    return redirect('/home')


@app.route('/logout')
def logout():
    session.pop('userId')
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
