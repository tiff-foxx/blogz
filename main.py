from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:aplus@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
# app.secret_key = '1234zyxw'


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(500))
    submitted = db.Column(db.Boolean)

    def __init__(self, title, body):
        self.title = title
        self.body = body
        self.submitted = True

@app.route('/blog', methods=['GET','POST'])
def index():

    if request.method == 'POST':
        blog_title = request.form['title']
        blog_body = request.form['body']
        new_entry = Blog(blog_title, blog_body)
      
    entries = Blog.query.filter_by(submitted=True).all()
    return render_template('blog.html',title="Build-A-Blog",entries=entries)

@app.route('/newpost', methods = ['GET','POST'])
def new_post():
    if request.method == 'POST':
        blog_title = request.form['title']
        blog_body = request.form['body']
        empty_error = ''
        if len(blog_title)<= 0 or len(blog_body)<=0:
            empty_error = 'Title and Body fields required'
            return render_template('newpost.html',title='TESTING',empty_error=empty_error,blog_title=blog_title,blog_body=blog_body)
            
        else: 
            new_entry = Blog(blog_title, blog_body)
            db.session.add(new_entry)
            db.session.commit()
            entries = Blog.query.filter_by(submitted=True).all()
            return render_template('blog.html',title="Build-A-Blog",entries=entries)

    return render_template('newpost.html',title="New Post")

@app.route("/individual")
def individual_blog():
    request.args.get('id')
    request.args.get('blog_body')
    return render_template('individual.html',title='123TESTING')
    
    #username = request.form['username']
    #template = jinja_env.get_template('valid_signup.html')
    #return template.render(name = username) -->

    # entries = Blog.query.filter_by(submitted=True).all()
    # return render_template('blog.html',title="Build-A-Blog")

if __name__ == '__main__':
    app.run()