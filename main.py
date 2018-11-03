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
        # db.session.add(new_entry)
        # db.session.commit()
        

    entries = Blog.query.filter_by(submitted=True).all()
    return render_template('blog.html',title="Build-A-Blog",entries=entries)


# @app.route('/', methods=['POST', 'GET'])
# def index():

#     if request.method == 'POST':
#         task_name = request.form['task']
#         new_task = Task(task_name)
#         db.session.add(new_task)
#         db.session.commit()

#     tasks = Task.query.filter_by(completed=False).all()
#     completed_tasks = Task.query.filter_by(completed=True).all()
#     return render_template('todos.html',title="Get It Done!", 
#         tasks=tasks, completed_tasks=completed_tasks)

@app.route('/newpost', methods = ['GET','POST'])
def new_post():

    if request.method == 'POST':
        blog_title = request.form['title']
        blog_body = request.form['body']
        new_entry = Blog(blog_title, blog_body)
        db.session.add(new_entry)
        db.session.commit()
        entries = Blog.query.filter_by(submitted=True).all()
        return render_template('blog.html',title="Build-A-Blog",entries=entries)

    return render_template('newpost.html',title="New Post")
    # entries = Blog.query.filter_by(submitted=True).all()
    # return render_template('blog.html',title="Build-A-Blog")




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