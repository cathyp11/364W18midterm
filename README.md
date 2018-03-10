#### Description

You can write a review about a restaurant in Ann Arbor. The restaurants are found using Yelp API and saves the address of the restaurant in Restaurants SQL database and the review for the restaurant in Review SQL database. There is also another form for submitting your favorite food and returns a statement. Those favorite food list is also saved in a SQL database.


#### Routes

- http://localhost:5000/ -> base.html
- http://localhost:5000/names -> name_example.html
- http://localhost:5000/restaurants -> restaurants.html
- http://localhost:5000/food_form -> food_form.html
- http://localhost:5000/fav_food -> food_results.html 
	- If clicked without submitting the form, it goes back to food_form because it can't save data using GET request. Thus, an empty dictionary shows up as flash_get_messages().
- http://localhost:5000/all_reviews -> all_reviews.html
- http://localhost:5000/all_restaurants -> all_restaurants.html
- http://localhost:5000/all_food -> all_food.html
- http://localhost:5000/404 -> 404.html


#### Code Requirements

**Note that many of these requirements go together!**

- [o] **Ensure that the `SI364midterm.py` file has all the setup (`app.config` values, import statements, code to run the app if that file is run, etc) necessary to run the Flask application, and the application runs correctly on `http://localhost:5000` (and the other routes you set up)**
- [o] **Add navigation in `base.html` with links (using `a href` tags) that lead to every other viewable page in the application. (e.g. in the lecture examples from the Feb 9 lecture, [like this](https://www.dropbox.com/s/hjcls4cfdkqwy84/Screenshot%202018-02-15%2013.26.32.png?dl=0) )**
- [o] **Ensure that all templates in the application inherit (using template inheritance, with `extends`) from `base.html` and include at least one additional `block`.**
- [o] **Include at least 2 additional template `.html` files we did not provide.**
- [o] **At least one additional template with a Jinja template for loop and at least one additional template with a Jinja template conditional.
    - These could be in the same template, and could be 1 of the 2 additional template files.**
- [o] **At least one errorhandler for a 404 error and a corresponding template.**
- [o] **At least one request to a REST API that is based on data submitted in a WTForm.**
- [o] **At least one additional (not provided) WTForm that sends data with a `GET` request to a new page.** 
	- FoodForm() makes a GET request to food_results.html.
- [o] **At least one additional (not provided) WTForm that sends data with a `POST` request to the *same* page.**
- [o] **At least one custom validator for a field in a WTForm.**
- [o] **At least 2 additional model classes.**
- [o] **Have a one:many relationship that works properly built between 2 of your models.**
- [o] **Successfully save data to each table.**
- [o] **Successfully query data from each of your models (so query at least one column, or all data, from every database table you have a model for).**
- [o] **Query data using an `.all()` method in at least one view function and send the results of that query to a template.**
- [o] **Include at least one use of `redirect`. (HINT: This should probably happen in the view function where data is posted...)**
- [o] **Include at least one use of `url_for`. (HINT: This could happen where you render a form...)**
- [o] **Have at least 3 view functions that are not included with the code we have provided. (But you may have more! *Make sure you include ALL view functions in the app in the documentation and ALL pages in the app in the navigation links of `base.html`.*)**

### Additional Requirements for an additional 200 points (to reach 100%) -- an app with extra functionality!

[o] * **(100 points) Include an *additional* model class (to make at least 4 total in the application) with at least 3 columns. Save data to it AND query data from it; use the data you query in a view-function, and as a result of querying that data, something should show up in a view. (The data itself should show up, OR the result of a request made with the data should show up.)** 

[o] * **(100 points) Write code in your Python file that will allow a user to submit duplicate data to a form, but will *not* save duplicate data (like the same user should not be able to submit the exact same tweet text for HW3).** 
	- Only for RestForm() and not NameForm() or FoodForm().