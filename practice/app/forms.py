from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class NewSay(FlaskForm):
    name = StringField(u'标题', validators=[DataRequired('标题不能为空'), Length(1, 20)])
    body = StringField(u'内容', validators=[DataRequired("内容不能为空")])
    submit = SubmitField(u"增加")


class editsay(FlaskForm):
    name = StringField(u'标题', validators=[DataRequired('标题不能为空'), Length(1, 20)])
    body = StringField(u'内容', validators=[DataRequired("内容不能为空")])
    submit = SubmitField(u"更新")
