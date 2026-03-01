# EcoCleanUp Hub

EcoCleanUp Hub is a web-based community cleanup management system developed for the GreenSteps Initiative. 
The platform connects volunteers with local cleanup events, helps event leaders coordinate activities, and provides administrators with oversight and reporting tools.

There are three user roles in this system:
- **Volunteer**
- **Event Leader**
- **Admin**

Anyone who registers via the app will be default to **Volunteer**. 
Creating new accounts for **Event Leader** or **Admin** would require direct database population with INSERT function in PostgreSQL.


## Authorship Statement

I used AI (DeepSeek, Github Copilot) assistance for:
- Code structure suggestions
- Multiple complex route functions and HTML templates
- Bootstrap layout examples
- Create database population script for all tables
- Form validation patterns

All code was reviewed, tested, and understood before implementation.

Used prompts:
- "Event_outcomes" have actually 8 columns, but you only provided 5 of them, also column name convention is not the same. "eventregistrations" you provided the right amount of columns but the column name convention is not the same. "feedback", "users" and "events" table seem to be correct. But I do need "status" ENUM in users table and "attendance" ENUM in eventregistrations table to be predefined just like "role" ENUM.

- Today's date is 27th Feb 2026, all the event dates provided are after March 2026 - I am unsure why you said  5 events are in the past? Please provide a complete answer again

- In the Event data you provided, the 10 rows of past events data are not on the top for INSERT, do we need to adjust the sequence as the event id might impact the relationship with other tables. Please evaluate and fix the issue then provide me correct datasets.

- I am trying to log in account admin_smith, received this error below. Could you troubleshoot the issue for me and provide step-by-step fix with detailed explanations.
ValueError
ValueError: Invalid salt

- I logged in as event leader, when I tried to view the event called 'North Beach Spring Clean' with the 'View' button, I am experiencing the below error. Could you troubleshoot the issue for me and provide step-by-step fix with detailed explanations.
TypeError
TypeError: '<' not supported between instances of 'datetime.date' and 'datetime.datetime'

- I created an account username as EDDIE_CHAN, when I tried to log on with lower case eddie_chan, it did not work. Should we cater for this for username?

- When I test and modify the contact number, it allows to contain letter like 'sss' I think it should only allow + sign and numbers as a proper data validation, is that correct?


## Deploy and Use the Web App

To run the example yourself, you'll need to:

1. Open the project folder in Visual Studio Code.
2. Create a virtual environment under Command Palette.
3. Install all of the packages listed in requirements.txt while creating the virtual environment.
4. Create tables and populate the tables in PostgreSQL with database_creation_script and database_population_script for the **EcoCleanUp** project.
5. Modify [connect.py](loginapp/connect.py) with the connection details for
   your local database server.
6. Run [The Python/Flask application](run.py).

After executing the steps above, you should be able to register yourself a new **Volunteer** and use EcoCleanUp Hub.
You should also be able to use the account details provided in the submitted Excel sheet to test out the functionalities for **Volunteer**, **Event Leader**, or **Admin**.


## Features

### For All Users
- Login and logout
- Profile management - with options to upload image
- Change password
- Browse all upcoming cleanup events
- Receive reminders for upcoming events

### For Volunteers
- Sign up as a new Volunteer - data validation hints were implemented for email, phone number, password
- Register for upcoming events
- View personal participation history
- Submit feedback (rating and comments) for past events - The feedback button will only show when there's no existing personal review for a past event
- Receive reminders for upcoming events on home page

### For Event Leaders
- Create and manage cleanup events
- View registered volunteers for an event
- Remove volunteers from an event
- Track volunteer attendance - Event Leader can edit volunteer's attendance status
- Record event outcomes (bags collected, recyclables sorted) - The record outcomes button will only show when there's no existing outcomes for a past event
- Track participation history for volunteers in all events they manage
- Send reminders to volunteers - a pop-up flash message was implemented
- Review volunteer feedback
- Generate event reports - print report feature is also available

### For Administrators
- View past events that volunteer has participated in
- Manage existing events (edit and cancel)
- View registered volunteers for an event
- View all users with search functions
- Manage user accounts (activate/deactivate)
- View platform-wide statistics
- Generate event reports for all events - print report feature is also available


## Passwords

Users' passwords are not stored directly in our users table in the PostgreSQL database. Instead, we use the Flask-Bcrypt library to bundle a Bcrypt version number, users' password hash with a randomly generared salt value. Then this will be stored in our users table as a hash password to protect. The script below was used in our project to generate the hashed passwords for all users.
- [Python script to create password hashes](password_hash_generator.py)