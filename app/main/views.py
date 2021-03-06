from . import main
from flask import render_template,abort,flash,redirect,url_for,request,current_app,make_response
from datetime import datetime
from flask_login import login_required,current_user
from ..models import User,db,Role,Permission,Post,Follow,Comment
from .forms import EditProfileForm, EditProfileAdminForm,PostForm,CommentForm
from ..decorators import admin_required,permission_required
import hashlib
from ..email import send_email
from .list_to_dict import ListtoDict


@main.route('/',methods=['GET','POST'])
def index():
    form=PostForm()
    if current_user.can(Permission.WRITE_ARTICLES) and form.validate_on_submit():
        post=Post(body=form.body.data,author_id=current_user.id)
        db.session.add(post)
        return redirect(url_for('main.index'))
    #按时间排序
    #分页对路由的改动

    show_followed=False
    if current_user.is_authenticated:
        show_followed=bool(request.cookies.get('show_followed',''))
    if show_followed:
        query_1=current_user.followed_posts
    else:
        query_1=Post.query

    page=request.args.get('page',1,type=int)
    pagination=query_1.order_by(Post.timestamp.desc()).paginate(
        page,per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],error_out=False
    )
    posts=pagination.items

    return render_template('index.html',form=form,posts=posts,pagination=pagination)

@main.route('/user/<username>',methods=['GET','POST'])
def user(username):
    user=User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    page=request.args.get('page',1,type=int)
    pagination=user.posts.order_by(Post.timestamp.desc()).paginate(
        page=page,per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],error_out=False)
    posts=pagination.items

    return render_template('user.html',user=user,posts=posts,pagination=pagination)

@main.route('/edit-profile',methods=['GET','POST'])
@login_required
def edit_profile():
    form=EditProfileForm()
    if form.validate_on_submit():
        current_user.name=form.name.data
        current_user.location=form.location.data
        current_user.about_me=form.about_me.data
        db.session.add(current_user)
        flash('你的资料已更新')
        return redirect(url_for('main.edit_profile'))

    form.name.data=current_user.name
    form.location.data=current_user.location
    form.about_me.data=current_user.about_me
    return render_template('edit_profile.html',form=form)

@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        flash('The profile has been updated.')
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)

@main.route('/post/<int:id>',methods=['GET','POST'])
def post(id):
    post=Post.query.get_or_404(id)
    form=CommentForm()
    if form.validate_on_submit():
        comment=Comment(body=form.body.data,author=current_user._get_current_object(),post=post)
        db.session.add(comment)
        flash('评论已经提交')
        return redirect(url_for('main.post',id=post.id,page=-1))
    page=request.args.get('page',1,type=int)
    if page==-1:
        page = (post.comments.count() - 1) // \
            current_app.config['FLASKY_COMMENTS_PER_PAGE'] + 1
    pagination = post.comments.order_by(Comment.timestamp.asc()).paginate(
        page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    return render_template('post.html', posts=[post], form=form,
                           comments=comments, pagination=pagination)
@main.route('/post_edit/<int:id>',methods=['GET','POST'])
@login_required
def post_edit(id):
    form=PostForm()
    post = Post.query.get_or_404(id)
    old_msg=post.body
    if current_user != post.author and not current_user.can(Permission.ADMINISTER):
        abort(403)

    if form.validate_on_submit():
        post.body=form.body.data
        db.session.add(post)
        flash('你的文章已经修改')
        if not post.author.can(Permission.ADMINISTER):
            send_email(post.author.email, '信息修改', 'auth/email/msg_edit',old_msg=old_msg,post=post)



        return redirect(url_for('main.post',id=id))
    form.body.data=post.body


    return render_template('postedit.html', form=form)

@main.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user=User.query.filter_by(username=username).first()
    if user is None:
        flash('用户不存在')
        return redirect(url_for('main.index'))
    if not current_user.is_following(user):
        flash('你没有关注他')
        return redirect(url_for('main.user', username=user.username))
    current_user.unfollow(user)

    return redirect(url_for('main.user',username=user.username))

@main.route('/follow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    if current_user.is_following(user):
        flash('You are already following this user.')
        return redirect(url_for('.user', username=username))
    current_user.follow(user)
    flash('You are now following %s.' % username)
    return redirect(url_for('.user', username=username))

@main.route('/followers/<username>')
def followers(username):
    user=User.query.filter_by(username=username).first()
    if user is None:
        flash('用户不存在')
        return redirect(url_for('main.index'))

    page = request.args.get('page', 1, type=int)

    pagination = user.followers.paginate(
        page, per_page=current_app.config['FLASKY_FOLLOWERS_PER_PAGE'],
        error_out=False)




    follows = [{'user': item.follower, 'timestamp': item.timestamp}
               for item in pagination.items if item.follower.username!= username]
    follows=ListtoDict(follows,'num').f



    return render_template('followers.html', user=user, title="Followers of",
                           endpoint='.followers', pagination=pagination,
                           follows=follows)

@main.route('/followed-by/<username>')
def followed_by(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followed.paginate(
        page, per_page=current_app.config['FLASKY_FOLLOWERS_PER_PAGE'],
        error_out=False)
    follows = [{'user': item.followed, 'timestamp': item.timestamp}
               for item in pagination.items if item.followed.username!= username]

    follows=ListtoDict(follows,'num').f


    return render_template('followers.html', user=user, title="Followed by",
                           endpoint='.followed_by', pagination=pagination,
                           follows=follows)

@main.route('/all')
@login_required
def show_all():
    resp=make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed','',max_age=30*24*60*60)
    return resp
@main.route('/followed')
@login_required
def show_followed():
    resp=make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed','1',max_age=30*24*60*60)
    return resp





