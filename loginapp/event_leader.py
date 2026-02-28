"""Event Leader-specific routes for EcoCleanUp Hub."""
from loginapp import app
from loginapp import db
from flask import redirect, render_template, session, url_for, request, flash
from datetime import datetime

def event_leader_required():
    """Check if user is logged in as event leader."""
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'event_leader':
        return render_template('access_denied.html'), 403
    return None

@app.route('/event_leader/home', endpoint='event_leader_home')
def event_leader_home():
    """Event Leader Homepage."""
    check = event_leader_required()
    if check:
        return check

    with db.get_cursor() as cursor:
        # Get upcoming events created by this leader
        cursor.execute('''
            SELECT event_id, event_name, location, event_date, start_time, end_time,
                   (SELECT COUNT(*) FROM eventregistrations WHERE event_id = e.event_id) as volunteer_count
            FROM events e
            WHERE event_leader_id = %s AND event_date >= CURRENT_DATE
            ORDER BY event_date;
        ''', (session['user_id'],))
        upcoming_events = cursor.fetchall()

        # Get past events for summary
        cursor.execute('''
            SELECT COUNT(*) as total_events,
                   COALESCE(SUM(eo.num_attendees), 0) as total_volunteers,
                   COALESCE(SUM(eo.bags_collected), 0) as total_bags,
                   COALESCE(SUM(eo.recyclables_sorted), 0) as total_recyclables
            FROM events e
            LEFT JOIN eventoutcomes eo ON e.event_id = eo.event_id
            WHERE e.event_leader_id = %s AND e.event_date < CURRENT_DATE;
        ''', (session['user_id'],))
        stats = cursor.fetchone()

    return render_template('event_leader/home.html', 
                         upcoming_events=upcoming_events,
                         stats=stats)

@app.route('/event_leader/manage_events', endpoint='manage_events')
def manage_events():
    """Manage events created by this leader."""
    check = event_leader_required()
    if check:
        return check

    with db.get_cursor() as cursor:
        cursor.execute('''
            SELECT e.event_id, e.event_name, e.location, e.event_type,
                   e.event_date, e.start_time, e.end_time, e.duration,
                   e.description, e.supplies, e.safety_instructions,
                   (SELECT COUNT(*) FROM eventregistrations WHERE event_id = e.event_id) as registered_count,
                   CASE WHEN eo.outcome_id IS NOT NULL THEN TRUE ELSE FALSE END as outcomes_recorded
            FROM events e
            LEFT JOIN eventoutcomes eo ON e.event_id = eo.event_id
            WHERE e.event_leader_id = %s
            ORDER BY e.event_date DESC;
        ''', (session['user_id'],))
        events = cursor.fetchall()

    return render_template('event_leader/manage_events.html', events=events)

@app.route('/event_leader/create_event', methods=['GET', 'POST'], endpoint='create_event')
def create_event():
    """Create a new cleanup event."""
    check = event_leader_required()
    if check:
        return check

    if request.method == 'POST':
        event_name = request.form['event_name']
        location = request.form['location']
        event_type = request.form['event_type']
        event_date = request.form['event_date']
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        duration = request.form['duration']
        description = request.form['description']
        supplies = request.form['supplies']
        safety_instructions = request.form['safety_instructions']

        # Validate date is in future
        if datetime.strptime(event_date, '%Y-%m-%d').date() < datetime.now().date():
            flash('Event date must be in the future.', 'danger')
            return render_template('event_leader/create_event.html')

        with db.get_cursor() as cursor:
            cursor.execute('''
                INSERT INTO events (event_name, event_leader_id, location, event_type,
                                   event_date, start_time, end_time, duration,
                                   description, supplies, safety_instructions)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            ''', (event_name, session['user_id'], location, event_type,
                  event_date, start_time, end_time, duration,
                  description, supplies, safety_instructions))
            
            flash('Event created successfully!', 'success')
            return redirect(url_for('manage_events'))

    return render_template('event_leader/create_event.html')

@app.route('/event_leader/edit_event/<int:event_id>', methods=['GET', 'POST'], endpoint='edit_event')
def edit_event(event_id):
    """Edit an existing event."""
    check = event_leader_required()
    if check:
        return check

    if request.method == 'POST':
        event_name = request.form['event_name']
        location = request.form['location']
        event_type = request.form['event_type']
        event_date = request.form['event_date']
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        duration = request.form['duration']
        description = request.form['description']
        supplies = request.form['supplies']
        safety_instructions = request.form['safety_instructions']

        with db.get_cursor() as cursor:
            cursor.execute('''
                UPDATE events
                SET event_name = %s, location = %s, event_type = %s,
                    event_date = %s, start_time = %s, end_time = %s,
                    duration = %s, description = %s, supplies = %s,
                    safety_instructions = %s
                WHERE event_id = %s AND event_leader_id = %s;
            ''', (event_name, location, event_type, event_date, start_time,
                  end_time, duration, description, supplies, safety_instructions,
                  event_id, session['user_id']))
            
            flash('Event updated successfully!', 'success')
            return redirect(url_for('manage_events'))

    # GET request - show edit form
    with db.get_cursor() as cursor:
        cursor.execute('''
            SELECT * FROM events
            WHERE event_id = %s AND event_leader_id = %s;
        ''', (event_id, session['user_id']))
        event = cursor.fetchone()

        if not event:
            flash('Event not found.', 'danger')
            return redirect(url_for('manage_events'))

    return render_template('event_leader/edit_event.html', event=event)

@app.route('/event_leader/cancel_event/<int:event_id>', methods=['POST'], endpoint='cancel_event')
def cancel_event(event_id):
    """Cancel an event."""
    check = event_leader_required()
    if check:
        return check

    with db.get_cursor() as cursor:
        # Check if event has passed
        cursor.execute('SELECT event_date FROM events WHERE event_id = %s;', (event_id,))
        event = cursor.fetchone()
        
        if event and event['event_date'] < datetime.now().date():
            flash('Cannot cancel past events.', 'danger')
        else:
            cursor.execute('''
                DELETE FROM eventregistrations WHERE event_id = %s;
                DELETE FROM events WHERE event_id = %s AND event_leader_id = %s;
            ''', (event_id, event_id, session['user_id']))
            flash('Event cancelled successfully.', 'success')

    return redirect(url_for('manage_events'))

@app.route('/event_leader/event_details/<int:event_id>', endpoint='event_details')
def event_details(event_id):
    """View details of a specific event."""
    check = event_leader_required()
    if check:
        return check

    with db.get_cursor() as cursor:
        cursor.execute('''
            SELECT e.*, u.full_name as leader_name,
                   (SELECT COUNT(*) FROM eventregistrations WHERE event_id = e.event_id) as registered_count,
                   (SELECT COUNT(*) FROM eventregistrations WHERE event_id = e.event_id AND attendance = 'attended') as attended_count
            FROM events e
            JOIN users u ON e.event_leader_id = u.user_id
            WHERE e.event_id = %s AND e.event_leader_id = %s;
        ''', (event_id, session['user_id']))
        event = cursor.fetchone()

        if not event:
            flash('Event not found.', 'danger')
            return redirect(url_for('manage_events'))

        # Get registered volunteers
        cursor.execute('''
            SELECT u.user_id, u.full_name, u.email, u.contact_number,
                   er.attendance, er.registered_at
            FROM users u
            JOIN eventregistrations er ON u.user_id = er.volunteer_id
            WHERE er.event_id = %s
            ORDER BY u.full_name;
        ''', (event_id,))
        volunteers = cursor.fetchall()

        # Get event outcomes if any
        cursor.execute('SELECT * FROM eventoutcomes WHERE event_id = %s;', (event_id,))
        outcomes = cursor.fetchone()

        # Get feedback for past event
        if event['event_date'] < datetime.now().date():
            cursor.execute('''
                SELECT f.*, u.full_name as volunteer_name
                FROM feedback f
                JOIN users u ON f.volunteer_id = u.user_id
                WHERE f.event_id = %s
                ORDER BY f.submitted_at DESC;
            ''', (event_id,))
            feedback_list = cursor.fetchall()
        else:
            feedback_list = []

    return render_template('event_leader/event_details.html',
                         event=event, volunteers=volunteers,
                         outcomes=outcomes, feedback_list=feedback_list)

@app.route('/event_leader/remove_volunteer/<int:event_id>/<int:volunteer_id>', methods=['POST'], endpoint='remove_volunteer')
def remove_volunteer(event_id, volunteer_id):
    """Remove a volunteer from an event."""
    check = event_leader_required()
    if check:
        return check

    with db.get_cursor() as cursor:
        cursor.execute('''
            DELETE FROM eventregistrations
            WHERE event_id = %s AND volunteer_id = %s
            AND EXISTS (SELECT 1 FROM events WHERE event_id = %s AND event_leader_id = %s);
        ''', (event_id, volunteer_id, event_id, session['user_id']))
        
        flash('Volunteer removed from event.', 'success')

    return redirect(url_for('event_details', event_id=event_id))

@app.route('/event_leader/track_attendance/<int:event_id>', methods=['GET', 'POST'], endpoint='track_attendance')
def track_attendance(event_id):
    """Track volunteer attendance for an event."""
    check = event_leader_required()
    if check:
        return check

    if request.method == 'POST':
        attendance_data = request.form.getlist('attendance')
        
        with db.get_cursor() as cursor:
            for item in attendance_data:
                volunteer_id, status = item.split(':')
                cursor.execute('''
                    UPDATE eventregistrations
                    SET attendance = %s
                    WHERE event_id = %s AND volunteer_id = %s;
                ''', (status, event_id, volunteer_id))
            
            flash('Attendance recorded successfully!', 'success')
            return redirect(url_for('event_details', event_id=event_id))

    # GET request - show attendance tracking form
    with db.get_cursor() as cursor:
        cursor.execute('''
            SELECT e.* FROM events e
            WHERE e.event_id = %s AND e.event_leader_id = %s;
        ''', (event_id, session['user_id']))
        event = cursor.fetchone()

        if not event:
            flash('Event not found.', 'danger')
            return redirect(url_for('manage_events'))

        cursor.execute('''
            SELECT u.user_id, u.full_name, u.email, er.attendance
            FROM users u
            JOIN eventregistrations er ON u.user_id = er.volunteer_id
            WHERE er.event_id = %s
            ORDER BY u.full_name;
        ''', (event_id,))
        volunteers = cursor.fetchall()

    return render_template('event_leader/track_attendance.html',
                         event=event, volunteers=volunteers)

@app.route('/event_leader/record_outcomes/<int:event_id>', methods=['GET', 'POST'], endpoint='record_outcomes')
def record_outcomes(event_id):
    """Record outcomes for a past event."""
    check = event_leader_required()
    if check:
        return check

    if request.method == 'POST':
        num_attendees = request.form['num_attendees']
        bags_collected = request.form['bags_collected']
        recyclables_sorted = request.form['recyclables_sorted']
        other_achievements = request.form['other_achievements']

        with db.get_cursor() as cursor:
            # Check if outcomes already exist
            cursor.execute('SELECT outcome_id FROM eventoutcomes WHERE event_id = %s;', (event_id,))
            if cursor.fetchone():
                cursor.execute('''
                    UPDATE eventoutcomes
                    SET num_attendees = %s, bags_collected = %s,
                        recyclables_sorted = %s, other_achievements = %s,
                        recorded_at = CURRENT_TIMESTAMP
                    WHERE event_id = %s;
                ''', (num_attendees, bags_collected, recyclables_sorted,
                      other_achievements, event_id))
            else:
                cursor.execute('''
                    INSERT INTO eventoutcomes (event_id, num_attendees, bags_collected,
                                              recyclables_sorted, other_achievements, recorded_by)
                    VALUES (%s, %s, %s, %s, %s, %s);
                ''', (event_id, num_attendees, bags_collected,
                      recyclables_sorted, other_achievements, session['user_id']))
            
            flash('Event outcomes recorded successfully!', 'success')
            return redirect(url_for('event_details', event_id=event_id))

    # GET request - show outcomes form
    with db.get_cursor() as cursor:
        cursor.execute('''
            SELECT e.*, eo.*
            FROM events e
            LEFT JOIN eventoutcomes eo ON e.event_id = eo.event_id
            WHERE e.event_id = %s AND e.event_leader_id = %s;
        ''', (event_id, session['user_id']))
        event = cursor.fetchone()

        if not event:
            flash('Event not found.', 'danger')
            return redirect(url_for('manage_events'))

        # Get number of volunteers who attended
        cursor.execute('''
            SELECT COUNT(*) as attended_count
            FROM eventregistrations
            WHERE event_id = %s AND attendance = 'attended';
        ''', (event_id,))
        attended = cursor.fetchone()
        event['attended_count'] = attended['attended_count']

    return render_template('event_leader/record_outcomes.html', event=event)

@app.route('/event_leader/participation_history', endpoint='leader_history')
def leader_history():
    """View participation history for volunteers in all managed events."""
    check = event_leader_required()
    if check:
        return check

    volunteer_id = request.args.get('volunteer_id', '')

    with db.get_cursor() as cursor:
        if volunteer_id:
            # View specific volunteer's history in leader's events
            cursor.execute('''
                SELECT u.user_id, u.full_name, u.email,
                       e.event_id, e.event_name, e.event_date,
                       er.attendance,
                       eo.bags_collected, eo.recyclables_sorted
                FROM users u
                JOIN eventregistrations er ON u.user_id = er.volunteer_id
                JOIN events e ON er.event_id = e.event_id
                LEFT JOIN eventoutcomes eo ON e.event_id = eo.event_id
                WHERE e.event_leader_id = %s
                AND u.user_id = %s
                AND e.event_date < CURRENT_DATE
                ORDER BY e.event_date DESC;
            ''', (session['user_id'], volunteer_id))
            history = cursor.fetchall()

            cursor.execute('''
                SELECT full_name FROM users WHERE user_id = %s;
            ''', (volunteer_id,))
            volunteer = cursor.fetchone()
        else:
            # Get list of volunteers who have participated in leader's events
            cursor.execute('''
                SELECT DISTINCT u.user_id, u.full_name, u.email,
                       (SELECT COUNT(*) FROM eventregistrations er2 
                        JOIN events e2 ON er2.event_id = e2.event_id
                        WHERE er2.volunteer_id = u.user_id 
                        AND e2.event_leader_id = %s) as events_attended
                FROM users u
                JOIN eventregistrations er ON u.user_id = er.volunteer_id
                JOIN events e ON er.event_id = e.event_id
                WHERE e.event_leader_id = %s
                AND e.event_date < CURRENT_DATE
                GROUP BY u.user_id, u.full_name, u.email
                ORDER BY u.full_name;
            ''', (session['user_id'], session['user_id']))
            volunteers = cursor.fetchall()
            history = None
            volunteer = None

    return render_template('event_leader/participation_history.html',
                         volunteers=volunteers if not volunteer_id else None,
                         history=history,
                         selected_volunteer=volunteer)

@app.route('/event_leader/send_reminder/<int:event_id>', methods=['POST'], endpoint='send_reminder')
def send_reminder(event_id):
    """Send reminder to volunteers for an upcoming event."""
    check = event_leader_required()
    if check:
        return check

    with db.get_cursor() as cursor:
        # Get event details
        cursor.execute('''
            SELECT event_name, event_date FROM events
            WHERE event_id = %s AND event_leader_id = %s;
        ''', (event_id, session['user_id']))
        event = cursor.fetchone()

        if event:
            session[f'reminder_sent_{event_id}'] = True
            flash(f'Reminder sent to all volunteers for {event["event_name"]}!', 'success')

    return redirect(url_for('event_details', event_id=event_id))

@app.route('/event_leader/review_feedback/<int:event_id>', endpoint='review_feedback')
def review_feedback(event_id):
    """Review feedback for a specific event."""
    check = event_leader_required()
    if check:
        return check

    with db.get_cursor() as cursor:
        cursor.execute('''
            SELECT f.*, u.full_name as volunteer_name
            FROM feedback f
            JOIN users u ON f.volunteer_id = u.user_id
            JOIN events e ON f.event_id = e.event_id
            WHERE f.event_id = %s AND e.event_leader_id = %s
            ORDER BY f.submitted_at DESC;
        ''', (event_id, session['user_id']))
        feedback_list = cursor.fetchall()

        cursor.execute('''
            SELECT event_name, event_date FROM events
            WHERE event_id = %s;
        ''', (event_id,))
        event = cursor.fetchone()

    return render_template('event_leader/review_feedback.html',
                         feedback_list=feedback_list, event=event)

@app.route('/event_leader/event_report/<int:event_id>', endpoint='event_report')
def event_report(event_id):
    """Generate report for a specific event."""
    check = event_leader_required()
    if check:
        return check

    with db.get_cursor() as cursor:
        cursor.execute('''
            SELECT e.*, u.full_name as leader_name,
                   eo.*,
                   (SELECT COUNT(*) FROM eventregistrations WHERE event_id = e.event_id) as total_registered,
                   (SELECT COUNT(*) FROM eventregistrations WHERE event_id = e.event_id AND attendance = 'attended') as total_attended,
                   (SELECT AVG(rating)::numeric(10,2) FROM feedback WHERE event_id = e.event_id) as avg_rating,
                   (SELECT COUNT(*) FROM feedback WHERE event_id = e.event_id) as feedback_count
            FROM events e
            JOIN users u ON e.event_leader_id = u.user_id
            LEFT JOIN eventoutcomes eo ON e.event_id = eo.event_id
            WHERE e.event_id = %s AND e.event_leader_id = %s;
        ''', (event_id, session['user_id']))
        report = cursor.fetchone()

        if not report:
            flash('Event not found.', 'danger')
            return redirect(url_for('manage_events'))

        # Get volunteer list for this event
        cursor.execute('''
            SELECT u.full_name, u.email, er.attendance
            FROM users u
            JOIN eventregistrations er ON u.user_id = er.volunteer_id
            WHERE er.event_id = %s
            ORDER BY u.full_name;
        ''', (event_id,))
        volunteers = cursor.fetchall()

    return render_template('event_leader/event_report.html',
                         report=report, volunteers=volunteers)

@app.route('/event_leader/browse_events', endpoint='leader_browse_events')
def leader_browse_events():
    """Event Leader browse all upcoming events."""
    check = event_leader_required()
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
               (SELECT COUNT(*) FROM eventregistrations WHERE event_id = e.event_id) as registered_count
        FROM events e
        JOIN users u ON e.event_leader_id = u.user_id
        WHERE e.event_date >= CURRENT_DATE
    '''
    params = []

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

    return render_template('event_leader/browse_events.html', 
                         events=events, 
                         event_types=event_types,
                         date_filter=date_filter,
                         location_filter=location_filter,
                         type_filter=type_filter)