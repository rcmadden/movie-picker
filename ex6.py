# Extend the movie picker Flask application from exercise 5 a database, forms, user registration/login, sessions, and (bonus) an AJAX call. The new pieces of functionality we want are:

# Store the movie categories in a database, replacing the list of default categories.
# Allow users to register and log in, storing user credentials in the database.
# Allow logged in users to add new categories to the database.
# (Bonus) Allow the logged in user to add or remove movies on their "list" using AJAX.
# A basic solution is likely to have the following pieces:

# A new "model" layer which will talk to a database. I recommend sqlite3 and have covered it in the sections below.
# A "users" table which contains email addresses and password hashes (and any other data you wish to collect, e.g. name).
# A "categories" table which contains category names.
# A third table for storing lists of movies. The common way of doing this is to create a many-to-many relation between users and movie titles (i.e. many rows of (user_id, movie_title) data for a given user_id).
# A template for displaying a login form and a view for handling the form (e.g. /login)
# A template for displaying a registration form and a view for handling the form (e.g. /register)
# A template for displaying the "add category" form and a view for handling the form (e.g. /add_category)
# A view for logging users out of the site (e.g. /logout)
# A view for displaying the current user's list of movies (e.g. GET /my_movies)
# A view for adding/removing movies from the user's list of movies (e.g. POST /my_movies)
# (Bonus) JavaScript code for allowing the user to add/remove movies via AJAX requests. I recommend jQuery.

