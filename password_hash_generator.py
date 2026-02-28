"""Script to generate password hashes for user accounts."""
from collections import namedtuple
from flask import Flask
from flask_bcrypt import Bcrypt

UserAccount = namedtuple('UserAccount', ['username', 'password'])

app = Flask(__name__)
flask_bcrypt = Bcrypt(app)

# Volunteers - password: Volunteer123!
volunteers = [
    UserAccount('emily_wilson', 'Volunteer123!'),
    UserAccount('james_chen', 'Volunteer123!'),
    UserAccount('sarah_parker', 'Volunteer123!'),
    UserAccount('michael_torres', 'Volunteer123!'),
    UserAccount('lisa_wong', 'Volunteer123!'),
    UserAccount('david_kumar', 'Volunteer123!'),
    UserAccount('emma_thompson', 'Volunteer123!'),
    UserAccount('ryan_obrien', 'Volunteer123!'),
    UserAccount('olivia_martinez', 'Volunteer123!'),
    UserAccount('thomas_williams', 'Volunteer123!'),
    UserAccount('grace_lee', 'Volunteer123!'),
    UserAccount('benjamin_clark', 'Volunteer123!'),
    UserAccount('sophie_taylor', 'Volunteer123!'),
    UserAccount('daniel_anderson', 'Volunteer123!'),
    UserAccount('chloe_robinson', 'Volunteer123!'),
    UserAccount('matthew_white', 'Volunteer123!'),
    UserAccount('hannah_brown', 'Volunteer123!'),
    UserAccount('lucas_garcia', 'Volunteer123!'),
    UserAccount('mia_johnson', 'Volunteer123!'),
    UserAccount('alexander_nguyen', 'Volunteer123!')
]

# Event Leaders - password: Leader123!
event_leaders = [
    UserAccount('rachel_green', 'Leader123!'),
    UserAccount('mark_sutherland', 'Leader123!'),
    UserAccount('jennifer_patel', 'Leader123!'),
    UserAccount('robert_fisher', 'Leader123!'),
    UserAccount('maria_rodriguez', 'Leader123!')
]

# Admins - password: Admin123!
admins = [
    UserAccount('admin_smith', 'Admin123!'),
    UserAccount('admin_wilson', 'Admin123!')
]

all_users = volunteers + event_leaders + admins

print('Username | Password | Hash')
print('-' * 80)

for user in all_users:
    password_hash = flask_bcrypt.generate_password_hash(user.password)
    print(f'{user.username} | {user.password} | {password_hash.decode()}')