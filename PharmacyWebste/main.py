from flask import Flask,render_template
from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

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
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT user.Id, user.PersonId, person.Name, person.Contact, person.Email, lookup.Value, person.CNIC, user.Username, user.Password, user.Salary, user.Hiring_date, user.User_role FROM user, person, lookup where user.PersonId= person.Id and lookup.Id= person.Gender;')
    data = cursor.fetchall()
    print(data)
    mysql.connection.commit()
    cursor.close()
    # results = User.query.first()
    return render_template('manageusers.html', active_page='home', data=data)

@app.route("/addmedicine")
def medicine():
    return render_template('addmedicine.html')

if __name__ == '__main__':
    app.run(debug=True)

