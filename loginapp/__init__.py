"""EcoCleanUp Hub - Main application initialization."""
from flask import Flask

app = Flask(__name__)

# Set secret key for session security
app.secret_key = 'EcoCleanUp_Sustainable_Community_2026_Secret_Key'

# Set upload folder for profile images
import os
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Set up database connection
from loginapp import connect
from loginapp import db
db.init_db(app, connect.dbuser, connect.dbpass, connect.dbhost, connect.dbname,
           connect.dbport)

# Import all route modules
from loginapp import user
from loginapp import volunteer
from loginapp import event_leader
from loginapp import admin

# Import utils LAST to register template filters and context processors
from loginapp import utils

# Debug: Print all registered filters
if app.debug:
    print("\n=== Registered Jinja2 Filters ===")
    for filter_name in app.jinja_env.filters.keys():
        print(f"  - {filter_name}")
    print("===============================\n")