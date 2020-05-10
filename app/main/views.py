from flask import render_template,request,redirect,url_for
from flask_login import login_required,current_user
from . import main
from .forms import PostForm 
from flask import flash
from ..models import Post,User
from .. import db

# from .forms import LoginForm
# posts =[{
#     'author':"ruth mugo",
#     'title':'Blog Post 1',
#     'content':'First Post Content',
#     'date_posted':'April 20,2020'
# },{
#     'author':"wesley mugo",
#     'title':'Blog Post 2',
#     'content':'Second  Post Content',
#     'date_posted':'April 20,2029'
# }]
# Views
@main.route('/')
@login_required
def index():

    '''
    View root page function that returns the index page and its data
    '''
    # global Post
    posts = Post.query.all() 
    return render_template('index.html',posts=posts)

@main.route('/post/new',methods=['GET','POST'])
@login_required 
def new_post():
    form =PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,content=form.content.data,author=current_user)
        db.session.add(post)
        db.session.commit()

        flash('Your post has been created','success')
        return redirect(url_for('main.index')) 
    '''
    View root page function that returns the index page and its data
    '''
    return render_template('posts.html',form=form)
