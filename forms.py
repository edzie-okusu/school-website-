from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField,SelectField
from wtforms.validators import DataRequired, URL, Length, Email, EqualTo


class NewStudentForm(FlaskForm):
    full_name = StringField("Full Name", validators=[DataRequired()])
    father_name = StringField("Father's Name", validators=[DataRequired()])
    father_contact = StringField("'Father's Number", validators=[DataRequired()])
    mother_name = StringField("Mother's name ", validators=[DataRequired()])
    mother_number = StringField("'Mother's Number", validators=[DataRequired()])
    date_of_birth = StringField("Date of Birth", validators=[DataRequired()])
    current_class = StringField("Class Registered To", validators=[DataRequired()])
    submit = SubmitField("Add Student")


class NewTeacherForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    subject = StringField('Subject', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    number = StringField('Telephone Number', validators=[DataRequired()])
    submit = SubmitField("Add Teacher")


class NewAdminForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=20)])
    subject = StringField('Your Subject', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',validators=[EqualTo('password', message='Passwords must match')])
    submit = SubmitField("Sign Me Up")


class StudentAssessmentForm(FlaskForm):
    classtest = StringField('Class Tests 20%', validators=[DataRequired()])
    midterms = StringField('MidTerms 50% ', validators=[DataRequired()])
    project_work = StringField('Project Work 30% ', validators=[DataRequired()])
    examinations = StringField('End Of Term Examination 50% ', validators=[DataRequired()])
    submit = SubmitField("Submit")


class TeacherRegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=20)])
    subject = StringField('Your Subject', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[EqualTo('password', message='Passwords must match')])
    submit = SubmitField("Sign Me Up")


class TeacherSignInForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    subject = SelectField('Your Subject', choices=[('1','mathematics'), ('2','English Language'), ('3','Integrated Science'), ('4','Social Studies'),('5', 'Computing'), ('6', 'Religious and Moral Education'), ('7', 'Creative Arts and Design'), ('8', 'Career Technology')], validators=[DataRequired()])
    submit = SubmitField('Sign-In')
