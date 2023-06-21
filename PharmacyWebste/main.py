from datetime import datetime

from flask import Flask, render_template, request, redirect, session, flash
from flask_mysqldb import MySQL
from forms import UserForm
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.secret_key = "your_secret_key_here"

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'pharmacy'

mysql = MySQL(app)

#
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/pharmacy'
# db = SQLAlchemy(app)
#
# class Lookup(db.Model):
#     '''
#     id, value, category
#     '''
#     id = db.Column(db.Integer, primary_key=True)
#     value = db.Column(db.String(30), nullable=False)
#     category = db.Column(db.String(30), nullable=False)
#     '''
#          Relationship bw lookup, person and user
#     '''
#     gender = db.relationship('Person', backref='lookup', lazy=True)
#     user_role = db.relationship('User', backref='lookup', lazy=True)
#
# class Person(db.Model):
#     '''
#     id, name, contact, email, gender, cnic
#     '''
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(80), nullable=False)
#     contact = db.Column(db.String(15), nullable=False)
#     email = db.Column(db.String(120), nullable=False)
#     gender = db.Column(db.String(11),db.ForeignKey('lookup.id'), nullable=False)
#     cnic = db.Column(db.String(80), nullable=False)
#     '''
#      Relationship bw user and person
#     '''
#     personuser= db.relationship('User', backref='person', lazy=True)
#
# class User(db.Model):
#     '''
#     id, personid, username, password, slaray, hiringdate, user_role
#     '''
#     id = db.Column(db.Integer, primary_key=True)
#     personid = db.Column(db.Integer,db.ForeignKey('person.id'), nullable=False)
#     username = db.Column(db.String(30), nullable=False)
#     password = db.Column(db.String(30), nullable=False)
#     salary = db.Column(db.Integer, nullable=False)
#     hiring_date = db.Column(db.String(12), nullable=True)
#     user_role = db.Column(db.Integer, db.ForeignKey('lookup.id'), nullable=False)



@app.route("/")
def layout():
    form = UserForm()
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT user.Id, user.PersonId, person.Name, person.Contact, person.Email, lookup.Value, person.CNIC, user.Username, user.Password, user.Salary, user.Hiring_date, user.User_role FROM user, person, lookup where user.PersonId= person.Id and lookup.Id= person.Gender;')
    data = cursor.fetchall()
    print(data)
    mysql.connection.commit()
    cursor.close()
    status = session.get("status", None)  # Retrieve the status from session variable
    session.pop("status", None)  # Remove the status from session to clear it
    # results = User.query.first()


    return render_template('manageusers.html', active_page='home', data=data, status=status, form=form)


# Adding User

@app.route("/addUser", methods=['POST', 'GET'])
def addUser():
    form = UserForm(request.form)
    # form = UserForm(request.form)
    if request.method == 'POST' and form.validate():
        name = request.form['name']
        email = request.form['email']
        contact = request.form['contact']
        gender = request.form['gender']
        cnic = request.form['cnic']
        username = request.form['username']
        password = request.form['password']
        salary = request.form['salary']
        userrole = request.form['userrole']
        date = datetime.now()

        # Create a cursor to execute SQL statements
        cursor = mysql.connection.cursor()

        try:
            # Construct the SQL query for inserting data into "person" table
            person_query = "INSERT INTO person (name, contact, email, gender, cnic) VALUES (%s, %s, %s, %s, %s)"
            person_values = (name, contact, email, gender, cnic)

            # Execute the person query
            cursor.execute(person_query, person_values)

            # Get the generated person ID
            person_id = cursor.lastrowid

            # Construct the SQL query for inserting data into "user" table
            user_query = "INSERT INTO user (personid, username, password, salary, user_role, hiring_date) VALUES (%s, %s, %s, %s, %s,%s )"
            user_values = (person_id, username, password, salary, userrole, date)

            # Execute the user query
            cursor.execute(user_query, user_values)

            # Commit the changes to the database
            mysql.connection.commit()
            session["status"] = "done"
            return redirect("/")

        except mysql.connector.Error as error:
            # Rollback the transaction in case of any error
            mysql.connection.rollback()
            return f'Error: {error}'
        finally:
            # Close the cursor
            cursor.close()
        flash('Form submitted successfully!', 'success')
    else:

        # Handle form validation errors
        for field, errors in form.errors.items():
            for error in errors:
                pass
                 # flash(f"Error in {getattr(form, field).label.text}: {error}", "danger")
        # Populate the form with submitted data

        # Repeat the above line for other form fields
    return render_template('manageusers.html', form=form)


@app.route("/addmedicine")
def medicine():
    return render_template('addmedicine.html')



if __name__ == '__main__':
    app.run(debug=True)

