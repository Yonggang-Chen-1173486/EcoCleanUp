"""User authentication and common functionality for EcoCleanUp Hub."""
from loginapp import app
from loginapp import db
from flask import redirect, render_template, request, session, url_for, flash
from flask_bcrypt import Bcrypt
import re
import os
from werkzeug.utils import secure_filename
from datetime import datetime

flask_bcrypt = Bcrypt(app)
DEFAULT_USER_ROLE = 'volunteer'

def allowed_file(filename):
    """Check if file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def user_home_url():
    """Generates a URL to the homepage for the currently logged-in user."""
    if 'loggedin' in session:
        role = session.get('role', None)

        if role == 'volunteer':
            home_endpoint = 'volunteer_home'
        elif role == 'event_leader':
            home_endpoint = 'event_leader_home'
        elif role == 'admin':
            home_endpoint = 'admin_home'
        else:
            home_endpoint = 'logout'
    else:
        home_endpoint = 'login'
    
    return url_for(home_endpoint)

@app.route('/', endpoint='root')
def root():
    """Root endpoint - redirects to appropriate home page."""
    return redirect(user_home_url())

@app.route('/login', methods=['GET', 'POST'], endpoint='login')
def login():
    """Login page endpoint."""
    if 'loggedin' in session:
        return redirect(user_home_url())

    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']

        with db.get_cursor() as cursor:
            cursor.execute('''
                SELECT user_id, username, password_hash, role, status
                FROM users
                WHERE LOWER(username) = LOWER(%s);
            ''', (username,))
            account = cursor.fetchone()
            
            if account is not None:
                if account['status'] != 'active':
                    return render_template('login.html',
                                         username=username,
                                         account_inactive=True)
                
                password_hash = account['password_hash']
                
                if flask_bcrypt.check_password_hash(password_hash, password):
                    session['loggedin'] = True
                    session['user_id'] = account['user_id']
                    session['username'] = account['username']
                    session['role'] = account['role']
                    
                    # Check for event reminders
                    check_event_reminders(account['user_id'])
                    
                    return redirect(user_home_url())
                else:
                    return render_template('login.html',
                                         username=username,
                                         password_invalid=True)
            else:
                return render_template('login.html',
                                     username=username,
                                     username_invalid=True)

    return render_template('login.html')

def check_event_reminders(user_id):
    """Check for upcoming events and set reminder flag."""
    with db.get_cursor() as cursor:
        cursor.execute('''
            SELECT e.event_name, e.event_date, e.start_time, e.location
            FROM events e
            JOIN eventregistrations er ON e.event_id = er.event_id
            WHERE er.volunteer_id = %s 
            AND e.event_date >= CURRENT_DATE
            AND e.event_date <= CURRENT_DATE + INTERVAL '7 days'
            ORDER BY e.event_date;
        ''', (user_id,))
        upcoming_events = cursor.fetchall()
        
        if upcoming_events:
            session['has_reminders'] = True
            session['upcoming_events'] = upcoming_events
        else:
            session.pop('has_reminders', None)
            session.pop('upcoming_events', None)

@app.route('/signup', methods=['GET', 'POST'], endpoint='signup')
def signup():
    """Signup (registration) page endpoint."""
    if 'loggedin' in session:
        return redirect(user_home_url())
    
    if request.method == 'POST':
        username = request.form['username']
        full_name = request.form['full_name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        contact_number = request.form['contact_number']
        home_address = request.form['home_address']
        environmental_interests = request.form.get('environmental_interests', '')

        username_error = None
        email_error = None
        password_error = None
        confirm_error = None
        fullname_error = None

        # Check if username exists
        with db.get_cursor() as cursor:
            cursor.execute('SELECT user_id FROM users WHERE LOWER(username) = LOWER(%s);', (username,))
            if cursor.fetchone() is not None:
                username_error = 'An account already exists with this username.'

        # Check if email exists
        with db.get_cursor() as cursor:
            cursor.execute('SELECT user_id FROM users WHERE LOWER(email) = LOWER(%s);', (email,))
            if cursor.fetchone() is not None:
                email_error = 'An account already exists with this email address.'

        # Validate username
        if not username_error and len(username) > 50:
            username_error = 'Your username cannot exceed 50 characters.'
        elif not username_error and not re.match(r'^[A-Za-z0-9_]+$', username):
            username_error = 'Username can only contain letters, numbers and underscores.'

        # Validate full name
        if not full_name:
            fullname_error = 'Full name is required.'
        elif len(full_name) > 100:
            fullname_error = 'Full name cannot exceed 100 characters.'

        # Validate email
        if not email_error and len(email) > 100:
            email_error = 'Email address cannot exceed 100 characters.'
        elif not email_error and not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            email_error = 'Invalid email address.'

        # Validate contact number (new validation)
        if contact_number and not re.match(r'^\+?[0-9\s\-\(\)]+$', contact_number):
            contact_error = 'Contact number can only contain digits, spaces, hyphens, parentheses, and optional + prefix.'
        elif len(contact_number) > 20:
            contact_error = 'Contact number cannot exceed 20 characters.'

        # Validate password
        if len(password) < 8:
            password_error = 'Password must be at least 8 characters long.'
        elif not re.search(r'[A-Z]', password):
            password_error = 'Password must contain at least one uppercase letter.'
        elif not re.search(r'[a-z]', password):
            password_error = 'Password must contain at least one lowercase letter.'
        elif not re.search(r'[0-9]', password):
            password_error = 'Password must contain at least one number.'
        
        # Confirm password
        if password != confirm_password:
            confirm_error = 'Passwords do not match.'

        if (username_error or email_error or password_error or 
            confirm_error or fullname_error):
            return render_template('signup.html',
                                 username=username,
                                 full_name=full_name,
                                 email=email,
                                 contact_number=contact_number,
                                 home_address=home_address,
                                 environmental_interests=environmental_interests,
                                 username_error=username_error,
                                 fullname_error=fullname_error,
                                 email_error=email_error,
                                 password_error=password_error,
                                 confirm_error=confirm_error,
                                 contact_error=contact_error)
        else:
            password_hash = flask_bcrypt.generate_password_hash(password).decode('utf-8')
            
            with db.get_cursor() as cursor:
                cursor.execute('''
                    INSERT INTO users (username, password_hash, full_name, email, 
                                      contact_number, home_address, environmental_interests, 
                                      role, status)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
                ''', (username, password_hash, full_name, email, contact_number, 
                      home_address, environmental_interests, DEFAULT_USER_ROLE, 'active'))
            
            return render_template('signup.html', signup_successful=True)

    return render_template('signup.html')

@app.route('/profile', methods=['GET', 'POST'], endpoint='profile')
def profile():
    """User Profile page endpoint."""
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        full_name = request.form['full_name']
        email = request.form['email']
        contact_number = request.form['contact_number']
        home_address = request.form['home_address']
        environmental_interests = request.form.get('environmental_interests', '')

        # Validate contact number
        contact_error = None
        if contact_number and not re.match(r'^\+?[0-9\s\-\(\)]+$', contact_number):
            contact_error = 'Contact number can only contain digits, spaces, hyphens, parentheses, and optional + prefix.'
            flash(contact_error, 'danger')
            # Still need to re-render the profile page with error
            # But we'll handle this by checking after validation

        # Handle profile image upload
        profile_image = None
        if 'profile_image' in request.files:
            file = request.files['profile_image']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(f"user_{session['user_id']}_{file.filename}")
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                profile_image = filename
            elif 'remove_image' in request.form:
                profile_image = None

        with db.get_cursor() as cursor:
            if profile_image is not None:
                cursor.execute('''
                    UPDATE users 
                    SET full_name = %s, email = %s, contact_number = %s, 
                        home_address = %s, environmental_interests = %s, profile_image = %s
                    WHERE user_id = %s;
                ''', (full_name, email, contact_number, home_address, 
                      environmental_interests, profile_image, session['user_id']))
            else:
                cursor.execute('''
                    UPDATE users 
                    SET full_name = %s, email = %s, contact_number = %s, 
                        home_address = %s, environmental_interests = %s
                    WHERE user_id = %s;
                ''', (full_name, email, contact_number, home_address, 
                      environmental_interests, session['user_id']))
            
            flash('Profile updated successfully!', 'success')

    # Retrieve user profile
    with db.get_cursor() as cursor:
        cursor.execute('''
            SELECT username, full_name, email, contact_number, home_address, 
                   environmental_interests, profile_image, role, status
            FROM users 
            WHERE user_id = %s;
        ''', (session['user_id'],))
        profile = cursor.fetchone()

    return render_template('profile.html', profile=profile)

@app.route('/change_password', methods=['GET', 'POST'], endpoint='change_password')
def change_password():
    """Change password page endpoint."""
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        error = None

        # Verify current password
        with db.get_cursor() as cursor:
            cursor.execute('SELECT password_hash FROM users WHERE user_id = %s;', 
                         (session['user_id'],))
            user = cursor.fetchone()
            
            if not flask_bcrypt.check_password_hash(user['password_hash'], current_password):
                error = 'Current password is incorrect.'
            elif new_password != confirm_password:
                error = 'New passwords do not match.'
            elif new_password == current_password:
                error = 'New password cannot be the same as current password.'
            elif len(new_password) < 8:
                error = 'Password must be at least 8 characters long.'
            elif not re.search(r'[A-Z]', new_password):
                error = 'Password must contain at least one uppercase letter.'
            elif not re.search(r'[a-z]', new_password):
                error = 'Password must contain at least one lowercase letter.'
            elif not re.search(r'[0-9]', new_password):
                error = 'Password must contain at least one number.'

            if not error:
                new_password_hash = flask_bcrypt.generate_password_hash(new_password).decode('utf-8')
                cursor.execute('''
                    UPDATE users SET password_hash = %s WHERE user_id = %s;
                ''', (new_password_hash, session['user_id']))
                flash('Password changed successfully!', 'success')
                return redirect(url_for('profile'))

        return render_template('change_password.html', error=error)

    return render_template('change_password.html')

@app.route('/dismiss_reminders', endpoint='dismiss_reminders')
def dismiss_reminders():
    """Dismiss event reminders."""
    session.pop('has_reminders', None)
    session.pop('upcoming_events', None)
    return redirect(user_home_url())

@app.route('/logout', endpoint='logout')
def logout():
    """Logout endpoint."""
    session.clear()
    return redirect(url_for('login'))