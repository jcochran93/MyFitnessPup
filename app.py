from flask import Flask, jsonify, request, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

db = SQLAlchemy(app)

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

class UserInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    dogFoods = db.relationship('DogFood', backref='user_info', lazy=True)
    



#Members Login Route
@app.route("/login", methods=['POST','GET'])
def userLogin():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = None

        try:
            user = UserInfo.query.filter_by(username=username).first_or_404()
            global userId
            userId = user.id
            if(check_password_hash(user.password, password)):
                 return redirect("/")
            else:
                return "Incorrect Password"

        except:
            return "Username does not exist"

    return render_template('login.html')

@app.route("/register", methods=['POST','GET'])
def userRegister():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        if not username:
            error = 'Username is required'
        elif not password:
            error = 'Password is required'

        if error is None:
            new_user = UserInfo(username=username, password=generate_password_hash(password))

            try:
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for('userLogin'))
            except:
                return "There was an error creating your account"
    else:
        
        return render_template('register.html')

@app.route("/", methods=['POST', 'GET'])
def index():

    userId = 1

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


if __name__ =="__main__":
    app.run(debug=True)
