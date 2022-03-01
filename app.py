from flask import Flask, jsonify, request, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

app.config['SECRET_KEY'] = 'thisIsASecretKey'

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return UserInfo.query.get(int(user_id))


class DogFood(db.Model):
    id = db.Column(db.Integer, primary_key=True )
    user_id = db.Column(db.Integer, db.ForeignKey('user_info.id'), nullable=False)
    brandName = db.Column(db.String(50), nullable=False)
    calories = db.Column(db.Integer, default=300, nullable=False)
    meal = db.Column(db.String(15), nullable=False)
    pet = db.Column(db.String(50), nullable=False, default="Thor")
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    

    def __repr__(self):
        return '<Food %r>' % self.id

class UserInfo(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    dogFoods = db.relationship('DogFood', backref='user_info', lazy=True)
    pets = db.relationship('Pets', backref='user_info', lazy=True)

class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Password"})
    
    submit = SubmitField("Register")

    def validate_username(self, username):
        existing_user_username = UserInfo.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                "That username already exists. Please choose a different one.")

class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Password"})
    
    submit = SubmitField("Login")

class Pets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user_info.id'), nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    date_logged = db.Column(db.DateTime, default=datetime.utcnow)



#Members Login Route
@app.route("/login", methods=['POST','GET'])
def userLogin():

    form =  LoginForm()

    if form.validate_on_submit():
        user = UserInfo.query.filter_by(username=form.username.data).first_or_404()
    
        if(check_password_hash(user.password, form.password.data)):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            return "Incorrect Password"

    return render_template('login.html', form=form)

@app.route("/register", methods=['POST','GET'])
def userRegister():
    error = None
    form = RegisterForm()
    
    if not form.username.data:
        error = 'Username is required'
    elif not form.password.data:
        error = 'Password is required'

    if error is None:
        new_user = UserInfo(username=form.username.data, password=generate_password_hash(form.password.data))

        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('userLogin'))
        except:
            return "There was an error creating your account"



    return render_template('register.html', form=form)

@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    return render_template('dashboard.html')


@app.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('userLogin'))


@app.route("/", methods=['POST', 'GET'])
@login_required
def index():

    userId = current_user.id

    petName = "Thor"

    if request.method =='POST':
        food_content = request.form['content']
        meal_content = request.form['meal']
        kcals = request.form['calories']

        new_food = DogFood(brandName=food_content, meal=meal_content, calories=kcals, user_id=userId)
        
        if new_food.calories == '':
            new_food.calories = 0

        try:
            db.session.add(new_food)
            db.session.commit()
            return redirect("/")
        except:
            return "There was a problem adding your food."

    else:
        foods = DogFood.query.order_by(DogFood.date_created).all()
        return render_template('index.html', foods=foods, petName=petName)


@app.route("/delete/<int:id>")
def delete(id):
    food_to_delete = DogFood.query.get_or_404(id)

    try:
        db.session.delete(food_to_delete)
        db.session.commit()
        return redirect('/')
    
    except:
        return "There was a problem deleting that item."

@app.route("/weight-data/<int:id>", methods=["POST", "GET"])
def weight(id):

    userName = UserInfo.query.get_or_404(id)

    return jsonify({"user" : userName.username})

if __name__ =="__main__":
    app.run(debug=True)
