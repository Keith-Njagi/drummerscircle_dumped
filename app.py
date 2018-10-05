from flask import Flask, render_template, url_for, redirect, request, flash
from flask_sqlalchemy import SQLAlchemy

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from forms import LogInForm, RegisterForm, ContactForm, AddPost, UploadTutorialForm
from flask_mail import Message, Mail
from datetime import datetime
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

mail = Mail()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///drumcircle.sqlite'
app.config['SECRET_KEY'] = 'su93r-su93r-s3cr3t-qu1t3-h@r6-t0-h@ck'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 534
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'drummerscirclesupport@gmail.com'
app.config['MAIL_PASSWORD'] = 'drumc1rcl3@001'

admin = Admin(app)
mail.init_app(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30))
    subtitle = db.Column(db.String(50))
    author = db.Column(db.String(20))
    date_posted = db.Column(db.DateTime)
    content = db.Column(db.Text)

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(BlogPost, db.session))

@app.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('index.html', loggedin=True)
    else:
        return render_template('index.html')

@app.route('/about')
def about():
    if current_user.is_authenticated:
        return render_template('about.html', loggedin=True)
    else:
        return render_template('about.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LogInForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(request.args.get("next") or url_for('blogposts'))

        return '<h1>Invalid Username or Password</h1>'

    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.password.data == form.password_confirm.data:
        if form.validate_on_submit():
            hashed_password = generate_password_hash(form.password.data, method='sha256')
            new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            return '<h1>New User has been created</h1><br/><p><a href="JavaScript:history.go(-1);">Back</a></p>'
    else:
        return '<h1>Please ensure your passwords match!</h1><br/><p><a href="JavaScript:history.go(-1);">Back</a></p>' 


    return render_template('register.html', form=form)


@app.route('/forums')
@login_required
def forums():
    return render_template('forums.html', loggedin=True)

@app.route('/blogposts')
@login_required
def blogposts():
    posts = BlogPost.query.order_by(BlogPost.date_posted.desc()).all()
    post = BlogPost.query.filter_by(id=BlogPost.id).first()
    
    return render_template('blogposts.html',loggedin=True, user=current_user.username, posts=posts, post=post)



@app.route('/tutorials')
@login_required
def tutorials():
    return render_template('tutorials.html', loggedin=True)


@app.route('/getsupport', methods=['GET', 'POST'])
@login_required
def getsupport():
    form = ContactForm()

    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required')
            return render_template('getsupport.html', loggedin=True, form=form, user=current_user.username)
        else:
            msg = Message(form.subject.data, sender=['drummerscirclesupport@gmail.com'], recipients=['drummerscircle@gmail.com'])
            msg.body = """
            From: %s <%s>
            %s
            """ % (form.name.data, form.email.data, form.message.data)
            mail.send(msg)
            return render_template('getsupport.html', success=True, loggedin=True, user=current_user.username)
    elif request.method == 'GET':
        return render_template('getsupport.html', loggedin=True, form=form, user=current_user.username)

@app.route('/participate')
@login_required
def participate():
    return render_template('participate.html', loggedin=True)

@app.route('/profile/<username>')
@login_required
def profile(username):
    username=current_user.username
    user = User.query.filter_by(username=username).first()
    return render_template('profile.html', loggedin=True, user=user, username=current_user.username)


@app.route('/addpost', methods=['GET','POST'])
@login_required
def addpost():
    form = AddPost()
    author = current_user.username
    
    if request.method == 'POST':
        if form.validate_on_submit() == False:
            flash('Please fill all Fields')
            return render_template('add_blog_post.html', loggedin=True, form=form)
        else:
            post = BlogPost(title=form.title.data, subtitle=form.subtitle.data, author=author, content=form.content.data, date_posted=datetime.now())

            db.session.add(post)
            db.session.commit()
            return render_template('add_blog_post.html', success=True, loggedin=True, user=current_user.username)
    elif request.method == 'GET':
        return render_template('add_blog_post.html', loggedin=True, form=form)

@app.route('/post/<int:post_id>')
@login_required
def post(post_id):
    post = BlogPost.query.filter_by(id=post_id).one()

    return render_template('post.html', post=post, loggedin=True)

@app.route('/addtutorial', methods=['GET', 'POST'])
@login_required
def addtutorial():
    form = UploadTutorialForm()
    
    return render_template('addtutorial.html', form=form, loggedin=True)


@app.route('/uploadtutorial', methods=['POST'])
@login_required
def uploadtutorial():
    form = UploadTutorialForm()
    file = request.files['tutorialFile']
    
    return render_template('addtutorial.html', form=form, loggedin=True, success=True)


if __name__ == '__main__':
    app.run(debug=True)
