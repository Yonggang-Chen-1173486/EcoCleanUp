-- Create ENUM types
CREATE TYPE user_role AS ENUM ('volunteer', 'event_leader', 'admin');
CREATE TYPE user_status AS ENUM ('active', 'inactive');
CREATE TYPE attendance_status AS ENUM ('registered', 'attended', 'no_show');

-- Users table - exactly matching ERD
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    contact_number VARCHAR(20),
    home_address VARCHAR(255),
    profile_image VARCHAR(255),
    environmental_interests VARCHAR(255),
    role user_role NOT NULL DEFAULT 'volunteer',
    status user_status NOT NULL DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Events table - exactly matching ERD
CREATE TABLE events (
    event_id SERIAL PRIMARY KEY,
    event_name VARCHAR(100) NOT NULL,
    event_leader_id INTEGER NOT NULL REFERENCES users(user_id),
    location VARCHAR(255) NOT NULL,
    event_type VARCHAR(50),
    event_date DATE NOT NULL,
    start_time TIME,
    end_time TIME,
    duration INTEGER,
    description TEXT,
    supplies TEXT,
    safety_instructions TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Eventregistrations table - exactly matching ERD with correct column names
CREATE TABLE eventregistrations (
    registration_id SERIAL PRIMARY KEY,
    event_id INTEGER NOT NULL REFERENCES events(event_id),
    volunteer_id INTEGER NOT NULL REFERENCES users(user_id),
    attendance attendance_status NOT NULL DEFAULT 'registered',
    registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(event_id, volunteer_id)
);

-- Feedback table - exactly matching ERD
CREATE TABLE feedback (
    feedback_id SERIAL PRIMARY KEY,
    event_id INTEGER NOT NULL REFERENCES events(event_id),
    volunteer_id INTEGER NOT NULL REFERENCES users(user_id),
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    comments TEXT,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(event_id, volunteer_id)
);

-- Eventoutcomes table - exactly matching ERD with all 8 columns
CREATE TABLE eventoutcomes (
    outcome_id SERIAL PRIMARY KEY,
    event_id INTEGER NOT NULL REFERENCES events(event_id) UNIQUE,
    num_attendees INTEGER DEFAULT 0,
    bags_collected INTEGER DEFAULT 0,
    recyclables_sorted INTEGER DEFAULT 0,
    other_achievements TEXT,
    recorded_by INTEGER NOT NULL REFERENCES users(user_id),
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes
CREATE INDEX idx_users ON users(username, email, role, status);
CREATE INDEX idx_events ON events(event_leader_id, event_date, event_type);
CREATE INDEX idx_feedback ON feedback(event_id, volunteer_id);
CREATE INDEX idx_eventregistrations ON eventregistrations(event_id, volunteer_id);
CREATE INDEX idx_eventoutcomes ON eventoutcomes(event_id);