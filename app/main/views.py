from flask import render_template,request,redirect
from flask_login import login_required
from . import main


# Views
@main.route('/')
@login_required
def index():

    '''
    View root page function that returns the index page and its data
    '''
    return render_template('index.html')

@main.route('/post/new',methods=['GET','POST'])
@login_required 
def new_post():
    form =PostForm()
    if login_form.validate_on_submit():
        flash('Your post has been created')
        return redirect(url_for('index')) 
    '''
    View root page function that returns the index page and its data
    '''
    return render_template('posts.html',form=form)
