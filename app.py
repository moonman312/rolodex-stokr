from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import config
from flask_mail import Mail, Message
from flask_apscheduler import APScheduler

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'  # Replace with your secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # Using SQLite for local development
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = config.sender_email_address
app.config['MAIL_PASSWORD'] = config.app_password
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
mail = Mail(app)
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

# User model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150))
    name = db.Column(db.String(150))
    contacts = db.relationship('Contact', backref='user', lazy=True)

# Contact model
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    note = db.Column(db.String(500))
    frequency = db.Column(db.Integer)  # in days
    last_interaction = db.Column(db.Date)
    next_interaction = db.Column(db.Date)
    email = db.Column(db.String(150))
    phone_number = db.Column(db.String(20))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        email = request.form['email']
        name = request.form['name']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return redirect(url_for('register'))

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered!', 'danger')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        user = User(email=email, name=name, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if not user:
            flash('Invalid email or password.', 'danger')
            return redirect(url_for('login'))
        if not check_password_hash(user.password, password):
            flash('Invalid email or password.', 'danger')
            return redirect(url_for('login'))

        login_user(user)
        return redirect(url_for('dashboard'))

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    contacts = Contact.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', contacts=contacts)

@app.route('/add_contact', methods=['GET', 'POST'])
@login_required
def add_contact():
    if request.method == 'POST':
        name = request.form['name']
        note = request.form['note']
        frequency = int(request.form['frequency'])
        email = request.form['email']
        phone_number = request.form['phone_number']
        today = datetime.now().date()
        next_interaction = today + timedelta(days=frequency)
        contact = Contact(
            name=name,
            note=note,
            frequency=frequency,
            email=email,
            phone_number=phone_number,
            last_interaction=today,
            next_interaction=next_interaction,
            user_id=current_user.id
        )
        db.session.add(contact)
        db.session.commit()
        flash('Contact added successfully!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('add_contact.html')

@app.route('/edit_contact/<int:contact_id>', methods=['GET', 'POST'])
@login_required
def edit_contact(contact_id):
    contact = Contact.query.get_or_404(contact_id)
    if contact.user_id != current_user.id:
        flash('Unauthorized access!', 'danger')
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        contact.name = request.form['name']
        contact.note = request.form['note']
        contact.frequency = int(request.form['frequency'])
        contact.email = request.form['email']
        contact.phone_number = request.form['phone_number']
        db.session.commit()
        flash('Contact updated successfully!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('edit_contact.html', contact=contact)

@app.route('/delete_contact/<int:contact_id>')
@login_required
def delete_contact(contact_id):
    contact = Contact.query.get_or_404(contact_id)
    if contact.user_id != current_user.id:
        flash('Unauthorized access!', 'danger')
        return redirect(url_for('dashboard'))
    db.session.delete(contact)
    db.session.commit()
    flash('Contact deleted successfully!', 'success')
    return redirect(url_for('dashboard'))

def send_reminders():
    today = datetime.now().date()
    contacts = Contact.query.filter(Contact.next_interaction <= today).all()
    for contact in contacts:
        user = User.query.get(contact.user_id)
        if user:
            # Send email reminder
            msg = Message(f"Reminder to contact {contact.name}",
                          sender=config.sender_email_address,
                          recipients=[user.email])
            time_since_last = (today - contact.last_interaction).days
            msg.body = f"Hi {user.name},\n\nYou haven't interacted with {contact.name} for {time_since_last} days. Don't forget to reach out!\n\nNote: {contact.note}"
            mail.send(msg)
            # Send SMS reminder via Twilio (if phone_number is provided)
            if contact.phone_number:
                send_sms(contact.phone_number, msg.body)
            # Update next_interaction date
            contact.next_interaction = today + timedelta(days=contact.frequency)
            db.session.commit()

def send_sms(phone_number, message):
    from twilio.rest import Client
    client = Client(config.TWILIO_ACCOUNT_SID, config.TWILIO_AUTH_TOKEN)
    client.messages.create(
        body=message,
        from_=config.TWILIO_PHONE_NUMBER,
        to=phone_number
    )

@scheduler.task('cron', id='send_reminders', hour=8)
def scheduled_task():
    with app.app_context():
        send_reminders()


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)