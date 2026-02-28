"""Volunteer-specific routes for EcoCleanUp Hub."""
from loginapp import app
from loginapp import db
from flask import redirect, render_template, session, url_for, request, flash
from datetime import datetime

def volunteer_required():
    """Check if user is logged in as volunteer."""
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'volunteer':
        return render_template('access_denied.html'), 403
    return None

@app.route('/volunteer/home', endpoint='volunteer_home')
def volunteer_home():
    """Volunteer Homepage."""
    check = volunteer_required()
    if check:
        return check

    # Get upcoming registered events
    with db.get_cursor() as cursor:
        cursor.execute('''
            SELECT e.event_id, e.event_name, e.location, e.event_date, 
                   e.start_time, e.end_time, e.event_type,
                   u.full_name as leader_name
            FROM events e
            JOIN eventregistrations er ON e.event_id = er.event_id
            JOIN users u ON e.event_leader_id = u.user_id
            WHERE er.volunteer_id = %s 
            AND e.event_date >= CURRENT_DATE
            AND er.attendance = 'registered'
            ORDER BY e.event_date;
        ''', (session['user_id'],))
        upcoming_events = cursor.fetchall()

        # Get past events for participation history preview
        cursor.execute('''
            SELECT e.event_id, e.event_name, e.location, e.event_date,
                   er.attendance,
                   CASE WHEN f.feedback_id IS NOT NULL THEN TRUE ELSE FALSE END as feedback_submitted
            FROM events e
            JOIN eventregistrations er ON e.event_id = er.event_id
            LEFT JOIN feedback f ON e.event_id = f.event_id AND f.volunteer_id = %s
            WHERE er.volunteer_id = %s 
            AND e.event_date < CURRENT_DATE
            ORDER BY e.event_date DESC
            LIMIT 5;
        ''', (session['user_id'], session['user_id']))
        past_events = cursor.fetchall()

    return render_template('volunteer/home.html', 
                         upcoming_events=upcoming_events,
                         past_events=past_events)

@app.route('/volunteer/browse_events', endpoint='browse_events')
def browse_events():
    """Browse all upcoming events with filters."""
    check = volunteer_required()
    if check:
        return check

    # Get filter parameters
    date_filter = request.args.get('date', '')
    location_filter = request.args.get('location', '')
    type_filter = request.args.get('type', '')

    query = '''
        SELECT e.event_id, e.event_name, e.location, e.event_type,
               e.event_date, e.start_time, e.end_time, e.duration,
               e.description, e.supplies, e.safety_instructions,
               u.full_name as leader_name,
               CASE WHEN er.registration_id IS NOT NULL THEN TRUE ELSE FALSE END as registered
        FROM events e
        JOIN users u ON e.event_leader_id = u.user_id
        LEFT JOIN eventregistrations er ON e.event_id = er.event_id 
            AND er.volunteer_id = %s
        WHERE e.event_date >= CURRENT_DATE
    '''
    params = [session['user_id']]

    if date_filter:
        query += " AND e.event_date = %s"
        params.append(date_filter)
    
    if location_filter:
        query += " AND e.location ILIKE %s"
        params.append(f'%{location_filter}%')
    
    if type_filter:
        query += " AND e.event_type ILIKE %s"
        params.append(f'%{type_filter}%')

    query += " ORDER BY e.event_date;"

    with db.get_cursor() as cursor:
        cursor.execute(query, tuple(params))
        events = cursor.fetchall()

        # Get unique event types for filter dropdown
        cursor.execute('SELECT DISTINCT event_type FROM events WHERE event_type IS NOT NULL;')
        event_types = cursor.fetchall()

    return render_template('volunteer/browse_events.html', 
                         events=events, 
                         event_types=event_types,
                         date_filter=date_filter,
                         location_filter=location_filter,
                         type_filter=type_filter)

@app.route('/volunteer/register/<int:event_id>', methods=['POST'], endpoint='register_for_event')
def register_for_event(event_id):
    """Register volunteer for an event."""
    check = volunteer_required()
    if check:
        return check

    # Check for scheduling conflicts
    with db.get_cursor() as cursor:
        cursor.execute('''
            SELECT e.event_date, e.start_time, e.end_time
            FROM events e
            WHERE e.event_id = %s;
        ''', (event_id,))
        new_event = cursor.fetchone()

        if not new_event:
            flash('Event not found.', 'danger')
            return redirect(url_for('browse_events'))

        # Check if already registered
        cursor.execute('''
            SELECT registration_id FROM eventregistrations 
            WHERE event_id = %s AND volunteer_id = %s;
        ''', (event_id, session['user_id']))
        if cursor.fetchone():
            flash('You are already registered for this event.', 'warning')
            return redirect(url_for('browse_events'))

        # Check for conflicts with other registered events
        cursor.execute('''
            SELECT e.event_name, e.event_date, e.start_time, e.end_time
            FROM events e
            JOIN eventregistrations er ON e.event_id = er.event_id
            WHERE er.volunteer_id = %s 
            AND e.event_date = %s
            AND (
                (e.start_time <= %s AND e.end_time > %s) OR
                (e.start_time < %s AND e.end_time >= %s) OR
                (e.start_time >= %s AND e.start_time < %s)
            );
        ''', (session['user_id'], new_event['event_date'], 
              new_event['end_time'], new_event['start_time'],
              new_event['end_time'], new_event['start_time'],
              new_event['start_time'], new_event['end_time']))
        
        conflict = cursor.fetchone()
        if conflict:
            flash(f'Conflict: You are already registered for "{conflict["event_name"]}" at the same time.', 'danger')
            return redirect(url_for('browse_events'))

        # Register for event
        cursor.execute('''
            INSERT INTO eventregistrations (event_id, volunteer_id, attendance, registered_at)
            VALUES (%s, %s, 'registered', CURRENT_TIMESTAMP);
        ''', (event_id, session['user_id']))
        
        flash('Successfully registered for event!', 'success')

    return redirect(url_for('browse_events'))

@app.route('/volunteer/my_events', endpoint='my_events')
def my_events():
    """View volunteer's registered events."""
    check = volunteer_required()
    if check:
        return check

    with db.get_cursor() as cursor:
        # Upcoming events
        cursor.execute('''
            SELECT e.event_id, e.event_name, e.location, e.event_type,
                   e.event_date, e.start_time, e.end_time, e.duration,
                   e.description, e.supplies, e.safety_instructions,
                   u.full_name as leader_name
            FROM events e
            JOIN eventregistrations er ON e.event_id = er.event_id
            JOIN users u ON e.event_leader_id = u.user_id
            WHERE er.volunteer_id = %s 
            AND e.event_date >= CURRENT_DATE
            AND er.attendance = 'registered'
            ORDER BY e.event_date;
        ''', (session['user_id'],))
        upcoming_events = cursor.fetchall()

    return render_template('volunteer/my_events.html', upcoming_events=upcoming_events)

@app.route('/volunteer/participation_history', endpoint='volunteer_history')
def volunteer_history():
    """View volunteer's own participation history."""
    check = volunteer_required()
    if check:
        return check

    with db.get_cursor() as cursor:
        cursor.execute('''
            SELECT e.event_id, e.event_name, e.location, e.event_type,
                   e.event_date, e.start_time, e.end_time,
                   er.attendance,
                   eo.num_attendees, eo.bags_collected, eo.recyclables_sorted,
                   f.rating, f.comments, f.submitted_at as feedback_date
            FROM events e
            JOIN eventregistrations er ON e.event_id = er.event_id
            LEFT JOIN eventoutcomes eo ON e.event_id = eo.event_id
            LEFT JOIN feedback f ON e.event_id = f.event_id AND f.volunteer_id = %s
            WHERE er.volunteer_id = %s 
            AND e.event_date < CURRENT_DATE
            ORDER BY e.event_date DESC;
        ''', (session['user_id'], session['user_id']))
        past_events = cursor.fetchall()

    return render_template('volunteer/participation_history.html', past_events=past_events)

@app.route('/volunteer/feedback/<int:event_id>', methods=['GET', 'POST'], endpoint='submit_feedback')
def submit_feedback(event_id):
    """Submit feedback for a past event."""
    check = volunteer_required()
    if check:
        return check

    if request.method == 'POST':
        rating = request.form['rating']
        comments = request.form['comments']

        with db.get_cursor() as cursor:
            # Check if volunteer attended the event
            cursor.execute('''
                SELECT attendance FROM eventregistrations
                WHERE event_id = %s AND volunteer_id = %s;
            ''', (event_id, session['user_id']))
            reg = cursor.fetchone()

            if not reg or reg['attendance'] != 'attended':
                flash('You can only provide feedback for events you attended.', 'danger')
                return redirect(url_for('volunteer_history'))

            # Check if feedback already submitted
            cursor.execute('''
                SELECT feedback_id FROM feedback
                WHERE event_id = %s AND volunteer_id = %s;
            ''', (event_id, session['user_id']))
            if cursor.fetchone():
                flash('You have already submitted feedback for this event.', 'warning')
                return redirect(url_for('volunteer_history'))

            # Submit feedback
            cursor.execute('''
                INSERT INTO feedback (event_id, volunteer_id, rating, comments, submitted_at)
                VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP);
            ''', (event_id, session['user_id'], rating, comments))
            
            flash('Thank you for your feedback!', 'success')

        return redirect(url_for('volunteer_history'))

    # GET request - show feedback form
    with db.get_cursor() as cursor:
        cursor.execute('''
            SELECT e.event_name, e.event_date
            FROM events e
            JOIN eventregistrations er ON e.event_id = er.event_id
            WHERE e.event_id = %s AND er.volunteer_id = %s AND er.attendance = 'attended';
        ''', (event_id, session['user_id']))
        event = cursor.fetchone()

        if not event:
            flash('Event not found or you did not attend.', 'danger')
            return redirect(url_for('volunteer_history'))

    return render_template('volunteer/feedback.html', event=event, event_id=event_id)