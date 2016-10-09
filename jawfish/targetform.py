#from flask.ext.wtf import Form
from wtforms import Form, SelectField, StringField
from wtforms.validators import DataRequired

class TargetForm(Form):
    TARGET = StringField('TARGET', validators=[DataRequired()])
    ADDR = StringField('ADDR', validators=[DataRequired()])
    VULN_VAR = StringField('VULN_VAR', validators=[DataRequired()])
    METHOD = SelectField('METHOD', choices=[('GET', 'GET'), ('POST', 'POST')])
    GOAL_TEXT = StringField('GOAL_TEXT', validators=[DataRequired()])
