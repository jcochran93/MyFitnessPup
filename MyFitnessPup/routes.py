from datetime import datetime
from flask import jsonify, request, render_template, url_for, redirect, session
from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    login_required,
    logout_user,
    current_user,
)
from werkzeug.security import check_password_hash, generate_password_hash

from MyFitnessPup import app, db
from MyFitnessPup.forms import RegisterForm, LoginForm
from MyFitnessPup.models import UserInfo, Pets, DogFood, PetWeight

loginManager = LoginManager()
loginManager.init_app(app)
loginManager.login_view = "userLogin"


@loginManager.user_loader
def load_user(user_id):
    return UserInfo.query.get(int(user_id))


# Members Login Route
@app.route("/login", methods=["POST", "GET"])
def userLogin():

    form = LoginForm()

    if form.validate_on_submit():
        user = UserInfo.query.filter_by(username=form.username.data).first_or_404()

        if check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for("dashboard"))
        else:
            return "Incorrect Password"

    return render_template("login.html", form=form)


@app.route("/register", methods=["POST", "GET"])
def userRegister():
    error = None
    form = RegisterForm()

    if not form.username.data:
        error = "Username is required"
    elif not form.password.data:
        error = "Password is required"

    if error is None:
        new_user = UserInfo(
            username=form.username.data,
            password=generate_password_hash(form.password.data),
        )

        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for("userLogin"))
        except:
            return "There was an error creating your account"

    return render_template("register.html", form=form)


@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():

    pets = Pets.query.filter_by(owner_id=current_user.id)
    numberOfPets = pets.count()
    # print(pets)

    if request.method == "POST":
        # Get the name of an existing pet
        # or create a new pet for the current user
        pet_name = request.form["new-pet"] or request.form["pet-name"]

        if pet_name == request.form["new-pet"]:
            newPet = Pets(name=pet_name, owner_id=current_user.id)
            db.session.add(newPet)
            db.session.commit()
        session["pet_name"] = pet_name
        currentPet = Pets.query.filter_by(
            name=pet_name, owner_id=current_user.id
        ).first()
        session["pet_id"] = currentPet.id
        return redirect(url_for("index"))

    else:

        return render_template(
            "dashboard.html", pet_list=pets, numberOfPets=numberOfPets
        )


@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    session.clear()
    logout_user()
    return redirect(url_for("userLogin"))


@app.route("/", methods=["POST", "GET"])
@login_required
def index():

    petName = session.get("pet_name")
    petId = session.get("pet_id")
    selectedDate = session.get("date") or datetime.utcnow()

    if request.method == "POST":
        foodContent = request.form["content"]
        mealContent = request.form["meal"]
        kCals = request.form["calories"]

        newFood = DogFood(
            pet_id=petId, brandName=foodContent, meal=mealContent, calories=kCals
        )

        if newFood.calories == "":
            newFood.calories = 0

        try:
            db.session.add(newFood)
            db.session.commit()
            return redirect("/")
        except:
            return "There was a problem adding your food."

    else:
        foods = (
            DogFood.query.filter_by(pet_id=petId).order_by(DogFood.date_created).all()
        )
        petOwner = Pets.query.filter_by(id=petId).first()
        return render_template(
            "index.html",
            foods=foods,
            petName=petName,
            petId=petId,
            ownerId=petOwner.owner_id,
            date=selectedDate,
        )


@app.route("/delete/<int:id>")
@login_required
def delete(id):
    food_to_delete = DogFood.query.get_or_404(id)

    try:
        db.session.delete(food_to_delete)
        db.session.commit()
        return redirect("/")

    except:
        return "There was a problem deleting that item."


@app.route("/weight", methods=["POST", "GET"])
@login_required
def weight():

    petId = session.get("pet_id")

    if request.method == "POST":
        weight = request.form["weight"]
        date = request.form["date"]
        date = datetime.strptime(date, "%Y-%m-%d")

        newWeight = PetWeight(pet_id=petId, weight=weight, date_logged=date)
        db.session.add(newWeight)
        db.session.commit()

    elif request.method == "GET":
        weightHistory = PetWeight.query.filter_by(pet_id=petId).all()
        data = {}

        for history in weightHistory:
            date = history.date_logged.strftime("%Y-%m-%d")
            data[date] = history.weight

        return jsonify({"weight": data})

    return redirect("/")


@app.route("/date", methods=["POST", "GET"])
@login_required
def date():

    if request.method == "POST":

        content = request.json
        # print(content)

    session["date"] = content["date"][:10]

    return redirect("/")
