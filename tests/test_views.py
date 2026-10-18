# test_views.py

import os
# Set the application environment to testing so that Pytest will use the test database
os.environ['APP_ENVIRONMENT'] = 'testing'

import pytest
from app import db, app
from app.models import Restaurant, Review, User
from datetime import datetime
from app.views import get_average_rating
from sqlalchemy import func
from decimal import Decimal

@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all() 

@pytest.fixture
def sample_data():
    # Create sample users
    user1 = User(username='user1', name='User One')
    user2 = User(username='user2', name='User Two')
    
    # Add users to the database
    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()

    current_date = datetime.now()

     # Create a sample restaurant
    restaurant = Restaurant(name='Test Restaurant', street_address='789 Oak St', phone='456-789-0123', description='A test restaurant')
    db.session.add(restaurant)
    db.session.commit()

    # Create sample reviews
    review1 = Review(restaurant_id=restaurant.id, review='Review 1', rating=4, reviewed_by=user1.id, date_reviewed=current_date)
    review2 = Review(restaurant_id=restaurant.id, review='Review 2', rating=5, reviewed_by=user2.id, date_reviewed=current_date)
    db.session.add_all([review1, review2])
    db.session.commit()

def test_index(client, sample_data):
    # Create some sample restaurants
    restaurant1 = Restaurant(name='Restaurant 1', street_address='123 Main St', phone='123-456-7890')
    restaurant2 = Restaurant(name='Restaurant 2', street_address='456 Elm St', phone='987-654-3210')
    db.session.add(restaurant1)
    db.session.add(restaurant2)
    db.session.commit()

    # Test the index route
    response = client.get('/')
    # print(response)
    assert response.status_code == 200
    assert b'Restaurant 1' in response.data
    assert b'Restaurant 2' in response.data

def test_restaurant_detail(client, sample_data):
    # Create a sample restaurant and a review for it
    restaurant = Restaurant(name='Test Restaurant', street_address='789 Oak St', phone='456-789-0123')
    db.session.add(restaurant)
    db.session.commit()


    # Get the ID of the first user
    first_user = User.query.first()

    # Get the current date and time
    current_date = datetime.now()

    # Create a review for the restaurant with one of the sample users as the reviewer
    review = Review(restaurant_id=restaurant.id, review='Test review', rating=5, reviewed_by=first_user.id, date_reviewed=current_date)
    db.session.add(review)
    db.session.commit()

    # Test the restaurant detail route
    response = client.get('/restaurant-detail/' + str(restaurant.id))
    assert response.status_code == 200
    assert b'Test Restaurant' in response.data
    assert b'Test review' in response.data

def test_add_review(client, sample_data):
    # Create a sample restaurant
    restaurant = Restaurant(name='Test Restaurant', street_address='789 Oak St', phone='456-789-0123')
    db.session.add(restaurant)
    db.session.commit()

    # Get the ID of the first user
    first_user = User.query.first()

    # Test the add review route
    response = client.post('/add-review/' + str(restaurant.id), data={'review': 'Test review', 'rating': 5, 'user_id': first_user.id})
    assert response.status_code == 302  # Check for redirect after successful POST request
    assert response.headers['Location'] == '/restaurant-detail/' + str(restaurant.id)

    # Verify that the review was added
    assert Review.query.filter_by(restaurant_id=restaurant.id).count() == 1


def test_get_average_rating(client, sample_data):
    """
    TODO: implement test to get average rating

    """
    pass

def test_get_average_rating_no_reviews(client):
    """
    TODO: implement test to get average rating when no review has been submitted for the restaurant

    """
    pass