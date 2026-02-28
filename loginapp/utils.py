"""Utility functions for EcoCleanUp Hub."""
from loginapp import app
from flask import session, redirect, url_for, render_template
from functools import wraps
from datetime import datetime

def login_required(f):
    """Decorator to require login for a route."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'loggedin' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def role_required(*roles):
    """Decorator to require specific role(s) for a route."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'loggedin' not in session:
                return redirect(url_for('login'))
            if session['role'] not in roles:
                return render_template('access_denied.html'), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def format_datetime(value, format='%d %b %Y'):
    """Format datetime for display."""
    if value is None:
        return ''
    if isinstance(value, str):
        # If it's a string, try to parse it
        try:
            value = datetime.strptime(value, '%Y-%m-%d')
        except:
            return value
    return value.strftime(format)

def get_rating_stars(rating):
    """Convert numeric rating to star HTML."""
    if rating is None:
        return ''
    full_stars = int(rating)
    half_star = 1 if rating - full_stars >= 0.5 else 0
    empty_stars = 5 - full_stars - half_star
    
    stars = '★' * full_stars
    if half_star:
        stars += '½'
    stars += '☆' * empty_stars
    return stars

# Register filters with Jinja2
app.jinja_env.filters['format_datetime'] = format_datetime
app.jinja_env.filters['rating_stars'] = get_rating_stars

# Also make current datetime available in templates
@app.context_processor
def utility_processor():
    from datetime import date, datetime
    return {
        'now': date.today,  # This returns a function that gives date object
        'datetime_now': datetime.now  # Keep this if needed elsewhere
    }