from flask import render_template, request, redirect, url_for, abort
from .models import db, Restaurant, Review
from app import app
from flask import jsonify
from app.models import Restaurant, Review, User
from datetime import datetime
from seeder.seed import seed_restaurants, seed_users
from sqlalchemy import func
from decimal import Decimal

@app.route("/")
def index():
    seed_restaurants(db)
    seed_users(db)
    restaurants = Restaurant.query.all()
    return render_template('index.html', restaurants=restaurants)

@app.route("/restaurant-detail/<int:restaurant_id>")
def restaurant_detail(restaurant_id):
    # Retrieve the restaurant from the database using Session.get()
    restaurant = db.session.get(Restaurant, restaurant_id)
    
    # Check if the restaurant exists
    if not restaurant:
        abort(404)  # Return a 404 Not Found error if the restaurant doesn't exist
    
    # Retrieve the reviews for the restaurant
    reviews = Review.query.join(User, Review.reviewed_by == User.id).filter(Review.restaurant_id==restaurant_id).all()
 
    # Retrieve users
    users = User.query.all()

    # Get average rating
    average_rating = get_average_rating(restaurant_id)
    if average_rating is None:
        stars = 0
    else:
        stars = int(average_rating.quantize(Decimal('0')))

    return render_template('restaurant_detail.html', restaurant=restaurant, reviews=reviews, users=users, rating=average_rating, stars=stars)

@app.route("/add-review/<int:restaurant_id>", methods=['GET', 'POST'])
def add_review(restaurant_id):
    if request.method == 'POST':
        review = request.form['review']
        rating = int(request.form['rating'])
        user_id = int(request.form['user_id'])

        # Get the current date and time
        current_date = datetime.now()

        review_obj = Review(restaurant_id=restaurant_id, review=review, reviewed_by=user_id, rating=rating, date_reviewed=current_date)
        db.session.add(review_obj)
        db.session.commit()
        return redirect(url_for('restaurant_detail', restaurant_id=restaurant_id))
    else:
        restaurant = Restaurant.query.get_or_404(restaurant_id)
        return render_template('add_review.html', restaurant=restaurant)


def get_average_rating(restaurant_id):
  """Calculates the average rating for a restaurant.

  Args:
      restaurant_id: The ID of the restaurant.

  Returns:
      The average rating as a float, or None if no reviews exist.
  """
  # Get all reviews for the restaurant
  reviews = Review.query.filter_by(restaurant_id=restaurant_id).all()

  # Check if there are any reviews
  if not reviews:
    return None

  # Calculate the average rating using SQLAlchemy's func.avg
  average_rating = db.session.query(func.avg(Review.rating)).filter_by(restaurant_id=restaurant_id).scalar()
  
  average_rating = Decimal(str(average_rating)).quantize(Decimal('0.1'))  # Round to one decimal place

  # Return the average rating
  return average_rating