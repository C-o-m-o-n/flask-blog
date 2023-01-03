#import all the necessary packages
from flask import Flask, render_template, url_for, request, redirect
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
#initialise Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
#initialise SQLAlchemy with Flask
db = SQLAlchemy(app)

#define the BlogPost table
class BlogPost(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(50))
  subtitle = db.Column(db.String(50))
  author = db.Column(db.String(50))
  date_posted = db.Column(db.DateTime)
  content = db.Column(db.Text)

with app.app_context(): #put all the code inside the app context
  #the homepage
  @app.route('/')
  def index():
    posts = BlogPost.query.all()
    return render_template("index.html", posts=posts)
  #the about page
  @app.route('/about')
  def about():
    return render_template("about.html")
  #the post page
  @app.route('/post/<int:post_id>')
  def post(post_id):
    post = BlogPost.query.filter_by(id=post_id).one()
    date_posted = post.date_posted.strftime('%B, %d, %Y')
    return render_template("post.html", post=post, date_posted=date_posted)
  #the page for adding posts from the frontend  
  @app.route('/add')
  def add():
    return render_template("add.html")
  #handles the posts
  @app.route('/addpost', methods=['POST'])
  def addpost():
    title = request.form['title']
    subtitle = request.form['subtitle']
    author = request.form['author']
    content = request.form['content']
    
    post = BlogPost(title=title, subtitle=subtitle, author=author, content=content, date_posted=datetime.now())
    db.create_all()
    db.session.add(post)
    db.session.commit()
    return redirect(url_for('index'))
  #the contact page
  @app.route('/contact')
  def contact():
    return render_template("contact.html")
  #run the Flask app
  if __name__ == "__main__":
    app.run(debug=True)