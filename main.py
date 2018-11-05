from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:Done530@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = '1234zyxw'


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(500))
    submitted = db.Column(db.Boolean)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.submitted = True
        self.owner = owner

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password

@app.before_request
def require_login():
    allowed_routes = ['login', 'blog_page', 'index', 'signup']
    if request.endpoint not in allowed_routes and 'username' not in session:
        # flash(request.endpoint)
        return redirect('/login')

@app.route('/blog', methods=['GET','POST'])
def blog_page():


    
    if request.method == 'POST':
        blog_title = request.form['title']
        blog_body = request.form['body']
        new_entry = Blog(blog_title, blog_body)

    entries = Blog.query.filter_by(submitted=True).all()
    return render_template('blog.html',title="Build-A-Blog",entries=entries)


@app.route('/newpost', methods = ['GET','POST'])
def new_post():

    owner = User.query.filter_by(username=session['username']).first()
    
    if request.method == 'POST':
        blog_title = request.form['title']
        blog_body = request.form['body']
        title_error = ''
        body_error = ''

        if len(blog_title) <= 0:
            title_error = 'Please enter title'

        if len(blog_body) <= 0:
            body_error = 'Please enter body'

        if not title_error and not body_error:
            new_entry = Blog(blog_title, blog_body, owner)
            db.session.add(new_entry)
            db.session.commit()
            entries = Blog.query.filter_by(id=new_entry.id).all()
            return render_template('individual.html',title='latest_entry',entries=entries)
        else:
            return render_template('newpost.html',title='TESTING',title_error=title_error,body_error=body_error,blog_title=blog_title,blog_body=blog_body)

    return render_template('newpost.html',title="New Post")


@app.route("/individual")
def individual_blog():
    blog_id = request.args.get('id')
    entries = Blog.query.filter_by(id=blog_id).all()
    return render_template('individual.html',title='123TESTING',entries=entries)


@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and user.password == password:
            session['username'] = username
            flash('Logged in')
            return redirect ('/newpost')

        if user and user.password != password:
            flash('Password incorrect')
            return render_template('login.html',title='OHOHO')

        if user not in User.query.filter_by(username=username).all():
            flash('Username does not exist')
            return render_template('login.html',title="HAHAHA")
        
    return render_template('login.html',title="Login Page")
    


@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        
        blank_error = ''
        username_error = ''
        length_error = ''
        verify_error = ''
   
        if len(username) == 0 or len(password) == 0 or len(verify) == 0:
            blank_error = 'One or more fields empty'
            return render_template('signup.html',title="Try AgainA",
            username=username,password=password,verify=verify,blank_error=blank_error,
            username_error=username_error,length_error=length_error,verify_error=verify_error)
        
        existing_user = User.query.filter_by(username=username).first()
        if existing_user: 
            username_error = 'Username already exists'
            return render_template('signup.html',title="Try AgainD",username=username,password=password,
            verify=verify,blank_error=blank_error, username_error=username_error,length_error=length_error,
            verify_error=verify_error)

        if password != verify:
            verify_error = 'Passwords must match'
            return render_template('signup.html',title="Try AgainB",
            username=username,password=password,verify=verify,blank_error=blank_error,
            username_error=username_error,length_error=length_error,verify_error=verify_error)

        if len(username) <3 or len(password) <3:
            length_error = 'Username and password must be between 3-20 characters'
            return render_template('signup.html',title="Try AgainC",username=username,
            password=password,verify=verify,blank_error=blank_error,
            username_error=username_error,length_error=length_error,verify_error=verify_error)
      
        if not blank_error and not username_error and not length_error and not verify_error:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            flash('Welcome')
            return redirect ('/newpost')
    else:
        return render_template('signup.html',title="Blogz Signup")

@app.route('/logout')
def logout(): 
    session.clear()
    return redirect('/blog')

@app.route('/')
def index():   
    users = User.query.filter_by(username= User.username).all()
    return render_template('index.html',title="Home_All Users",users=users)

@app.route('/user_id_page')
def user_id_page():
    
    if request.method == 'GET':
        user_id = request.args.get('user')
        entries = Blog.query.filter_by(owner_id=user_id).all()
        return render_template('blog.html',title='HotDog',entries=entries)
        # return render_template('user_id_page',title='HotDog',users=users,entries=entries)


if __name__ == '__main__':
    app.run()

