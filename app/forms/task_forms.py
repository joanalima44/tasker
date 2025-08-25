from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, Length

class TaskForm(FlaskForm):
    title = StringField("Título", validators=[DataRequired(), Length(min=2, max=200)])
    description = TextAreaField("Descrição")
    project_id = HiddenField("project_id")
    submit = SubmitField("Salvar")
