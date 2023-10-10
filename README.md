# OnlineGroceryStore
A web application for managing a grocery store that that will help grocery stores run smoothly and sell their products online. This website will be like the store's digital manager, making it easy to sell groceries to customers.
## Technologies used
+ HTML: used for structuring web pages.
+ Bootstrap 5: For styling the web pages.
+ Jinja2: Templating Engine.
+ Flask: Manages HTTP requests, routing, and provides a foundation for the application structure.
+ Flask Login: Create user accounts, handle login/logout. 
+ Flask-SQLAlchemy: Simplifies Pythonic database interactions with class-based table and record representation.
+ SQLite: Data Storage
+ Flask-RESTful: Simplify the development of RESTful APIs in Flask
## Database Schema
1. roles_users Table
    1. **id (Primary Key)**: Unique identifier for role assignments.
    2.  **user_id (Foreign Key)**: References the id in the user table, establishing a relationship between users and 
roles.
    3. **role_id (Foreign Key)**: References the id in the role table, specifying the user's role.
2. role Table
    1. **id (Primary Key)**: Unique identifier for roles.
    2. **name**: The name of the role (e.g., "Admin" or "Customer").
    3. **description**: A description of the role.
3. user Table
    1.** id (Primary Key)**: Unique identifier for users.
    2.** email**: User's email address (unique).
    3.** username**: User's username (unique).
    4. **password**: User's hashed password.
    5.** active**: Boolean flag indicating whether the user account is active.
    6. **fs_uniquifier**: A unique string associated with the user.
    7.** roles**: A many-to-many relationship with the role table, allowing users to have multiple roles.
4. category Table
    1. **category_id (Primary Key)**: Unique identifier for product categories.
    2. **category_name**: The name of the category.
    3. **products**: One-to-many relationship with the products table, linking products to their respective 
categories.
5. products Table
    1. **product_id (Primary Key)**: Unique identifier for products.
    2. **product_name**: The name of the product (unique).
    3. **category_id (Foreign Key)**: References the category_id in the category table, associating products with 
categories.
    4.** price**: The price of the product, with a check constraint to ensure its non-negative.
    5. **unit**: The unit of measurement for the product (e.g., "unit").
    6. **quantity**: The quantity of the product available in stock, with a check constraint to ensure its nonnegative.
6. cart Table
    1. **user_id (Foreign Key, Primary Key)**: References the id in the user table, establishing a relationship 
between users and their cart items.
    2. **product_id (Foreign Key, Primary Key)**: References the product_id in the products table, specifying the 
product in the cart.
    3. **quantity**: The quantity of the product in the user's cart, with a check constraint to ensure its nonnegative.
    4. **product**: Relationship with the Products table, linking cart items to products.
7. bills Table
      1. **bill_id (Primary Key)**: Unique identifier for bills.
      2. **user_id (Foreign Key)**: References the id in the user table, indicating the user associated with the bill.
    3.** total_amount**: The total amount of the bill, with a check constraint to ensure its non-negative.
    4. **bill_items**: One-to-many relationship with the bill_items table, linking bills to their respective bill items.
9. bill_items Table
    1. **bill_item_id (Primary Key)**: Unique identifier for bill items.
    2.** bill_id (Foreign Key)**: References the bill_id in the bills table, associating bill items with bills.
    3.**product_name**: The name of the product in the bill.
    4. **price**: The price of the product in the bill, with a check constraint to ensure its non-negative.
    5. **quantity**: The quantity of the product in the bill, with a check constraint to ensure its non-negative.
  
  
## API Design
This project implements APIs for Category which includes creating, reading, updating and deleting a category. 
Also implements APIs for Products which includes creating, reading, updating, deleting a product and list all 
products present in a particular category.
## Architecture and Features
The project structure is centered around an entry point, app.py, and features distinct directories, including 
application, db_directory, static, and templates. Within the application directory, there are modules 
such as config.py for configuring the app, database.py for establishing the database, models.py for 
defining data tables, api.py for RESTful APIs, validation.py for validations and routes.py for housing app 
routes. The db_directory stores the SQLite3 database file, while static contains CSS for page styling, and 
templates houses all HTML pages. Additionally, a requirements.txt file lists the app packages along with 
their respective versions.

The app offers user registration and login, with admin privileges including inventory and product management. 
Users can browse and purchase products, perform searches by category or product name, manage their 
cart, view out-of-stock items, and calculate total amounts. Also implemented Restful APIs for category and 
products. All user inputs are validated for accuracy.

##  Running the App
To run the app, follow these steps:
1. Execute the local_setup.sh script to set up the environment and install required packages.
2. Launch the app by running local_run.sh. You can access the app at http://127.0.0.1:5000/ to begin using it.
