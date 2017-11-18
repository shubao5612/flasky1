from ..models import User
from flask_wtf import FlaskForm
from wtforms import SubmitField,StringField,BooleanField,PasswordField
from wtforms import ValidationError
from wtforms.validators import DataRequired,Email,Length,Regexp,EqualTo
from flask_login import current_user


class LoginForm(FlaskForm):
    email=StringField('输入你的邮箱',validators=[DataRequired(),Email(message='必须是邮箱，如1@163.com')])
    password=PasswordField('输入密码',validators=[DataRequired()])
    remember_me=BooleanField('记住我')
    submit=SubmitField('登陆')

class RegistrationForm(FlaskForm):
    email=StringField('输入你的邮箱',validators=[DataRequired(),Email(message='必须是邮箱，如1@163.com')])
    username=StringField('输入你的用户名',validators=[DataRequired(),Length(1,64)])
    password=PasswordField('输入你的密码',validators=[EqualTo('password2',message='两次密码必须输入一致'),Length(6,64,message='长度至少6位')])
    password2=PasswordField('再次输入你的密码',validators=[DataRequired()])
    submit=SubmitField('提交账户')

    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已经注册')
    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已经存在')

class Change_password(FlaskForm):
    old_p=PasswordField('输入当前密码',validators=[DataRequired()])
    new_p=PasswordField('输入新密码',validators=[DataRequired(),Length(6,64),EqualTo('new_p2',message='两次密码需要输入一致')])
    new_p2=PasswordField('再次输入密码')
    submit=SubmitField('确认修改')

class Reset_password_request(FlaskForm):
    email = StringField('输入你的邮箱', validators=[DataRequired(), Email(message='必须是邮箱，如1@163.com')])
    submit = SubmitField('确定')

class Reset_password(FlaskForm):
    email = StringField('输入你的邮箱', validators=[DataRequired(), Email(message='必须是邮箱，如1@163.com')])
    password=PasswordField('输入你的密码',validators=[EqualTo('password2',message='两次密码必须输入一致'),Length(6,64,message='长度至少6位')])
    password2=PasswordField('再次输入你的密码',validators=[DataRequired()])

    submit = SubmitField('确定')

class Reset_email_request(FlaskForm):
    email = StringField('输入你的邮箱', validators=[DataRequired(), Email(message='必须是邮箱，如1@163.com')])
    password=PasswordField('输入你的登陆密码',validators=[DataRequired()])
    submit = SubmitField('确定')

    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已经注册')

