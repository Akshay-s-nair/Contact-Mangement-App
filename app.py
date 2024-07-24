from flask import Flask, request, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from functools import wraps
import uuid 
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
from datetime import datetime, timedelta
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random


    
app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'zzx1keyaskfbj123asdaASas2233f'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contactmanagement.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'src/assets/profile_pictures'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    dob = db.Column(db.Date, nullable=True)
    gender = db.Column(db.String(20), nullable=True)
    phone = db.Column(db.String(15), nullable=False)
    address = db.Column(db.String(200), nullable=True)
    profile_picture = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(70), unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    contacts = db.relationship('Contacts', backref='user', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.firstname

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Contacts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(15), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'address': self.address,
            'company': self.company,
            'phone': self.phone
        }


class TokenBlacklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(500), unique=True, nullable=False)

    def __repr__(self):
        return f"<TokenBlacklist {self.token}>"
    
class PasswordReset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    reset_code = db.Column(db.String(6), nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)



with app.app_context():
    db.create_all()

# Function to send email
def send_reset_email(to_email, reset_code):
    from_email = "your_email@gmail.com"
    from_password = "your_email_password"
    subject = "Password Reset Code"

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    body = f"Your password reset code is {reset_code}"
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, from_password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False
    

def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Token is missing'}), 401

        blacklisted_token = TokenBlacklist.query.filter_by(token=token).first()
        if blacklisted_token:
            return jsonify({'error': 'Token has been revoked'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = User.query.filter_by(public_id=data['user_pid']).first()
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401

        return func(current_user, *args, **kwargs)

    return decorated




@app.route('/register', methods=['POST'])
def register():
    data = request.form.to_dict()
    profile_picture = request.files.get('profile_picture')

    required_fields = ['email', 'password', 'firstname', 'lastname', 'phone']
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        return jsonify({'error': f'Missing required fields: {", ".join(missing_fields)}'}), 400

    if User.query.filter_by(email=data.get('email')).first():
        return jsonify({'error': 'User already exists'}), 400
    
    if data.get('password')!=data.get('confirmpassword'):
        return jsonify({'error':"password does'nt match"})
    
    if profile_picture:
        filename = secure_filename(profile_picture.filename)
        profile_picture.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        data['profile_picture'] = filename

    try:
        dob = datetime.strptime(data.get('dob'), '%Y-%m-%d').date() if data.get('dob') else None
    except ValueError:
        return jsonify({'error': 'Invalid date format for dob. Use YYYY-MM-DD.'}), 400

    pid = str(uuid.uuid4())
    new_user = User(
        public_id=pid,
        firstname=data.get('firstname'),
        lastname=data.get('lastname'),
        email=data.get('email'),
        dob=dob,
        gender=data.get('gender'),
        phone=data.get('phone'),
        address=data.get('address'),
        profile_picture=data.get('profile_picture')
    )
    new_user.set_password(data.get('password'))
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'Successfully Registered. Now you can Login.'}), 201



@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email:
        return jsonify({'error': 'Email is Missing'}), 400
    elif validateEmail(email):
        return jsonify({'error': 'Invalid Email Format'}), 400
    elif not password:
        return jsonify({'error': 'Password is Missing'}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'error': 'No user found'}), 401
    
    if not user.check_password(password):
        return jsonify({'error': 'Wrong Password'}), 401

    # Add a timestamp to the token payload to make it unique
    token = jwt.encode(
        {
            'user_pid': user.public_id,
            'exp': datetime.utcnow() + timedelta(hours=24),
            'iat': datetime.utcnow()
        }, 
        app.config['SECRET_KEY'], 
        algorithm='HS256'
    )
    return jsonify({'token': token, 'username': user.firstname+" "+user.lastname}), 200

def validateEmail(email):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return True

@app.route('/logout', methods=['POST'])
@token_required
def logout(current_user):
    token = request.headers.get('Authorization')

    # Add the token to the blacklist
    blacklisted_token = TokenBlacklist(token=token)
    db.session.add(blacklisted_token)
    db.session.commit()

    return jsonify({'message': 'Successfully logged out'}), 200

@app.route('/contacts', methods=['GET'])
@token_required
def get_contacts(current_user):
    search = request.args.get('search', '', type=str)
    sort = request.args.get('sort', 'id', type=str)  # default to 'id'
    sort_order = request.args.get('sort_order', 'asc', type=str)  # default to 'asc'

    query = Contacts.query.filter(Contacts.user_id == current_user.id)

    if search:
        query = query.filter(
            (Contacts.firstname.ilike(f'%{search}%')) |
            (Contacts.lastname.ilike(f'%{search}%'))
        )

    if sort == 'name':
        if sort_order == 'asc':
            query = query.order_by(Contacts.firstname.asc())
        else:
            query = query.order_by(Contacts.firstname.desc())
    else:  # default sort by 'id'
        if sort_order == 'asc':
            query = query.order_by(Contacts.id.asc())
        else:
            query = query.order_by(Contacts.id.desc())

    contacts = query.all()
    total_count = query.count()
    return jsonify({
        'total_count': total_count,
        'contacts': [contact.to_dict() for contact in contacts]
    }), 200




@app.route('/contacts', methods=['POST'])
@token_required
def add_contact(current_user):
    try:
        data = request.get_json()
        # required_fields = ['firstname', 'lastname', 'address', 'company', 'phone']
        # missing_fields = [field for field in required_fields if field not in data]

        # if missing_fields:
        #     return jsonify({'error': f'Missing required fields: {", ".join(missing_fields)}'}), 400

        # if not all(field in data for field in required_fields):
        #     return jsonify({'error': 'Missing required fields'}), 400

        new_contact = Contacts(
            user_id=current_user.id,
            firstname=data.get('firstname'),
            lastname=data.get('lastname'),
            address=data.get('address'),
            company=data.get('company'),
            phone=data.get('phone')
        )
        db.session.add(new_contact)
        db.session.commit()
        return jsonify(new_contact.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400



@app.route('/contacts/<int:id>', methods=['PUT'])
@token_required
def update_contact(current_user, id):
    data = request.get_json()
    contact = Contacts.query.get(id)
    if Contacts.query.get(id) == None:
        return jsonify({'message': 'Contact not found'}), 404
    if contact.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 401

    contact.firstname = data.get('firstname', contact.firstname)
    contact.lastname = data.get('lastname', contact.lastname)
    contact.address = data.get('address', contact.address)
    contact.company = data.get('company', contact.company)
    contact.phone = data.get('phone', contact.phone)
    db.session.commit()
    return jsonify(contact.to_dict()), 200


@app.route('/contacts/<int:id>', methods=['DELETE'])
@token_required
def delete_contact(current_user, id):
    contact = Contacts.query.get_or_404(id)
    if contact.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 401

    db.session.delete(contact)
    db.session.commit()
    return jsonify({'message': 'Contact deleted'}), 200

@app.route('/forgot_password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    email = data.get('email')
    phone = data.get('phone')

    user = User.query.filter_by(email=email, phone=phone).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Generate reset code
    reset_code = str(random.randint(100000, 999999))
    expires_at = datetime.utcnow() + timedelta(minutes=10)

    # Save reset code in the database
    reset_record = PasswordReset(user_id=user.id, reset_code=reset_code, expires_at=expires_at)
    db.session.add(reset_record)
    db.session.commit()

    # Send reset code to user's email
    if send_reset_email(user.email, reset_code):
        return jsonify({'message': 'Password reset code sent to your email'}), 200
    else:
        return jsonify({'error': 'Failed to send reset code'}), 500

@app.route('/reset_password', methods=['POST'])
def reset_password():
    data = request.get_json()
    email = data.get('email')
    reset_code = data.get('reset_code')
    new_password = data.get('new_password')

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Validate reset code
    reset_record = PasswordReset.query.filter_by(user_id=user.id, reset_code=reset_code).first()
    if not reset_record or reset_record.expires_at < datetime.utcnow():
        return jsonify({'error': 'Invalid or expired reset code'}), 400

    # Update user's password
    user.set_password(new_password)
    db.session.commit()

    # Delete the reset record
    db.session.delete(reset_record)
    db.session.commit()

    return jsonify({'message': 'Password reset successful'}), 200
if __name__ == '__main__':
    app.run(debug=True)
