"""Admin-specific routes for EcoCleanUp Hub."""
from loginapp import app
from loginapp import db
from flask import redirect, render_template, session, url_for, request, flash
from datetime import datetime

def admin_required():
    """Check if user is logged in as admin."""
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'admin':
        return render_template('access_denied.html'), 403
    return None

@app.route('/admin/home')
def admin_home():
    """Admin Homepage."""
    check = admin_required()
    if check:
        return check

    # Get platform statistics
    with db.get_cursor() as cursor:
        cursor.execute('''
            SELECT 
                (SELECT COUNT(*) FROM users WHERE role = 'volunteer') as total_volunteers,
                (SELECT COUNT(*) FROM users WHERE role = 'event_leader') as total_leaders,
                (SELECT COUNT(*) FROM users WHERE role = 'admin') as total_admins,
                (SELECT COUNT(*) FROM events) as total_events,
                (SELECT COUNT(*) FROM events WHERE event_date >= CURRENT_DATE) as upcoming_events,
                (SELECT COUNT(*) FROM events WHERE event_date < CURRENT_DATE) as past_events,
                (SELECT COUNT(*) FROM feedback) as total_feedback,
                (SELECT AVG(rating)::numeric(10,2) FROM feedback) as avg_rating,
                (SELECT COUNT(*) FROM eventregistrations) as total_registrations,
                (SELECT SUM(bags_collected) FROM eventoutcomes) as total_bags,
                (SELECT SUM(recyclables_sorted) FROM eventoutcomes) as total_recyclables;
        ''')
        stats = cursor.fetchone()

        # Recent events
        cursor.execute('''
            SELECT e.event_id, e.event_name, e.event_date, u.full_name as leader_name,
                   (SELECT COUNT(*) FROM eventregistrations WHERE event_id = e.event_id) as registered
            FROM events e
            JOIN users u ON e.event_leader_id = u.user_id
            ORDER BY e.created_at DESC
            LIMIT 5;
        ''')
        recent_events = cursor.fetchall()

    return render_template('admin/home.html', stats=stats, recent_events=recent_events)

@app.route('/admin/manage_users')
def manage_users():
    """Manage all users."""
    check = admin_required()
    if check:
        return check

    search = request.args.get('search', '')
    role_filter = request.args.get('role', '')
    status_filter = request.args.get('status', '')

    query = '''
        SELECT user_id, username, full_name, email, role, status, created_at
        FROM users
        WHERE 1=1
    '''
    params = []

    if search:
        query += " AND (full_name ILIKE %s OR username ILIKE %s OR email ILIKE %s)"
        params.extend([f'%{search}%', f'%{search}%', f'%{search}%'])
    
    if role_filter:
        query += " AND role = %s"
        params.append(role_filter)
    
    if status_filter:
        query += " AND status = %s"
        params.append(status_filter)

    query += " ORDER BY full_name;"

    with db.get_cursor() as cursor:
        cursor.execute(query, tuple(params))
        users = cursor.fetchall()

    return render_template('admin/manage_users.html', users=users,
                         search=search, role_filter=role_filter, status_filter=status_filter)

@app.route('/admin/view_user/<int:user_id>')
def view_user(user_id):
    """View user profile."""
    check = admin_required()
    if check:
        return check

    with db.get_cursor() as cursor:
        cursor.execute('''
            SELECT user_id, username, full_name, email, contact_number,
                   home_address, environmental_interests, profile_image,
                   role, status, created_at
            FROM users
            WHERE user_id = %s;
        ''', (user_id,))
        user = cursor.fetchone()

        if not user:
            flash('User not found.', 'danger')
            return redirect(url_for('manage_users'))

        # Get user's event registrations
        cursor.execute('''
            SELECT e.event_id, e.event_name, e.event_date, er.attendance
            FROM events e
            JOIN eventregistrations er ON e.event_id = er.event_id
            WHERE er.volunteer_id = %s
            ORDER BY e.event_date DESC;
        ''', (user_id,))
        events = cursor.fetchall()

        # If event leader, get their events
        if user['role'] == 'event_leader':
            cursor.execute('''
                SELECT event_id, event_name, event_date,
                       (SELECT COUNT(*) FROM eventregistrations WHERE event_id = e.event_id) as registered
                FROM events e
                WHERE event_leader_id = %s
                ORDER BY event_date DESC;
            ''', (user_id,))
            created_events = cursor.fetchall()
        else:
            created_events = []

    return render_template('admin/user_profile_view.html',
                         user=user, events=events, created_events=created_events)

@app.route('/admin/change_user_status/<int:user_id>', methods=['POST'])
def change_user_status(user_id):
    """Change user status (active/inactive)."""
    check = admin_required()
    if check:
        return check

    new_status = request.form['status']

    with db.get_cursor() as cursor:
        cursor.execute('''
            UPDATE users SET status = %s WHERE user_id = %s;
        ''', (new_status, user_id))
        
        flash(f'User status updated to {new_status}.', 'success')

    return redirect(url_for('view_user', user_id=user_id))

@app.route('/admin/reports')
def platform_reports():
    """View platform-wide reports."""
    check = admin_required()
    if check:
        return check

    with db.get_cursor() as cursor:
        # Summary statistics
        cursor.execute('''
            SELECT 
                (SELECT COUNT(*) FROM users WHERE role = 'volunteer' AND status = 'active') as active_volunteers,
                (SELECT COUNT(*) FROM users WHERE role = 'event_leader' AND status = 'active') as active_leaders,
                (SELECT COUNT(*) FROM users WHERE role = 'admin' AND status = 'active') as active_admins,
                (SELECT COUNT(*) FROM events WHERE event_date >= CURRENT_DATE) as upcoming_events,
                (SELECT COUNT(*) FROM events WHERE event_date < CURRENT_DATE) as completed_events,
                (SELECT COUNT(*) FROM feedback) as total_feedback,
                (SELECT AVG(rating)::numeric(10,2) FROM feedback) as avg_rating,
                (SELECT SUM(bags_collected) FROM eventoutcomes) as total_bags,
                (SELECT SUM(recyclables_sorted) FROM eventoutcomes) as total_recyclables;
        ''')
        summary = cursor.fetchone()

        # Events by month
        cursor.execute('''
            SELECT TO_CHAR(event_date, 'YYYY-MM') as month,
                   COUNT(*) as event_count,
                   SUM(CASE WHEN event_date < CURRENT_DATE THEN 1 ELSE 0 END) as completed,
                   SUM(CASE WHEN event_date >= CURRENT_DATE THEN 1 ELSE 0 END) as upcoming
            FROM events
            GROUP BY TO_CHAR(event_date, 'YYYY-MM')
            ORDER BY month DESC
            LIMIT 12;
        ''')
        events_by_month = cursor.fetchall()

        # Top event leaders
        cursor.execute('''
            SELECT u.user_id, u.full_name,
                   COUNT(DISTINCT e.event_id) as events_created,
                   COUNT(DISTINCT er.volunteer_id) as unique_volunteers,
                   COALESCE(SUM(eo.bags_collected), 0) as total_bags
            FROM users u
            LEFT JOIN events e ON u.user_id = e.event_leader_id
            LEFT JOIN eventregistrations er ON e.event_id = er.event_id
            LEFT JOIN eventoutcomes eo ON e.event_id = eo.event_id
            WHERE u.role = 'event_leader'
            GROUP BY u.user_id, u.full_name
            ORDER BY events_created DESC
            LIMIT 5;
        ''')
        top_leaders = cursor.fetchall()

        # Event type distribution
        cursor.execute('''
            SELECT event_type, COUNT(*) as count
            FROM events
            WHERE event_type IS NOT NULL
            GROUP BY event_type
            ORDER BY count DESC;
        ''')
        event_types = cursor.fetchall()

    return render_template('admin/reports.html',
                         summary=summary,
                         events_by_month=events_by_month,
                         top_leaders=top_leaders,
                         event_types=event_types)

@app.route('/admin/event_reports', endpoint='event_reports')
def event_reports():
    """View reports for all events."""
    check = admin_required()
    if check:
        return check

    # Filter parameters
    from_date = request.args.get('from_date', '')
    to_date = request.args.get('to_date', '')
    leader_id = request.args.get('leader_id', '')

    query = '''
        SELECT e.event_id, e.event_name, e.event_date, u.full_name as leader_name,
               (SELECT COUNT(*) FROM eventregistrations WHERE event_id = e.event_id) as registered,
               (SELECT COUNT(*) FROM eventregistrations WHERE event_id = e.event_id AND attendance = 'attended') as attended,
               COALESCE(eo.bags_collected, 0) as bags_collected,
               COALESCE(eo.recyclables_sorted, 0) as recyclables_sorted,
               (SELECT AVG(rating)::numeric(10,2) FROM feedback WHERE event_id = e.event_id) as avg_rating,
               (SELECT COUNT(*) FROM feedback WHERE event_id = e.event_id) as feedback_count
        FROM events e
        JOIN users u ON e.event_leader_id = u.user_id
        LEFT JOIN eventoutcomes eo ON e.event_id = eo.event_id
        WHERE 1=1
    '''
    params = []

    if from_date:
        query += " AND e.event_date >= %s"
        params.append(from_date)
    
    if to_date:
        query += " AND e.event_date <= %s"
        params.append(to_date)
    
    if leader_id:
        query += " AND e.event_leader_id = %s"
        params.append(leader_id)

    query += " ORDER BY e.event_date DESC;"

    with db.get_cursor() as cursor:
        cursor.execute(query, tuple(params))
        events = cursor.fetchall()

        # Get list of event leaders for filter
        cursor.execute('''
            SELECT user_id, full_name FROM users
            WHERE role = 'event_leader' AND status = 'active'
            ORDER BY full_name;
        ''')
        leaders = cursor.fetchall()

    return render_template('admin/event_reports.html',
                         events=events, leaders=leaders,
                         from_date=from_date, to_date=to_date,
                         selected_leader=leader_id)

@app.route('/admin/manage_events', endpoint='admin_manage_events')
def admin_manage_events():
    """Admin view all events with edit/cancel options."""
    check = admin_required()
    if check:
        return check

    # Filter parameters
    search = request.args.get('search', '')
    status_filter = request.args.get('status', '')  # upcoming/past
    leader_filter = request.args.get('leader_id', '')

    query = '''
        SELECT e.event_id, e.event_name, e.location, e.event_type,
               e.event_date, e.start_time, e.end_time,
               u.full_name as leader_name, u.user_id as leader_id,
               (SELECT COUNT(*) FROM eventregistrations WHERE event_id = e.event_id) as registered_count,
               CASE WHEN e.event_date >= CURRENT_DATE THEN 'upcoming' ELSE 'past' END as status
        FROM events e
        JOIN users u ON e.event_leader_id = u.user_id
        WHERE 1=1
    '''
    params = []

    if search:
        query += " AND (e.event_name ILIKE %s OR e.location ILIKE %s OR u.full_name ILIKE %s)"
        params.extend([f'%{search}%', f'%{search}%', f'%{search}%'])
    
    if status_filter == 'upcoming':
        query += " AND e.event_date >= CURRENT_DATE"
    elif status_filter == 'past':
        query += " AND e.event_date < CURRENT_DATE"
    
    if leader_filter:
        query += " AND e.event_leader_id = %s"
        params.append(leader_filter)

    query += " ORDER BY e.event_date DESC;"

    with db.get_cursor() as cursor:
        cursor.execute(query, tuple(params))
        events = cursor.fetchall()

        # Get list of event leaders for filter
        cursor.execute('''
            SELECT user_id, full_name FROM users
            WHERE role = 'event_leader' AND status = 'active'
            ORDER BY full_name;
        ''')
        leaders = cursor.fetchall()

    return render_template('admin/manage_events.html',
                         events=events,
                         leaders=leaders,
                         search=search,
                         status_filter=status_filter,
                         leader_filter=leader_filter)

@app.route('/admin/edit_event/<int:event_id>', methods=['GET', 'POST'], endpoint='admin_edit_event')
def admin_edit_event(event_id):
    """Admin edit any event."""
    check = admin_required()
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
                WHERE event_id = %s;
            ''', (event_name, location, event_type, event_date, start_time,
                  end_time, duration, description, supplies, safety_instructions,
                  event_id))
            
            flash('Event updated successfully!', 'success')
            return redirect(url_for('admin_manage_events'))

    # GET request - show edit form
    with db.get_cursor() as cursor:
        cursor.execute('''
            SELECT e.*, u.full_name as leader_name
            FROM events e
            JOIN users u ON e.event_leader_id = u.user_id
            WHERE e.event_id = %s;
        ''', (event_id,))
        event = cursor.fetchone()

        if not event:
            flash('Event not found.', 'danger')
            return redirect(url_for('admin_manage_events'))

    return render_template('admin/edit_event.html', event=event, admin_view=True)

@app.route('/admin/cancel_event/<int:event_id>', methods=['POST'], endpoint='admin_cancel_event')
def admin_cancel_event(event_id):
    """Admin cancel any event."""
    check = admin_required()
    if check:
        return check

    with db.get_cursor() as cursor:
        # Get event details for flash message
        cursor.execute('SELECT event_name FROM events WHERE event_id = %s;', (event_id,))
        event = cursor.fetchone()
        
        if event:
            # Delete registrations first (foreign key constraint)
            cursor.execute('DELETE FROM eventregistrations WHERE event_id = %s;', (event_id,))
            # Delete feedback
            cursor.execute('DELETE FROM feedback WHERE event_id = %s;', (event_id,))
            # Delete outcomes if any
            cursor.execute('DELETE FROM eventoutcomes WHERE event_id = %s;', (event_id,))
            # Delete the event
            cursor.execute('DELETE FROM events WHERE event_id = %s;', (event_id,))
            
            flash(f'Event "{event["event_name"]}" has been cancelled.', 'success')
        else:
            flash('Event not found.', 'danger')

    return redirect(url_for('admin_manage_events'))

@app.route('/admin/view_event/<int:event_id>', endpoint='admin_view_event')
def admin_view_event(event_id):
    """Admin view event details."""
    check = admin_required()
    if check:
        return check

    with db.get_cursor() as cursor:
        cursor.execute('''
            SELECT e.*, u.full_name as leader_name,
                   (SELECT COUNT(*) FROM eventregistrations WHERE event_id = e.event_id) as registered_count,
                   (SELECT COUNT(*) FROM eventregistrations WHERE event_id = e.event_id AND attendance = 'attended') as attended_count
            FROM events e
            JOIN users u ON e.event_leader_id = u.user_id
            WHERE e.event_id = %s;
        ''', (event_id,))
        event = cursor.fetchone()

        if not event:
            flash('Event not found.', 'danger')
            return redirect(url_for('admin_manage_events'))

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

        # Get feedback
        cursor.execute('''
            SELECT f.*, u.full_name as volunteer_name
            FROM feedback f
            JOIN users u ON f.volunteer_id = u.user_id
            WHERE f.event_id = %s
            ORDER BY f.submitted_at DESC;
        ''', (event_id,))
        feedback_list = cursor.fetchall()

    return render_template('admin/event_details.html',
                         event=event, volunteers=volunteers,
                         outcomes=outcomes, feedback_list=feedback_list)

@app.route('/admin/event_report/<int:event_id>', endpoint='admin_event_report')
def admin_event_report(event_id):
    """Admin generate detailed report for a specific event."""
    check = admin_required()
    if check:
        return check

    with db.get_cursor() as cursor:
        cursor.execute('''
            SELECT e.*, u.full_name as leader_name,
                   (SELECT COUNT(*) FROM eventregistrations WHERE event_id = e.event_id) as total_registered,
                   (SELECT COUNT(*) FROM eventregistrations WHERE event_id = e.event_id AND attendance = 'attended') as total_attended,
                   eo.num_attendees, eo.bags_collected, eo.recyclables_sorted, eo.other_achievements,
                   (SELECT AVG(rating)::numeric(10,2) FROM feedback WHERE event_id = e.event_id) as avg_rating,
                   (SELECT COUNT(*) FROM feedback WHERE event_id = e.event_id) as feedback_count
            FROM events e
            JOIN users u ON e.event_leader_id = u.user_id
            LEFT JOIN eventoutcomes eo ON e.event_id = eo.event_id
            WHERE e.event_id = %s;
        ''', (event_id,))
        report = cursor.fetchone()

        if not report:
            flash('Event not found.', 'danger')
            return redirect(url_for('event_reports'))

        # Get volunteer list for this event
        cursor.execute('''
            SELECT u.full_name, u.email, u.contact_number, er.attendance
            FROM users u
            JOIN eventregistrations er ON u.user_id = er.volunteer_id
            WHERE er.event_id = %s
            ORDER BY u.full_name;
        ''', (event_id,))
        volunteers = cursor.fetchall()

        # Get all feedback for this event
        cursor.execute('''
            SELECT f.*, u.full_name as volunteer_name
            FROM feedback f
            JOIN users u ON f.volunteer_id = u.user_id
            WHERE f.event_id = %s
            ORDER BY f.submitted_at DESC;
        ''', (event_id,))
        feedback_list = cursor.fetchall()

    return render_template('admin/event_report_detail.html',
                         report=report,
                         volunteers=volunteers,
                         feedback_list=feedback_list,
                         event_id=event_id)