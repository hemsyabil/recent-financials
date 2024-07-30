from flask import Flask, redirect, render_template, jsonify, request, session
from access_data import DATA_JSON, filtered_data, total_i_owe_all, name_mapping
import humanize
import pandas as pd
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_session import Session

finance_app = Flask(__name__)
finance_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
finance_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
finance_app.config['SECRET_KEY'] = 'your_secret_key'
finance_app.config['SESSION_TYPE'] = 'filesystem'

db = SQLAlchemy(finance_app)
bcrypt = Bcrypt(finance_app)

# Initialize the Flask-Session extension
Session(finance_app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password_hash = bcrypt.generate_password_hash(password).decode(
            'utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)


with finance_app.app_context():
    db.create_all()


@finance_app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        new_user = User(name, email, password)
        db.session.add(new_user)
        db.session.commit()

        return redirect('/login')

    return render_template('register.html')


@finance_app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            session['email'] = user.email
            return redirect('/')
        else:
            return render_template('login.html', error='Invalid user')

    return render_template('login.html')


@finance_app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect('/login')


@finance_app.route('/')
def dashboard():
    if 'email' in session:
        user = User.query.filter_by(email=session['email']).first()
        total_owed = humanize.intcomma(int(total_i_owe_all))

        return render_template('dashboard.html',
                               title="Financial Dashboard",
                               name="Financial Dashboard",
                               user=user,
                               DATA_DICT=DATA_JSON,
                               filtered_data=filtered_data,
                               total_owed=total_owed)

    return redirect('/login')


@finance_app.route('/<name>')
def personal_dashboard(name):
    if 'email' in session:
        sheet_name = name_mapping.get(name)

        if not sheet_name:
            return jsonify({"error": "Record not found"}), 404

        record = DATA_JSON.get(sheet_name, [])
        total_owed = filtered_data[sheet_name]["Total I Owe"]

        df = pd.DataFrame(record)
        table_html = df.to_html(classes='table table-striped table-hover',
                                index=False)

        return render_template('personal-dashboard.html',
                               title="Recent Financials - Dashboard",
                               filtered_data=filtered_data,
                               name=sheet_name,
                               total_owed=total_owed,
                               table=table_html)

    return redirect('/login')


if __name__ == "__main__":
    finance_app.run(host='0.0.0.0', port=8080, debug=True)
