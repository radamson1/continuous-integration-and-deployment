from app.models import Restaurant, User

def seed_users(db):
    # Check if there are any existing records in the users table
    existing_users = User.query.count()

    # If there are existing records, don't seed the database again
    if existing_users > 0:
        print("Users table already seeded. Skipping seeding process.")
        return
    
    # Define the data to seed the users table
    users_data = [
        {
            'username': 'yoshi',
            'name': 'Yoshi Yamamoto'
        },
        {
            'username': 'jane',
            'name': 'Jane Smith'
        },
        {
            'username': 'lisa',
            'name': 'Lisa Johnson'
        },
        {
            'username': 'alex',
            'name': 'Alex Brown'
        },
        {
            'username': 'michael',
            'name': 'Michael Wilson'
        }
    ]

    # Seed the users table with the data
    for data in users_data:
        user = User(**data)
        db.session.add(user)

    # Commit the changes to the database
    db.session.commit()

def seed_restaurants(db):
    # Check if there are any existing records in the restaurants table
    existing_restaurants_count = Restaurant.query.count()

    # If there are existing records, don't seed the database again
    if existing_restaurants_count > 0:
        print("Restaurants table already seeded. Skipping seeding process.")
        return

    # Seed the restaurants table with some initial data
    restaurants_data = [
        {
            'name': 'The Rustic Spoon',
            'street_address': '789 Oak Avenue',
            'phone': '555-123-4567',
            'description': 'A farm-to-table restaurant offering seasonal dishes.'
        },
        {
            'name': 'Sakura Sushi Bar',
            'street_address': '321 Cherry Blossom Lane',
            'phone': '555-987-6543',
            'description': 'Authentic Japanese sushi and sashimi.'
        },
        {
            'name': 'La Pizzeria Napoli',
            'street_address': '456 Pepperoni Road',
            'phone': '555-789-0123',
            'description': 'Traditional Neapolitan pizza cooked in a wood-fired oven.'
        },
        {
            'name': 'Café du Monde',
            'street_address': '555 French Quarter Avenue',
            'phone': '555-456-7890',
            'description': 'A charming café famous for its beignets and café au lait.'
        },
        {
            'name': 'Taste of India',
            'street_address': '987 Curry Street',
            'phone': '555-234-5678',
            'description': 'Authentic Indian cuisine with a wide range of vegetarian and non-vegetarian options.'
        },
        {
            'name': 'The Hungry Bear Diner',
            'street_address': '101 Pancake Place',
            'phone': '555-876-5432',
            'description': 'A cozy diner serving hearty breakfasts and classic American comfort food.'
        },
        {
            'name': 'Mama Mia Trattoria',
            'street_address': '246 Spaghetti Avenue',
            'phone': '555-345-6789',
            'description': 'Family-owned Italian trattoria specializing in homemade pasta and sauces.'
        },
        {
            'name': 'The Green Leaf Salad Bar',
            'street_address': '789 Lettuce Lane',
            'phone': '555-654-3210',
            'description': 'A health-conscious salad bar with a wide selection of fresh ingredients.'
        },
        {
            'name': 'Thai Orchid Restaurant',
            'street_address': '456 Jasmine Street',
            'phone': '555-210-9876',
            'description': 'Exquisite Thai cuisine with bold flavors and aromatic spices.'
        },
        {
            'name': 'Smokehouse BBQ Pit',
            'street_address': '888 Barbecue Boulevard',
            'phone': '555-543-2109',
            'description': 'Authentic Southern barbecue slow-cooked to perfection.'
        }
    ]


    for restaurant_info in restaurants_data:
        restaurant = Restaurant(**restaurant_info)
        db.session.add(restaurant)

    db.session.commit()
    print("Restaurants table seeded successfully.")

if __name__ == '__main__':
    seed_restaurants()
