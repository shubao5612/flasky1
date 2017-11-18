from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,TextAreaField,PasswordField,BooleanField,SelectField
from wtforms.validators import DataRequired,Length,Email
from wtforms import ValidationError
from ..models import Role,User
from flask_pagedown.fields import PageDownField

class NameForm(FlaskForm):
    name=StringField('输入你的名字？',validators=[DataRequired(message='必须输入你的名字')])
    submit=SubmitField('提交')

class EditProfileForm(FlaskForm):
    name=StringField('你的名字',validators=[Length(2,20,message='填入真实的名字')])
    location=StringField('你的地址')
    about_me=TextAreaField('个人介绍')
    submit=SubmitField('修改')


class EditProfileAdminForm(FlaskForm):
    email=StringField('邮箱',validators=[Email()])
    username=StringField('用户名',validators=[DataRequired(),Length(1,64)])
    confirmed=BooleanField('确认')

    role=SelectField('角色',coerce=int)
    name=StringField('名字')
    location=StringField('地址')
    about_me=TextAreaField('个人介绍')
    submit=SubmitField('修改')

    def __init__(self,user,*args,**kwargs):
        super(EditProfileAdminForm,self).__init__(*args,**kwargs)
        self.role.choices=[(role.id,role.name) for role in Role.query.order_by(Role.name).all()]
        self.user=user
    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')
class PostForm(FlaskForm):
    body=PageDownField('记录你的想法',validators=[DataRequired()])
    submit=SubmitField('提交')

class CommentForm(FlaskForm):
    body=StringField('评论',validators=([DataRequired()]))
    submit=SubmitField('提交')

