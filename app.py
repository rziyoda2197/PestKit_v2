from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pest_kit.db'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max fayl hajmi
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Upload papkasini yaratish
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)

class Team(db.Model):
    __tablename__ = 'teams'
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(255), nullable=True)
    rank = db.Column(db.String(250))
    image = db.Column(db.Text, nullable=True)
   
class Contact(db.Model):
    __tablename__ = 'contacts'
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(255), nullable=True)
    email = db.Column(db.String(255), nullable=True)
    subject = db.Column(db.String(200), nullable=True)
    message = db.Column(db.Text(), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    


@app.route('/')
def index():
    teams = Team.query.all()[:4]
    return render_template('index.html', title='Home page', teams=teams)

@app.route('/error')
def error404():
    return render_template('404.html', title='Error 404')

@app.route('/about')
def about():
    teams = Team.query.all()[:4]
    return render_template('about.html', title='About', teams=teams)

@app.route('/blog')
def blog():
    return render_template('blog.html', title='Blog')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        fullname = request.form.get('fullname').strip().title()
        email = request.form.get('email').strip()
        subject = request.form.get('subject').strip().capitalize()
        message = request.form.get('message').strip().capitalize()

        contact = Contact(
            fullname=fullname,
            email=email,
            subject=subject,
            message=message
        )

        db.session.add(contact)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('contact.html', title='Contact')


@app.route('/price')
def price():
    return render_template('price.html', title='Price')

@app.route('/project')
def project():
    return render_template('project.html', title='Project')

@app.route('/service')
def service():
    return render_template('service.html', title='Service')

@app.route('/team')
def team():
    teams = Team.query.all()[:4]
    return render_template('team.html', title='Team', teams=teams)

@app.route('/testimonial')
def testimonial():
    return render_template('testimonial.html', title='Testimonial')




if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)


