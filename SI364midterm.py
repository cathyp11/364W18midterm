###############################
####### SETUP (OVERALL) #######
###############################

## Import statements
# Import statements
import os
from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError # Note that you may need to import more here! Check out examples that do what you want to figure out what.
from wtforms.validators import Required, Length # Here, too
from flask_sqlalchemy import SQLAlchemy
import requests
import json

## App setup code
app = Flask(__name__)
app.debug = True
app.use_reloader = True

## All app.config values
app.config['SECRET_KEY'] = 'hard to guess string from si364'
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://localhost/ycpark364midterm"
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

## Statements for db setup (and manager setup if using Manager)
db = SQLAlchemy(app)

## Error handling routes
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

######################################
######## HELPER FXNS (If any) ########
######################################




##################
##### MODELS #####
##################

class Name(db.Model):
    __tablename__ = "names"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64))

    def __repr__(self):
        return "{} (ID: {})".format(self.name, self.id)

class Location(db.Model):
    __tablename__ = 'location'
    id = db.Column(db.Integer, primary_key=True)
    restaurant = db.Column(db.String(100))
    address = db.Column(db.String(100))

    def __repr__(self):
        return "Address: {} | (ID: {})".format(self.address, self.id)

class Review(db.Model):
    __tablename__ = 'review'
    id = db.Column(db.Integer, primary_key=True)
    review = db.Column(db.String(280))
    rating = db.Column(db.Float)
    price = db.Column(db.String(4))
    location_id = db.Column(db.Integer, db.ForeignKey("location.id"))

    def __repr__(self):
        return "Review: {} | (ID: {})".format(self.review, self.id)
    
class Food(db.Model):
    __tablename__ = 'food'
    id = db.Column(db.Integer, primary_key=True)
    food = db.Column(db.String(100))
    reason = db.Column(db.String(280))

    def __repr__(self):
        return "Favorite Food: {} | (ID: {})".format(self.food, self.id)


###################
###### FORMS ######
###################

class NameForm(FlaskForm):
    name = StringField("Please enter your name.",validators=[Required()])
    submit = SubmitField()

class RestForm(FlaskForm):
    name = StringField('Please enter a restaurant in Ann Arbor. (Please spell them correctly.)', validators=[Required(), Length(min = 3, max = 280)])
    review = StringField('Please enter a review for the restaurant. (Please write in a sentence with a period.)', validators=[Required()])
    submit = SubmitField('Submit')

    def validate_review(self, field):
        if '.' not in field.data: 
            raise ValidationError('Review should be a sentence with a period')

class FoodForm(FlaskForm):
    food = StringField('Please enter your favorite food.', validators=[Required()])
    reason = StringField('Please enter a reason.', validators=[Required()])
    submit = SubmitField('Submit')

#######################
###### VIEW FXNS ######
#######################

@app.route('/', methods = ['GET', 'POST'])
def home():
    form = NameForm() # User should be able to enter name after name and each one will be saved, even if it's a duplicate! Sends data with GET
    if form.validate_on_submit():
        name = form.name.data
        newname = Name(name = name)
        db.session.add(newname)
        db.session.commit()
        return redirect(url_for('all_names'))
    return render_template('base.html',form = form)

@app.route('/names')
def all_names():
    names = Name.query.all()
    return render_template('name_example.html',names=names)


yelp_access_token = "ztsjq_LquhhLU5ABi4zWOIOISD-jy8UiWijyAzLb0yV7MChsj3pLa6ZP6yruRkTdS6M2SRvm3olECWEx6GTsE1JLEDkkHWS5oyWYYYSFfbAodGQ0-NmJFQMshTATWnYx"

@app.route('/restaurants', methods = ['GET', 'POST'])
def restaurants():
    form = RestForm()
    if request.method == 'POST' and form.validate_on_submit():
        name = form.name.data.title()
        review = form.review.data
        url = "https://api.yelp.com/v3/businesses/search?term=" + name + "&limit=1&location=annarbor"
        yelp_api = requests.get(url, headers = {'Authorization': "Bearer " + yelp_access_token, 'token_type': "Bearer"})
        data_y = json.loads(yelp_api.text)
        for b in data_y['businesses']:
            name = b['name']
            address = b['location']['address1']
            rating = b['rating']
            price = b['price']
            print(b)
        l = Location.query.filter_by(restaurant = name, address = address).first()   
        if l:
            loc = l.id
        else:
            l = Location(restaurant = name, address = address)
            db.session.add(l)
            db.session.commit()
            loc = l.id
        r = Review.query.filter_by(review = review, rating = rating, price = price, location_id = loc).first()
        if r:
            flash('Review already exists')
            return redirect(url_for('see_all_reviews'))
        else:
            r = Review(review = review, rating = rating, price = price, location_id = loc)
            db.session.add(r)
            db.session.commit()
            flash('Review successfully added')
            return redirect(url_for('restaurants'))
    errors = [e for e in form.errors.values()]
    if len(errors) > 0:
        flash("!! ERROR IN FORM SUBMISSION - " + str(errors))
    return render_template('restaurants.html', form = form)

@app.route('/food_form')
def food_form():
    form = FoodForm()
    return render_template('food_form.html', form = form)
    
@app.route('/fav_food', methods = ['GET', 'POST'])
def food():
    form = FoodForm(request.form)   
    if request.args:
        fav = request.args.get('food').title()
        reason = request.args.get('reason')
        f = Food(food = fav, reason = reason)
        db.session.add(f)
        db.session.commit()
        return render_template('food_results.html', fav=fav, reason=reason)
    flash(form.errors)
    return redirect(url_for('food_form'))

@app.route('/all_reviews')
def see_all_reviews():
    reviews = Review.query.all()
    review = []
    for r in reviews:
        l = Location.query.filter_by(id=r.location_id).first()
        tup = (r.review, l.restaurant)
        review.append(tup)
    return render_template('all_reviews.html', reviews = review)

@app.route('/all_restaurants')
def see_all_res():
    restaurants = Location.query.all()
    return render_template('all_restaurants.html', all_res = restaurants)

@app.route('/all_food')
def all_food():
    food = Food.query.all()
    return render_template('all_food.html', all_food = food)

## Code to run the application...

# Put the code to do so here!
# NOTE: Make sure you include the code you need to initialize the database structure when you run the application!
if __name__ == '__main__':
    db.create_all()
    app.run(use_reloader=True,debug=True)