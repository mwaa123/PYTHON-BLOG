from flask import render_template,request,redirect,url_for
from flask_login import login_required,current_user
from . import main
from .forms import PostForm, UpdateAccountForm,UpdateProfile,Comments
from flask import flash
from ..models import Post,User,Comment
from .. import db
from app.request import random_quotes


# from .forms import LoginForm

@main.route('/')
@login_required
def index():

    '''
    View root page function that returns the index page and its data
    '''
    posts = Post.query.all() 
    return render_template('index.html',posts=posts)
@main.route('/page')
def page():

    '''
    View root page function that returns the index page and its data
    '''
    return render_template('page.html')



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


@main.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

@main.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('main.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('posts.html', title='Update Post',
                           form=form, legend='Update Post')


@main.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.post',post_id=post_id))



def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/images', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@main.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        image_file = url_for('static', filename='images' + current_user.image_file)
    return render_template('account.html', title='Account',image_file=image_file, form=form)



@main.route("/random")
@login_required
def quotes():
    data = random_quotes() 

    return render_template('random.html',data =data)                           


@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)


@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)
   

@main.route('/post/<int:post_id>/comment', methods=['GET','POST'])
def comment(post_id):
    form_comment=Comments()
    post=post.query.filter_by(id=post_id).first()
    comment_query=Comment.query.filter_by(post_id=post.id).all()
    if form_comment.validate_on_submit():
        comment=Comment(comment=form_comment.comment.data,post_id=post.id,user_id=current_user.id)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('main.comment',post_id=post.id))
    print(image)
    return render_template('comment.html',form=form_comment,post=post,comments=comment_query,title='Comments')