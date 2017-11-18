from flask import render_template,flash,redirect,url_for,request
from . import auth
from .forms import LoginForm,RegistrationForm,Change_password,Reset_password_request,Reset_password,Reset_email_request
from flask_login import  login_required,login_user,login_manager,logout_user,current_user
from ..models import User,db
from ..email import send_email


@auth.before_app_request
def before_request():

    if current_user.is_authenticated:
        #更新最后登陆的时间
        current_user.ping()
        if not current_user.confirmed \
            and request.endpoint[:5] != 'auth.' \
            and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))
@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')



@auth.route('/login',methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user,form.remember_me.data)
            print(request.args.get('next'))


            return  redirect(request.args.get('next') or url_for('main.index'))
        flash('用户名或密码错误')


    return render_template('auth/login.html',form=form)

@auth.route('/logout',methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    flash('你已经退出')
    return redirect(url_for('main.index'))
@auth.route('/register',methods=['GET','POST'])
def register():
    form=RegistrationForm()
    if form.validate_on_submit():
        user=User(email=form.email.data,
                  username=form.username.data,
                  password=form.password.data
                  )
        print(form.password.data)
        db.session.add(user)
        db.session.commit()

        token=user.genrate_confirmation()
        send_email(user.email,'账户确认','auth/email/confirm',user=user,token=token)

        flash('确认邮件已经发送到你的邮箱，请查看邮箱确认')



        return redirect(url_for('auth.login'))


    return render_template('auth/register.html',form=form)

@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        flash('你已经是正式账户，无需验证')
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('你已经确认了你的账户')
    else:
        flash('你需要确认你的账户')
    return redirect(url_for('main.index'))

@auth.route('/confirm')
@login_required
def resend_confirmation():
    token=current_user.genrate_confirmation()
    send_email(current_user.email, '账户确认', 'auth/email/confirm', user=current_user, token=token)
    flash('确认邮件已经重新发送到你的邮箱')
    return redirect(url_for('main.index'))

@auth.route('/change_password',methods=['GET','POST'])
@login_required
def change_password():
    form=Change_password()
    if form.validate_on_submit():
        if not current_user.verify_password(form.old_p.data):
            flash('旧密码输入不正确')
            return redirect(url_for('auth.change_password'))
        elif form.old_p.data ==form.new_p.data:
            flash('密码没有修改')
            return redirect(url_for('auth.change_password'))
        else:
            current_user.password=form.old_p.data
            flash('密码修改成功，请重新登陆')
            logout_user()
            return redirect(url_for('auth.login'))
        return redirect(url_for('auth.logout'))

    return render_template('auth/change_password.html',form=form)

@auth.route('/reset',methods=['GET','POST'])

def reset_password():
    form=Reset_password_request()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user is not None:
            ip = request.remote_addr
            token=user.genrate_reset()
            send_email(user.email, '账户确认', 'auth/email/reset_password', user=current_user, token=token,ip=ip)

            flash('修改密码邮件已经发送到你的邮箱')
            return redirect(url_for('main.index'))
        else:
            flash('输入的邮箱不存在，请重新输入')
            return redirect(url_for('auth.reset_password'))
    return render_template('auth/reset_password.html',form=form)

@auth.route('/reset/<token>',methods=['GET','POST'])

def reset(token):
    form=Reset_password()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user is None:
            return redirect(url_for('main.index'))
        elif user.reset(token,form.password.data):
            flash('你已经修改了你的密码,请登陆')
            return redirect(url_for('auth.login'))
        else:
            flash('没有成功')
            return redirect(url_for('main.index'))
    return render_template('auth/reset_password.html',form=form)

@auth.route('/reset_email',methods=['GET','POST'])
@login_required
def reset_email_request():
    form=Reset_email_request()
    if form.validate_on_submit():

        if current_user.verify_password(form.password.data):
            new_email=form.email.data
            token=current_user.genrate_reset_email(new_email)
            send_email(current_user.email, '更换邮箱', 'auth/email/reset_email', user=current_user, token=token)
            flash('邮件已经发送到你的邮箱')
            return redirect(url_for('main.index'))

        else:
            flash('密码错误')

    return render_template('auth/reset_email.html',form=form)

@auth.route('/reset_email/<token>',methods=['GET','POST'])
@login_required
def reset_email(token):
    if current_user.reset_email(token):
        flash('修改邮箱成功，请使用新邮箱登陆')
    else:
        flash('没有成功')
    return redirect(url_for('main.index'))







