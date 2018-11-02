from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:aplus@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = '1234zyxw'


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(500))
    submitted = db.Column(db.Boolean)

    def __init__(self, title):
        self.title = title
        self.body = body
        self.submitted = True

@app.route('/blog', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        blog_title = request.form['title']
        new_entry = Blog(blog_title)
        db.session.add(new_entry)
        db.session.commit()

    entries = Blog.query.filter_by(submitted=True).all()
    return render_template('blog.html',title="Build-A-Blog")

@app.route('/newpost', methods = ['POST', 'GET'])
def new_post():

    if request.method == 'POST':
        blog_title = request.form['title']
        new_entry = Blog(blog_title)
        db.session.add(blog_title)
        db.session.commit()
    return render_template('newpost.html',title="New Post")

#    entries = Blog.query.filter_by(submitted=True).all()
#    return render_template('main_blog_pg.html',title="Build-A-Blog")





# @app.route('/delete-task', methods=['POST'])
# def delete_task():

#     task_id = int(request.form['task-id'])
#     task = Task.query.get(task_id)
#     task.completed = True
#     db.session.add(task)
#     db.session.commit()

#     return redirect('/')


if __name__ == '__main__':
    app.run()