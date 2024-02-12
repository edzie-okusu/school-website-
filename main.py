from flask import Flask, render_template, redirect, url_for, flash, request, g, abort
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from forms import NewAdminForm, NewStudentForm, NewTeacherForm, StudentAssessmentForm, TeacherRegisterForm, \
    TeacherSignInForm
# from flask_gravatar import Gravatar
from functools import wraps
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

# connect to db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///schooldatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# add login manager
login_manager = LoginManager(app)
login_manager.init_app(app)


# table for all teaching and administrative staff who are duly registered
class User(UserMixin, db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    subject = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(250), nullable=False)


# table for all students in jhs 1-3 or grade 7-9
class JHSStudent(UserMixin, db.Model):
    __tablename__ = 'JHS Students'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(250), nullable=True)
    fathers_name = db.Column(db.String(250), nullable=True)
    fathers_contact = db.Column(db.Integer, nullable=True)
    mothers_name = db.Column(db.String(250), nullable=True)
    mothers_number = db.Column(db.Integer, nullable=True)
    date_of_birth = db.Column(db.String(250), nullable=True)
    current_class = db.Column(db.String(250), nullable=True)
    school_fees = db.Column(db.Integer, nullable=False)
    amount_paid = db.Column(db.Integer, nullable=True)
    school_fees_debt = db.Column(db.Integer, nullable=True)


# table for jhs1 class teacher or homeroom teacher
class JHS1Teacher(db.Model):
    __tablename__ = 'JHS_1_Class_Teacher'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=True)
    students = relationship('JHS1Student', back_populates='teacher')


# table for jhs1 or grade 7 students
class JHS1Student(UserMixin, db.Model):
    __tablename__ = 'JHS 1 Students'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(250), nullable=True)
    fathers_name = db.Column(db.String(250), nullable=True)
    fathers_contact = db.Column(db.Integer, nullable=True)
    mothers_name = db.Column(db.String(250), nullable=True)
    mothers_number = db.Column(db.Integer, nullable=True)
    date_of_birth = db.Column(db.String(250), nullable=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('JHS_1_Class_Teacher.id'))
    teacher = relationship('JHS1Teacher', back_populates='students')


# table for jhs2 or grade 8 homeroom teacher
class JHS2Teacher(db.Model):
    __tablename__ = 'jhs_2_class_teacher'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=True)
    students = relationship('JHS2Student', back_populates='teacher')


# table for form 2/ grade 8 students
class JHS2Student(UserMixin, db.Model):
    __tablename__ = 'JHS 2 Students'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(250), nullable=True)
    fathers_name = db.Column(db.String(250), nullable=True)
    fathers_contact = db.Column(db.Integer, nullable=True)
    mothers_name = db.Column(db.String(250), nullable=True)
    mothers_number = db.Column(db.Integer, nullable=True)
    date_of_birth = db.Column(db.String(250), nullable=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('jhs_2_class_teacher.id'))
    teacher = relationship('JHS2Teacher', back_populates='students')


# table for form 3 class teacher (or homeroom teacher)
class JHS3Teacher(db.Model):
    __tablename__ = 'jhs_3_class_teacher'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=True)
    students = relationship('JHS3Student', back_populates='teacher')


# table for JHS3 students
class JHS3Student(UserMixin, db.Model):
    __tablename__ = 'JHS 3 Students'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(250), nullable=True)
    fathers_name = db.Column(db.String(250), nullable=True)
    fathers_contact = db.Column(db.Integer, nullable=True)
    mothers_name = db.Column(db.String(250), nullable=True)
    mothers_number = db.Column(db.Integer, nullable=True)
    date_of_birth = db.Column(db.String(250), nullable=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('jhs_3_class_teacher.id'))
    teacher = relationship('JHS3Teacher', back_populates='students')


# table for all teaching staff
class Teacher(UserMixin, db.Model):
    __tablename__ = 'Teachers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=True)
    subject = db.Column(db.String(250), nullable=True)
    email = db.Column(db.String(250), nullable=True)
    number = db.Column(db.Integer, nullable=True)


# set of tables containing the assessment of students for each of the subjects taught in the school. Starts from JHS1(or Grade 7) to JHS3 (Grade 9)
class FirstTermJHS1Mathematics(UserMixin, db.Model):
    __tablename__ = 'First Term JHS 1 Mathematics Assessment'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(250), nullable=True)
    classtest = db.Column(db.Integer, nullable=True)
    midterm_examination = db.Column(db.Integer, nullable=True)
    project_work = db.Column(db.Integer, nullable=True)
    subtotal = db.Column(db.Integer, nullable=True)
    end_of_term_examination = db.Column(db.Integer, nullable=True)
    half_subtotal = db.Column(db.Integer, nullable=True)
    half_examination = db.Column(db.Integer, nullable=True)
    grand_total = db.Column(db.Integer, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('jhs_3_class_teacher.id'))
    teacher = relationship('JHS3Teacher', backref=db.backref('First Term JHS 1 Mathematics Assessment', lazy=True))


class SecondTermJHS1Mathematics(UserMixin, db.Model):
    __tablename__ = 'Second Term JHS 1 Mathematics Assessment'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(250), nullable=True)
    classtest = db.Column(db.Integer, nullable=True)
    midterm_examination = db.Column(db.Integer, nullable=True)
    project_work = db.Column(db.Integer, nullable=True)
    subtotal = db.Column(db.Integer, nullable=True)
    end_of_term_examination = db.Column(db.Integer, nullable=True)
    half_subtotal = db.Column(db.Integer, nullable=True)
    half_examination = db.Column(db.Integer, nullable=True)
    grand_total = db.Column(db.Integer, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('jhs_3_class_teacher.id'))
    teacher = relationship('JHS3Teacher', backref=db.backref('Second Term JHS 1 Mathematics Assessment', lazy=True))


class ThirdTermJHS1Mathematics(UserMixin, db.Model):
    __tablename__ = 'JHS 1 Mathematics Assessment'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(250), nullable=True)
    classtest = db.Column(db.Integer, nullable=True)
    midterm_examination = db.Column(db.Integer, nullable=True)
    project_work = db.Column(db.Integer, nullable=True)
    subtotal = db.Column(db.Integer, nullable=True)
    end_of_term_examination = db.Column(db.Integer, nullable=True)
    half_subtotal = db.Column(db.Integer, nullable=True)
    half_examination = db.Column(db.Integer, nullable=True)
    grand_total = db.Column(db.Integer, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    promoted_to_form_2 = db.Column(db.String(50), nullable=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('jhs_3_class_teacher.id'))
    teacher = relationship('JHS3Teacher', backref=db.backref('Third Term JHS 1 Mathematics Assessment', lazy=True))


class FirstTermJHS2Mathematics(UserMixin, db.Model):
    __tablename__ = 'First Term JHS 2 Mathematics Assessment'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(250), nullable=True)
    classtest = db.Column(db.Integer, nullable=True)
    midterm_examination = db.Column(db.Integer, nullable=True)
    project_work = db.Column(db.Integer, nullable=True)
    subtotal = db.Column(db.Integer, nullable=True)
    end_of_term_examination = db.Column(db.Integer, nullable=True)
    half_subtotal = db.Column(db.Integer, nullable=True)
    half_examination = db.Column(db.Integer, nullable=True)
    grand_total = db.Column(db.Integer, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('jhs_3_class_teacher.id'))
    teacher = relationship('JHS3Teacher', backref=db.backref('First Term JHS 2 Mathematics Assessment', lazy=True))


class SecondTermJHS2Mathematics(UserMixin, db.Model):
    __tablename__ = 'Second Term JHS 2 Mathematics Assessment'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(250), nullable=True)
    classtest = db.Column(db.Integer, nullable=True)
    midterm_examination = db.Column(db.Integer, nullable=True)
    project_work = db.Column(db.Integer, nullable=True)
    subtotal = db.Column(db.Integer, nullable=True)
    end_of_term_examination = db.Column(db.Integer, nullable=True)
    half_subtotal = db.Column(db.Integer, nullable=True)
    half_examination = db.Column(db.Integer, nullable=True)
    grand_total = db.Column(db.Integer, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('jhs_3_class_teacher.id'))
    teacher = relationship('JHS3Teacher', backref=db.backref('Second Term JHS 2 Mathematics Assessment', lazy=True))


class ThirdTermJHS2Mathematics(UserMixin, db.Model):
    __tablename__ = 'Third Term JHS 2 Mathematics Assessment'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(250), nullable=True)
    classtest = db.Column(db.Integer, nullable=True)
    midterm_examination = db.Column(db.Integer, nullable=True)
    project_work = db.Column(db.Integer, nullable=True)
    subtotal = db.Column(db.Integer, nullable=True)
    end_of_term_examination = db.Column(db.Integer, nullable=True)
    half_subtotal = db.Column(db.Integer, nullable=True)
    half_examination = db.Column(db.Integer, nullable=True)
    grand_total = db.Column(db.Integer, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    promoted_to_form_3 = db.Column(db.String(50), nullable=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('jhs_3_class_teacher.id'))
    teacher = relationship('JHS3Teacher', backref=db.backref('Third Term JHS 2 Mathematics Assessment', lazy=True))


class FirstTermJHS3Mathematics(UserMixin, db.Model):
    __tablename__ = 'JHS 3 Mathematics Assessment'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(250), nullable=True)
    classtest = db.Column(db.Integer, nullable=True)
    midterm_examination = db.Column(db.Integer, nullable=True)
    project_work = db.Column(db.Integer, nullable=True)
    subtotal = db.Column(db.Integer, nullable=True)
    end_of_term_examination = db.Column(db.Integer, nullable=True)
    half_subtotal = db.Column(db.Integer, nullable=True)
    half_examination = db.Column(db.Integer, nullable=True)
    grand_total = db.Column(db.Integer, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('jhs_3_class_teacher.id'))
    teacher = relationship('JHS3Teacher', backref=db.backref('First Term JHS 3 Mathematics Assessment', lazy=True))


class SecondTermJHS3Mathematics(UserMixin, db.Model):
    __tablename__ = 'Second Term JHS 3 Mathematics Assessment'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(250), nullable=True)
    classtest = db.Column(db.Integer, nullable=True)
    midterm_examination = db.Column(db.Integer, nullable=True)
    project_work = db.Column(db.Integer, nullable=True)
    subtotal = db.Column(db.Integer, nullable=True)
    end_of_term_examination = db.Column(db.Integer, nullable=True)
    half_subtotal = db.Column(db.Integer, nullable=True)
    half_examination = db.Column(db.Integer, nullable=True)
    grand_total = db.Column(db.Integer, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('jhs_3_class_teacher.id'))
    teacher = relationship('JHS3Teacher', backref=db.backref('Second Term JHS 3 Mathematics Assessment', lazy=True))


class ThirdTermJHS3Mathematics(UserMixin, db.Model):
    __tablename__ = 'Third Term JHS 3 Mathematics Assessment'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(250), nullable=True)
    classtest = db.Column(db.Integer, nullable=True)
    midterm_examination = db.Column(db.Integer, nullable=True)
    project_work = db.Column(db.Integer, nullable=True)
    subtotal = db.Column(db.Integer, nullable=True)
    end_of_term_examination = db.Column(db.Integer, nullable=True)
    half_subtotal = db.Column(db.Integer, nullable=True)
    half_examination = db.Column(db.Integer, nullable=True)
    grand_total = db.Column(db.Integer, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('jhs_3_class_teacher.id'))
    teacher = relationship('JHS3Teacher', backref=db.backref('Third Term JHS 3 Mathematics Assessment', lazy=True))


class FirstTermJHS1IntegratedScience(UserMixin, db.Model):
    __tablename__ = 'First Term JHS 1 Integrated Science Assessment'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(250), nullable=True)
    classtest = db.Column(db.Integer, nullable=True)
    midterm_examination = db.Column(db.Integer, nullable=True)
    project_work = db.Column(db.Integer, nullable=True)
    subtotal = db.Column(db.Integer, nullable=True)
    end_of_term_examination = db.Column(db.Integer, nullable=True)
    half_subtotal = db.Column(db.Integer, nullable=True)
    half_examination = db.Column(db.Integer, nullable=True)
    grand_total = db.Column(db.Integer, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('jhs_3_class_teacher.id'))
    teacher = relationship('JHS3Teacher',
                           backref=db.backref('First Term JHS 1 Integrated Science Assessment', lazy=True))


class SecondTermJHS1IntegratedScience(UserMixin, db.Model):
    __tablename__ = 'Second Term JHS 1 Integrated Science Assessment'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(250), nullable=True)
    classtest = db.Column(db.Integer, nullable=True)
    midterm_examination = db.Column(db.Integer, nullable=True)
    project_work = db.Column(db.Integer, nullable=True)
    subtotal = db.Column(db.Integer, nullable=True)
    end_of_term_examination = db.Column(db.Integer, nullable=True)
    half_subtotal = db.Column(db.Integer, nullable=True)
    half_examination = db.Column(db.Integer, nullable=True)
    grand_total = db.Column(db.Integer, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('jhs_3_class_teacher.id'))
    teacher = relationship('JHS3Teacher',
                           backref=db.backref('Second Term JHS 1 Integrated Science Assessment', lazy=True))


class ThirdTermJHS1IntegratedScience(UserMixin, db.Model):
    __tablename__ = 'Third Term JHS 1 Integrated Science Assessment'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(250), nullable=True)
    classtest = db.Column(db.Integer, nullable=True)
    midterm_examination = db.Column(db.Integer, nullable=True)
    project_work = db.Column(db.Integer, nullable=True)
    subtotal = db.Column(db.Integer, nullable=True)
    end_of_term_examination = db.Column(db.Integer, nullable=True)
    half_subtotal = db.Column(db.Integer, nullable=True)
    half_examination = db.Column(db.Integer, nullable=True)
    grand_total = db.Column(db.Integer, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('jhs_3_class_teacher.id'))
    teacher = relationship('JHS3Teacher',
                           backref=db.backref('Third Term JHS 1 Integrated Science Assessment', lazy=True))


class FirstTermJHS2IntegratedScience(UserMixin, db.Model):
    __tablename__ = 'JHS 2 Integrated Science Assessment'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(250), nullable=True)
    classtest = db.Column(db.Integer, nullable=True)
    midterm_examination = db.Column(db.Integer, nullable=True)
    project_work = db.Column(db.Integer, nullable=True)
    subtotal = db.Column(db.Integer, nullable=True)
    end_of_term_examination = db.Column(db.Integer, nullable=True)
    half_subtotal = db.Column(db.Integer, nullable=True)
    half_examination = db.Column(db.Integer, nullable=True)
    grand_total = db.Column(db.Integer, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('jhs_3_class_teacher.id'))
    teacher = relationship('JHS3Teacher',
                           backref=db.backref('First Term JHS 2 Integrated Science Assessment', lazy=True))


class SecondTermJHS2IntegratedScience(UserMixin, db.Model):
    __tablename__ = 'Second Term JHS 2 Integrated Science Assessment'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(250), nullable=True)
    classtest = db.Column(db.Integer, nullable=True)
    midterm_examination = db.Column(db.Integer, nullable=True)
    project_work = db.Column(db.Integer, nullable=True)
    subtotal = db.Column(db.Integer, nullable=True)
    end_of_term_examination = db.Column(db.Integer, nullable=True)
    half_subtotal = db.Column(db.Integer, nullable=True)
    half_examination = db.Column(db.Integer, nullable=True)
    grand_total = db.Column(db.Integer, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('jhs_3_class_teacher.id'))
    teacher = relationship('JHS3Teacher',
                           backref=db.backref('Second Term JHS 2 Integrated Science Assessment', lazy=True))


class ThirdTermJHS2IntegratedScience(UserMixin, db.Model):
    __tablename__ = 'Third Term JHS 2 Integrated Science Assessment'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(250), nullable=True)
    classtest = db.Column(db.Integer, nullable=True)
    midterm_examination = db.Column(db.Integer, nullable=True)
    project_work = db.Column(db.Integer, nullable=True)
    subtotal = db.Column(db.Integer, nullable=True)
    end_of_term_examination = db.Column(db.Integer, nullable=True)
    half_subtotal = db.Column(db.Integer, nullable=True)
    half_examination = db.Column(db.Integer, nullable=True)
    grand_total = db.Column(db.Integer, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('jhs_3_class_teacher.id'))
    teacher = relationship('JHS3Teacher',
                           backref=db.backref('Third Term JHS 2 Integrated Science Assessment', lazy=True))


class FirstTermJHS3IntegratedScience(UserMixin, db.Model):
    __tablename__ = 'First Term JHS 3 Integrated Science Assessment'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(250), nullable=True)
    classtest = db.Column(db.Integer, nullable=True)
    midterm_examination = db.Column(db.Integer, nullable=True)
    project_work = db.Column(db.Integer, nullable=True)
    subtotal = db.Column(db.Integer, nullable=True)
    end_of_term_examination = db.Column(db.Integer, nullable=True)
    half_subtotal = db.Column(db.Integer, nullable=True)
    half_examination = db.Column(db.Integer, nullable=True)
    grand_total = db.Column(db.Integer, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('jhs_3_class_teacher.id'))
    teacher = relationship('JHS3Teacher',
                           backref=db.backref('First Term JHS 3 Integrated Science Assessment', lazy=True))


class SecondTermJHS3IntegratedScience(UserMixin, db.Model):
    __tablename__ = 'Second Term JHS 3 Integrated Science Assessment'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(250), nullable=True)
    classtest = db.Column(db.Integer, nullable=True)
    midterm_examination = db.Column(db.Integer, nullable=True)
    project_work = db.Column(db.Integer, nullable=True)
    subtotal = db.Column(db.Integer, nullable=True)
    end_of_term_examination = db.Column(db.Integer, nullable=True)
    half_subtotal = db.Column(db.Integer, nullable=True)
    half_examination = db.Column(db.Integer, nullable=True)
    grand_total = db.Column(db.Integer, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('jhs_3_class_teacher.id'))
    teacher = relationship('JHS3Teacher',
                           backref=db.backref('Second Term JHS 3 Integrated Science Assessment', lazy=True))


class ThirdTermJHS3IntegratedScience(UserMixin, db.Model):
    __tablename__ = 'Third Term JHS 3 Integrated Science Assessment'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(250), nullable=True)
    classtest = db.Column(db.Integer, nullable=True)
    midterm_examination = db.Column(db.Integer, nullable=True)
    project_work = db.Column(db.Integer, nullable=True)
    subtotal = db.Column(db.Integer, nullable=True)
    end_of_term_examination = db.Column(db.Integer, nullable=True)
    half_subtotal = db.Column(db.Integer, nullable=True)
    half_examination = db.Column(db.Integer, nullable=True)
    grand_total = db.Column(db.Integer, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('jhs_3_class_teacher.id'))
    teacher = relationship('JHS3Teacher',
                           backref=db.backref('Second Term JHS 3 Integrated Science Assessment', lazy=True))


class FirstTermJHS1SocialStudies(UserMixin, db.Model):
    __tablename__ = 'First Term JHS 1 Social Studies Assessment'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(250), nullable=True)
    classtest = db.Column(db.Integer, nullable=True)
    midterm_examination = db.Column(db.Integer, nullable=True)
    project_work = db.Column(db.Integer, nullable=True)
    subtotal = db.Column(db.Integer, nullable=True)
    end_of_term_examination = db.Column(db.Integer, nullable=True)
    half_subtotal = db.Column(db.Integer, nullable=True)
    half_examination = db.Column(db.Integer, nullable=True)
    grand_total = db.Column(db.Integer, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('JHS_1_Class_Teacher.id'))
    teacher = relationship('JHS1Teacher', backref=db.backref('First Term JHS 1 Social Studies Assessment', lazy=True))


class SecondTermJHS1SocialStudies(UserMixin, db.Model):
    __tablename__ = 'Second Term JHS 1 Social Studies Assessment'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(250), nullable=True)
    classtest = db.Column(db.Integer, nullable=True)
    midterm_examination = db.Column(db.Integer, nullable=True)
    project_work = db.Column(db.Integer, nullable=True)
    subtotal = db.Column(db.Integer, nullable=True)
    end_of_term_examination = db.Column(db.Integer, nullable=True)
    half_subtotal = db.Column(db.Integer, nullable=True)
    half_examination = db.Column(db.Integer, nullable=True)
    grand_total = db.Column(db.Integer, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('JHS_1_Class_Teacher.id'))
    teacher = relationship('JHS1Teacher', backref=db.backref('Second Term JHS 1 Social Studies Assessment', lazy=True))


class ThirdTermJHS1SocialStudies(UserMixin, db.Model):
    __tablename__ = 'Third Term JHS 1 Social Studies Assessment'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(250), nullable=True)
    classtest = db.Column(db.Integer, nullable=True)
    midterm_examination = db.Column(db.Integer, nullable=True)
    project_work = db.Column(db.Integer, nullable=True)
    subtotal = db.Column(db.Integer, nullable=True)
    end_of_term_examination = db.Column(db.Integer, nullable=True)
    half_subtotal = db.Column(db.Integer, nullable=True)
    half_examination = db.Column(db.Integer, nullable=True)
    grand_total = db.Column(db.Integer, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('JHS_1_Class_Teacher.id'))
    teacher = relationship('JHS1Teacher', backref=db.backref('Third Term JHS 1 Social Studies Assessment', lazy=True))


class FirstTermJHS2SocialStudies(UserMixin, db.Model):
    __tablename__ = 'First Term JHS 2 Social Studies Assessment'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(250), nullable=True)
    classtest = db.Column(db.Integer, nullable=True)
    midterm_examination = db.Column(db.Integer, nullable=True)
    project_work = db.Column(db.Integer, nullable=True)
    subtotal = db.Column(db.Integer, nullable=True)
    end_of_term_examination = db.Column(db.Integer, nullable=True)
    half_subtotal = db.Column(db.Integer, nullable=True)
    half_examination = db.Column(db.Integer, nullable=True)
    grand_total = db.Column(db.Integer, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('JHS_1_Class_Teacher.id'))
    teacher = relationship('JHS1Teacher', backref=db.backref('First Term JHS 2 Social Studies Assessment', lazy=True))


class SecondTermJHS2SocialStudies(UserMixin, db.Model):
    __tablename__ = 'Second Term JHS 2 Social Studies Assessment'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(250), nullable=True)
    classtest = db.Column(db.Integer, nullable=True)
    midterm_examination = db.Column(db.Integer, nullable=True)
    project_work = db.Column(db.Integer, nullable=True)
    subtotal = db.Column(db.Integer, nullable=True)
    end_of_term_examination = db.Column(db.Integer, nullable=True)
    half_subtotal = db.Column(db.Integer, nullable=True)
    half_examination = db.Column(db.Integer, nullable=True)
    grand_total = db.Column(db.Integer, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('JHS_1_Class_Teacher.id'))
    teacher = relationship('JHS1Teacher', backref=db.backref('Second Term JHS 2 Social Studies Assessment', lazy=True))


class ThirdTermJHS2SocialStudies(UserMixin, db.Model):
    __tablename__ = 'Third Term JHS 2 Social Studies Assessment'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(250), nullable=True)
    classtest = db.Column(db.Integer, nullable=True)
    midterm_examination = db.Column(db.Integer, nullable=True)
    project_work = db.Column(db.Integer, nullable=True)
    subtotal = db.Column(db.Integer, nullable=True)
    end_of_term_examination = db.Column(db.Integer, nullable=True)
    half_subtotal = db.Column(db.Integer, nullable=True)
    half_examination = db.Column(db.Integer, nullable=True)
    grand_total = db.Column(db.Integer, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('JHS_1_Class_Teacher.id'))
    teacher = relationship('JHS1Teacher', backref=db.backref('Third Term JHS 2 Social Studies Assessment', lazy=True))


class FirstTermJHS3SocialStudies(UserMixin, db.Model):
    __tablename__ = 'First Term JHS 3 Social Studies Assessment'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(250), nullable=True)
    classtest = db.Column(db.Integer, nullable=True)
    midterm_examination = db.Column(db.Integer, nullable=True)
    project_work = db.Column(db.Integer, nullable=True)
    subtotal = db.Column(db.Integer, nullable=True)
    end_of_term_examination = db.Column(db.Integer, nullable=True)
    half_subtotal = db.Column(db.Integer, nullable=True)
    half_examination = db.Column(db.Integer, nullable=True)
    grand_total = db.Column(db.Integer, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('JHS_1_Class_Teacher.id'))
    teacher = relationship('JHS1Teacher', backref=db.backref('First Term JHS 3 Social Studies Assessment', lazy=True))


class SecondTermJHS3SocialStudies(UserMixin, db.Model):
    __tablename__ = 'Second Term JHS 3 Social Studies Assessment'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(250), nullable=True)
    classtest = db.Column(db.Integer, nullable=True)
    midterm_examination = db.Column(db.Integer, nullable=True)
    project_work = db.Column(db.Integer, nullable=True)
    subtotal = db.Column(db.Integer, nullable=True)
    end_of_term_examination = db.Column(db.Integer, nullable=True)
    half_subtotal = db.Column(db.Integer, nullable=True)
    half_examination = db.Column(db.Integer, nullable=True)
    grand_total = db.Column(db.Integer, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('JHS_1_Class_Teacher.id'))
    teacher = relationship('JHS1Teacher', backref=db.backref('Second Term JHS 3 Social Studies Assessment', lazy=True))


class ThirdTermJHS3SocialStudies(UserMixin, db.Model):
    __tablename__ = 'Third Term JHS 3 Social Studies Assessment'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(250), nullable=True)
    classtest = db.Column(db.Integer, nullable=True)
    midterm_examination = db.Column(db.Integer, nullable=True)
    project_work = db.Column(db.Integer, nullable=True)
    subtotal = db.Column(db.Integer, nullable=True)
    end_of_term_examination = db.Column(db.Integer, nullable=True)
    half_subtotal = db.Column(db.Integer, nullable=True)
    half_examination = db.Column(db.Integer, nullable=True)
    grand_total = db.Column(db.Integer, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('JHS_1_Class_Teacher.id'))
    teacher = relationship('JHS1Teacher', backref=db.backref('Third Term JHS 3 Social Studies Assessment', lazy=True))


class FirstTermJHS1EnglishLanguage(UserMixin, db.Model):
    __tablename__ = 'First Term JHS 1 English Language Assessment'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(250), nullable=True)
    classtest = db.Column(db.Integer, nullable=True)
    midterm_examination = db.Column(db.Integer, nullable=True)
    project_work = db.Column(db.Integer, nullable=True)
    subtotal = db.Column(db.Integer, nullable=True)
    end_of_term_examination = db.Column(db.Integer, nullable=True)
    half_subtotal = db.Column(db.Integer, nullable=True)
    half_examination = db.Column(db.Integer, nullable=True)
    grand_total = db.Column(db.Integer, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('JHS_1_Class_Teacher.id'))
    teacher = relationship('JHS1Teacher', backref=db.backref('First Term JHS 1 English Language Assessment', lazy=True))


class SecondTermJHS1EnglishLanguage(UserMixin, db.Model):
    __tablename__ = 'Second Term JHS 1 English Language Assessment'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(250), nullable=True)
    classtest = db.Column(db.Integer, nullable=True)
    midterm_examination = db.Column(db.Integer, nullable=True)
    project_work = db.Column(db.Integer, nullable=True)
    subtotal = db.Column(db.Integer, nullable=True)
    end_of_term_examination = db.Column(db.Integer, nullable=True)
    half_subtotal = db.Column(db.Integer, nullable=True)
    half_examination = db.Column(db.Integer, nullable=True)
    grand_total = db.Column(db.Integer, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('JHS_1_Class_Teacher.id'))
    teacher = relationship('JHS1Teacher',
                           backref=db.backref('Second Term JHS 1 English Language Assessment', lazy=True))


class ThirdTermJHS1EnglishLanguage(UserMixin, db.Model):
    __tablename__ = 'Third Term JHS 1 English Language Assessment'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(250), nullable=True)
    classtest = db.Column(db.Integer, nullable=True)
    midterm_examination = db.Column(db.Integer, nullable=True)
    project_work = db.Column(db.Integer, nullable=True)
    subtotal = db.Column(db.Integer, nullable=True)
    end_of_term_examination = db.Column(db.Integer, nullable=True)
    half_subtotal = db.Column(db.Integer, nullable=True)
    half_examination = db.Column(db.Integer, nullable=True)
    grand_total = db.Column(db.Integer, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('JHS_1_Class_Teacher.id'))
    teacher = relationship('JHS1Teacher', backref=db.backref('Third Term JHS 1 English Language Assessment', lazy=True))


class FirstTermJHS2EnglishLanguage(UserMixin, db.Model):
    __tablename__ = 'First Term JHS 2 English Language Assessment'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(250), nullable=True)
    classtest = db.Column(db.Integer, nullable=True)
    midterm_examination = db.Column(db.Integer, nullable=True)
    project_work = db.Column(db.Integer, nullable=True)
    subtotal = db.Column(db.Integer, nullable=True)
    end_of_term_examination = db.Column(db.Integer, nullable=True)
    half_subtotal = db.Column(db.Integer, nullable=True)
    half_examination = db.Column(db.Integer, nullable=True)
    grand_total = db.Column(db.Integer, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('JHS_1_Class_Teacher.id'))
    teacher = relationship('JHS1Teacher', backref=db.backref('First Term JHS 2 English Language Assessment', lazy=True))


class SecondTermJHS2EnglishLanguage(UserMixin, db.Model):
    __tablename__ = 'Second Term JHS 2 English Language Assessment'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(250), nullable=True)
    classtest = db.Column(db.Integer, nullable=True)
    midterm_examination = db.Column(db.Integer, nullable=True)
    project_work = db.Column(db.Integer, nullable=True)
    subtotal = db.Column(db.Integer, nullable=True)
    end_of_term_examination = db.Column(db.Integer, nullable=True)
    half_subtotal = db.Column(db.Integer, nullable=True)
    half_examination = db.Column(db.Integer, nullable=True)
    grand_total = db.Column(db.Integer, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('JHS_1_Class_Teacher.id'))
    teacher = relationship('JHS1Teacher',
                           backref=db.backref('Second Term JHS 2 English Language Assessment', lazy=True))


class ThirdTermJHS2EnglishLanguage(UserMixin, db.Model):
    __tablename__ = 'Third Term JHS 2 English Language Assessment'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(250), nullable=True)
    classtest = db.Column(db.Integer, nullable=True)
    midterm_examination = db.Column(db.Integer, nullable=True)
    project_work = db.Column(db.Integer, nullable=True)
    subtotal = db.Column(db.Integer, nullable=True)
    end_of_term_examination = db.Column(db.Integer, nullable=True)
    half_subtotal = db.Column(db.Integer, nullable=True)
    half_examination = db.Column(db.Integer, nullable=True)
    grand_total = db.Column(db.Integer, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('JHS_1_Class_Teacher.id'))
    teacher = relationship('JHS1Teacher', backref=db.backref('Third Term JHS 2 English Language Assessment', lazy=True))


class FirstTermJHS3EnglishLanguage(UserMixin, db.Model):
    __tablename__ = 'First Term JHS 3 English Language Assessment'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(250), nullable=True)
    classtest = db.Column(db.Integer, nullable=True)
    midterm_examination = db.Column(db.Integer, nullable=True)
    project_work = db.Column(db.Integer, nullable=True)
    subtotal = db.Column(db.Integer, nullable=True)
    end_of_term_examination = db.Column(db.Integer, nullable=True)
    half_subtotal = db.Column(db.Integer, nullable=True)
    half_examination = db.Column(db.Integer, nullable=True)
    grand_total = db.Column(db.Integer, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('JHS_1_Class_Teacher.id'))
    teacher = relationship('JHS1Teacher', backref=db.backref('First Term JHS 3 English Language Assessment', lazy=True))


class SecondTermJHS3EnglishLanguage(UserMixin, db.Model):
    __tablename__ = 'Second Term JHS 3 English Language Assessment'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(250), nullable=True)
    classtest = db.Column(db.Integer, nullable=True)
    midterm_examination = db.Column(db.Integer, nullable=True)
    project_work = db.Column(db.Integer, nullable=True)
    subtotal = db.Column(db.Integer, nullable=True)
    end_of_term_examination = db.Column(db.Integer, nullable=True)
    half_subtotal = db.Column(db.Integer, nullable=True)
    half_examination = db.Column(db.Integer, nullable=True)
    grand_total = db.Column(db.Integer, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('JHS_1_Class_Teacher.id'))
    teacher = relationship('JHS1Teacher',
                           backref=db.backref('Second Term JHS 3 English Language Assessment', lazy=True))


class ThirdTermJHS3EnglishLanguage(UserMixin, db.Model):
    __tablename__ = 'Third Term JHS 3 English Language Assessment'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(250), nullable=True)
    classtest = db.Column(db.Integer, nullable=True)
    midterm_examination = db.Column(db.Integer, nullable=True)
    project_work = db.Column(db.Integer, nullable=True)
    subtotal = db.Column(db.Integer, nullable=True)
    end_of_term_examination = db.Column(db.Integer, nullable=True)
    half_subtotal = db.Column(db.Integer, nullable=True)
    half_examination = db.Column(db.Integer, nullable=True)
    grand_total = db.Column(db.Integer, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('JHS_1_Class_Teacher.id'))
    teacher = relationship('JHS1Teacher', backref=db.backref('Third Term JHS 3 English Language Assessment', lazy=True))


class FirstTermJHS1Computing(UserMixin, db.Model):
    __tablename__ = 'First Term JHS 1 Computing'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(250), nullable=True)
    classtest = db.Column(db.Integer, nullable=True)
    midterm_examination = db.Column(db.Integer, nullable=True)
    project_work = db.Column(db.Integer, nullable=True)
    subtotal = db.Column(db.Integer, nullable=True)
    end_of_term_examination = db.Column(db.Integer, nullable=True)
    half_subtotal = db.Column(db.Integer, nullable=True)
    half_examination = db.Column(db.Integer, nullable=True)
    grand_total = db.Column(db.Integer, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('jhs_2_class_teacher.id'))
    teacher = relationship('JHS2Teacher', backref=db.backref('First Term JHS 1 Computing', lazy=True))


class SecondTermJHS1Computing(UserMixin, db.Model):
    __tablename__ = 'Second Term JHS 1 Computing'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(250), nullable=True)
    classtest = db.Column(db.Integer, nullable=True)
    midterm_examination = db.Column(db.Integer, nullable=True)
    project_work = db.Column(db.Integer, nullable=True)
    subtotal = db.Column(db.Integer, nullable=True)
    end_of_term_examination = db.Column(db.Integer, nullable=True)
    half_subtotal = db.Column(db.Integer, nullable=True)
    half_examination = db.Column(db.Integer, nullable=True)
    grand_total = db.Column(db.Integer, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('jhs_2_class_teacher.id'))
    teacher = relationship('JHS2Teacher', backref=db.backref('Second Term JHS 1 Computing', lazy=True))


class ThirdTermJHS1Computing(UserMixin, db.Model):
    __tablename__ = 'Third Term JHS 1 Computing'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(250), nullable=True)
    classtest = db.Column(db.Integer, nullable=True)
    midterm_examination = db.Column(db.Integer, nullable=True)
    project_work = db.Column(db.Integer, nullable=True)
    subtotal = db.Column(db.Integer, nullable=True)
    end_of_term_examination = db.Column(db.Integer, nullable=True)
    half_subtotal = db.Column(db.Integer, nullable=True)
    half_examination = db.Column(db.Integer, nullable=True)
    grand_total = db.Column(db.Integer, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('jhs_2_class_teacher.id'))
    teacher = relationship('JHS2Teacher', backref=db.backref('Third Term JHS 1 Computing', lazy=True))


class FirstTermJHS2Computing(UserMixin, db.Model):
    __tablename__ = 'First Term JHS 2 Computing'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(250), nullable=True)
    classtest = db.Column(db.Integer, nullable=True)
    midterm_examination = db.Column(db.Integer, nullable=True)
    project_work = db.Column(db.Integer, nullable=True)
    subtotal = db.Column(db.Integer, nullable=True)
    end_of_term_examination = db.Column(db.Integer, nullable=True)
    half_subtotal = db.Column(db.Integer, nullable=True)
    half_examination = db.Column(db.Integer, nullable=True)
    grand_total = db.Column(db.Integer, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('jhs_2_class_teacher.id'))
    teacher = relationship('JHS2Teacher', backref=db.backref('First Term JHS 2 Computing', lazy=True))


class SecondTermJHS2Computing(UserMixin, db.Model):
    __tablename__ = 'Second Term JHS 2 Computing'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(250), nullable=True)
    classtest = db.Column(db.Integer, nullable=True)
    midterm_examination = db.Column(db.Integer, nullable=True)
    project_work = db.Column(db.Integer, nullable=True)
    subtotal = db.Column(db.Integer, nullable=True)
    end_of_term_examination = db.Column(db.Integer, nullable=True)
    half_subtotal = db.Column(db.Integer, nullable=True)
    half_examination = db.Column(db.Integer, nullable=True)
    grand_total = db.Column(db.Integer, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('jhs_2_class_teacher.id'))
    teacher = relationship('JHS2Teacher', backref=db.backref('Second Term JHS 2 Computing', lazy=True))


class ThirdTermJHS2Computing(UserMixin, db.Model):
    __tablename__ = 'Third Term JHS 2 Computing'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(250), nullable=True)
    classtest = db.Column(db.Integer, nullable=True)
    midterm_examination = db.Column(db.Integer, nullable=True)
    project_work = db.Column(db.Integer, nullable=True)
    subtotal = db.Column(db.Integer, nullable=True)
    end_of_term_examination = db.Column(db.Integer, nullable=True)
    half_subtotal = db.Column(db.Integer, nullable=True)
    half_examination = db.Column(db.Integer, nullable=True)
    grand_total = db.Column(db.Integer, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('jhs_2_class_teacher.id'))
    teacher = relationship('JHS2Teacher', backref=db.backref('Third Term JHS 2 Computing', lazy=True))


class FirstTermJHS3Computing(UserMixin, db.Model):
    __tablename__ = 'First Term JHS 3 Computing'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(250), nullable=True)
    classtest = db.Column(db.Integer, nullable=True)
    midterm_examination = db.Column(db.Integer, nullable=True)
    project_work = db.Column(db.Integer, nullable=True)
    subtotal = db.Column(db.Integer, nullable=True)
    end_of_term_examination = db.Column(db.Integer, nullable=True)
    half_subtotal = db.Column(db.Integer, nullable=True)
    half_examination = db.Column(db.Integer, nullable=True)
    grand_total = db.Column(db.Integer, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('jhs_2_class_teacher.id'))
    teacher = relationship('JHS2Teacher', backref=db.backref('First Term JHS 3 Computing', lazy=True))


class SecondTermJHS3Computing(UserMixin, db.Model):
    __tablename__ = 'Second Term JHS 3 Computing'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(250), nullable=True)
    classtest = db.Column(db.Integer, nullable=True)
    midterm_examination = db.Column(db.Integer, nullable=True)
    project_work = db.Column(db.Integer, nullable=True)
    subtotal = db.Column(db.Integer, nullable=True)
    end_of_term_examination = db.Column(db.Integer, nullable=True)
    half_subtotal = db.Column(db.Integer, nullable=True)
    half_examination = db.Column(db.Integer, nullable=True)
    grand_total = db.Column(db.Integer, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('jhs_2_class_teacher.id'))
    teacher = relationship('JHS2Teacher', backref=db.backref('Second Term JHS 3 Computing', lazy=True))


class ThirdTermJHS3Computing(UserMixin, db.Model):
    __tablename__ = 'Third Term JHS 3 Computing'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(250), nullable=True)
    classtest = db.Column(db.Integer, nullable=True)
    midterm_examination = db.Column(db.Integer, nullable=True)
    project_work = db.Column(db.Integer, nullable=True)
    subtotal = db.Column(db.Integer, nullable=True)
    end_of_term_examination = db.Column(db.Integer, nullable=True)
    half_subtotal = db.Column(db.Integer, nullable=True)
    half_examination = db.Column(db.Integer, nullable=True)
    grand_total = db.Column(db.Integer, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('jhs_2_class_teacher.id'))
    teacher = relationship('JHS2Teacher', backref=db.backref('Third Term JHS 3 Computing', lazy=True))


class FirstTermJHS1ReligiousMoralEducation(UserMixin, db.Model):
    __tablename__ = 'First Term JHS 1 RME Assessment'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(250), nullable=True)
    classtest = db.Column(db.Integer, nullable=True)
    midterm_examination = db.Column(db.Integer, nullable=True)
    project_work = db.Column(db.Integer, nullable=True)
    subtotal = db.Column(db.Integer, nullable=True)
    end_of_term_examination = db.Column(db.Integer, nullable=True)
    half_subtotal = db.Column(db.Integer, nullable=True)
    half_examination = db.Column(db.Integer, nullable=True)
    grand_total = db.Column(db.Integer, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('jhs_2_class_teacher.id'))
    teacher = relationship('JHS2Teacher', backref=db.backref('First Term JHS 1 RME Assessment', lazy=True))


class SecondTermJHS1ReligiousMoralEducation(UserMixin, db.Model):
    __tablename__ = 'Second Term JHS 1 RME Assessment'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(250), nullable=True)
    classtest = db.Column(db.Integer, nullable=True)
    midterm_examination = db.Column(db.Integer, nullable=True)
    project_work = db.Column(db.Integer, nullable=True)
    subtotal = db.Column(db.Integer, nullable=True)
    end_of_term_examination = db.Column(db.Integer, nullable=True)
    half_subtotal = db.Column(db.Integer, nullable=True)
    half_examination = db.Column(db.Integer, nullable=True)
    grand_total = db.Column(db.Integer, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('jhs_2_class_teacher.id'))
    teacher = relationship('JHS2Teacher', backref=db.backref('Second Term JHS 1 RME Assessment', lazy=True))


class ThirdTermJHS1ReligiousMoralEducation(UserMixin, db.Model):
    __tablename__ = 'Third Term JHS 1 RME Assessment'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(250), nullable=True)
    classtest = db.Column(db.Integer, nullable=True)
    midterm_examination = db.Column(db.Integer, nullable=True)
    project_work = db.Column(db.Integer, nullable=True)
    subtotal = db.Column(db.Integer, nullable=True)
    end_of_term_examination = db.Column(db.Integer, nullable=True)
    half_subtotal = db.Column(db.Integer, nullable=True)
    half_examination = db.Column(db.Integer, nullable=True)
    grand_total = db.Column(db.Integer, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('jhs_2_class_teacher.id'))
    teacher = relationship('JHS2Teacher', backref=db.backref('Third Term JHS 1 RME Assessment', lazy=True))


class FirstTermJHS2ReligiousMoralEducation(UserMixin, db.Model):
    __tablename__ = 'First Term JHS 2 RME Assessment'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(250), nullable=True)
    classtest = db.Column(db.Integer, nullable=True)
    midterm_examination = db.Column(db.Integer, nullable=True)
    project_work = db.Column(db.Integer, nullable=True)
    subtotal = db.Column(db.Integer, nullable=True)
    end_of_term_examination = db.Column(db.Integer, nullable=True)
    half_subtotal = db.Column(db.Integer, nullable=True)
    half_examination = db.Column(db.Integer, nullable=True)
    grand_total = db.Column(db.Integer, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('jhs_2_class_teacher.id'))
    teacher = relationship('JHS2Teacher', backref=db.backref('First Term JHS 2 RME Assessment', lazy=True))


class SecondTermJHS2ReligiousMoralEducation(UserMixin, db.Model):
    __tablename__ = 'Second Term JHS 2 RME Assessment'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(250), nullable=True)
    classtest = db.Column(db.Integer, nullable=True)
    midterm_examination = db.Column(db.Integer, nullable=True)
    project_work = db.Column(db.Integer, nullable=True)
    subtotal = db.Column(db.Integer, nullable=True)
    end_of_term_examination = db.Column(db.Integer, nullable=True)
    half_subtotal = db.Column(db.Integer, nullable=True)
    half_examination = db.Column(db.Integer, nullable=True)
    grand_total = db.Column(db.Integer, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('jhs_2_class_teacher.id'))
    teacher = relationship('JHS2Teacher', backref=db.backref('Second Term JHS 2 RME Assessment', lazy=True))


class ThirdTermJHS2ReligiousMoralEducation(UserMixin, db.Model):
    __tablename__ = 'Third Term JHS 2 RME Assessment'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(250), nullable=True)
    classtest = db.Column(db.Integer, nullable=True)
    midterm_examination = db.Column(db.Integer, nullable=True)
    project_work = db.Column(db.Integer, nullable=True)
    subtotal = db.Column(db.Integer, nullable=True)
    end_of_term_examination = db.Column(db.Integer, nullable=True)
    half_subtotal = db.Column(db.Integer, nullable=True)
    half_examination = db.Column(db.Integer, nullable=True)
    grand_total = db.Column(db.Integer, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('jhs_2_class_teacher.id'))
    teacher = relationship('JHS2Teacher', backref=db.backref('Third Term JHS 2 RME Assessment', lazy=True))


class FirstTermJHS3ReligiousMoralEducation(UserMixin, db.Model):
    __tablename__ = 'First Term JHS 3 RME Assessment'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(250), nullable=True)
    classtest = db.Column(db.Integer, nullable=True)
    midterm_examination = db.Column(db.Integer, nullable=True)
    project_work = db.Column(db.Integer, nullable=True)
    subtotal = db.Column(db.Integer, nullable=True)
    end_of_term_examination = db.Column(db.Integer, nullable=True)
    half_subtotal = db.Column(db.Integer, nullable=True)
    half_examination = db.Column(db.Integer, nullable=True)
    grand_total = db.Column(db.Integer, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('jhs_2_class_teacher.id'))
    teacher = relationship('JHS2Teacher', backref=db.backref('First Term JHS 3 RME Assessment', lazy=True))


class SecondTermJHS3ReligiousMoralEducation(UserMixin, db.Model):
    __tablename__ = 'Second Term JHS 3 RME Assessment'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(250), nullable=True)
    classtest = db.Column(db.Integer, nullable=True)
    midterm_examination = db.Column(db.Integer, nullable=True)
    project_work = db.Column(db.Integer, nullable=True)
    subtotal = db.Column(db.Integer, nullable=True)
    end_of_term_examination = db.Column(db.Integer, nullable=True)
    half_subtotal = db.Column(db.Integer, nullable=True)
    half_examination = db.Column(db.Integer, nullable=True)
    grand_total = db.Column(db.Integer, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('jhs_2_class_teacher.id'))
    teacher = relationship('JHS2Teacher', backref=db.backref('Second Term JHS 3 RME Assessment', lazy=True))


class ThirdTermJHS3ReligiousMoralEducation(UserMixin, db.Model):
    __tablename__ = 'Third Term JHS 3 RME Assessment'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(250), nullable=True)
    classtest = db.Column(db.Integer, nullable=True)
    midterm_examination = db.Column(db.Integer, nullable=True)
    project_work = db.Column(db.Integer, nullable=True)
    subtotal = db.Column(db.Integer, nullable=True)
    end_of_term_examination = db.Column(db.Integer, nullable=True)
    half_subtotal = db.Column(db.Integer, nullable=True)
    half_examination = db.Column(db.Integer, nullable=True)
    grand_total = db.Column(db.Integer, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('jhs_2_class_teacher.id'))
    teacher = relationship('JHS2Teacher', backref=db.backref('Third Term JHS 3 RME Assessment', lazy=True))


class FirstTermJHS1CareerTechnology(UserMixin, db.Model):
    __tablename__ = 'First TermJHS 1 Career Technology Assessment'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(250), nullable=True)
    classtest = db.Column(db.Integer, nullable=True)
    midterm_examination = db.Column(db.Integer, nullable=True)
    project_work = db.Column(db.Integer, nullable=True)
    subtotal = db.Column(db.Integer, nullable=True)
    end_of_term_examination = db.Column(db.Integer, nullable=True)
    half_subtotal = db.Column(db.Integer, nullable=True)
    half_examination = db.Column(db.Integer, nullable=True)
    grand_total = db.Column(db.Integer, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)


class SecondTermJHS1CareerTechnology(UserMixin, db.Model):
    __tablename__ = 'Second Term JHS 1 Career Technology Assessment'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(250), nullable=True)
    classtest = db.Column(db.Integer, nullable=True)
    midterm_examination = db.Column(db.Integer, nullable=True)
    project_work = db.Column(db.Integer, nullable=True)
    subtotal = db.Column(db.Integer, nullable=True)
    end_of_term_examination = db.Column(db.Integer, nullable=True)
    half_subtotal = db.Column(db.Integer, nullable=True)
    half_examination = db.Column(db.Integer, nullable=True)
    grand_total = db.Column(db.Integer, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)


class ThirdTermJHS1CareerTechnology(UserMixin, db.Model):
    __tablename__ = 'Third Term JHS 1 Career Technology Assessment'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(250), nullable=True)
    classtest = db.Column(db.Integer, nullable=True)
    midterm_examination = db.Column(db.Integer, nullable=True)
    project_work = db.Column(db.Integer, nullable=True)
    subtotal = db.Column(db.Integer, nullable=True)
    end_of_term_examination = db.Column(db.Integer, nullable=True)
    half_subtotal = db.Column(db.Integer, nullable=True)
    half_examination = db.Column(db.Integer, nullable=True)
    grand_total = db.Column(db.Integer, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)


class FirstTermJHS2CareerTechnology(UserMixin, db.Model):
    __tablename__ = 'First Term JHS 2 Career Technology Assessment'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(250), nullable=True)
    classtest = db.Column(db.Integer, nullable=True)
    midterm_examination = db.Column(db.Integer, nullable=True)
    project_work = db.Column(db.Integer, nullable=True)
    subtotal = db.Column(db.Integer, nullable=True)
    end_of_term_examination = db.Column(db.Integer, nullable=True)
    half_subtotal = db.Column(db.Integer, nullable=True)
    half_examination = db.Column(db.Integer, nullable=True)
    grand_total = db.Column(db.Integer, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)


class SecondTermJHS2CareerTechnology(UserMixin, db.Model):
    __tablename__ = 'Second Term JHS 2 Career Technology Assessment'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(250), nullable=True)
    classtest = db.Column(db.Integer, nullable=True)
    midterm_examination = db.Column(db.Integer, nullable=True)
    project_work = db.Column(db.Integer, nullable=True)
    subtotal = db.Column(db.Integer, nullable=True)
    end_of_term_examination = db.Column(db.Integer, nullable=True)
    half_subtotal = db.Column(db.Integer, nullable=True)
    half_examination = db.Column(db.Integer, nullable=True)
    grand_total = db.Column(db.Integer, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)


class ThirdTermJHS2CareerTechnology(UserMixin, db.Model):
    __tablename__ = 'Third Term JHS 2 Career Technology Assessment'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(250), nullable=True)
    classtest = db.Column(db.Integer, nullable=True)
    midterm_examination = db.Column(db.Integer, nullable=True)
    project_work = db.Column(db.Integer, nullable=True)
    subtotal = db.Column(db.Integer, nullable=True)
    end_of_term_examination = db.Column(db.Integer, nullable=True)
    half_subtotal = db.Column(db.Integer, nullable=True)
    half_examination = db.Column(db.Integer, nullable=True)
    grand_total = db.Column(db.Integer, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)


class FirstTermJHS3CareerTechnology(UserMixin, db.Model):
    __tablename__ = 'First Term JHS 3 Career Technology Assessment'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(250), nullable=True)
    classtest = db.Column(db.Integer, nullable=True)
    midterm_examination = db.Column(db.Integer, nullable=True)
    project_work = db.Column(db.Integer, nullable=True)
    subtotal = db.Column(db.Integer, nullable=True)
    end_of_term_examination = db.Column(db.Integer, nullable=True)
    half_subtotal = db.Column(db.Integer, nullable=True)
    half_examination = db.Column(db.Integer, nullable=True)
    grand_total = db.Column(db.Integer, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)


class SecondTermJHS3CareerTechnology(UserMixin, db.Model):
    __tablename__ = 'Second Term JHS 3 Career Technology Assessment'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(250), nullable=True)
    classtest = db.Column(db.Integer, nullable=True)
    midterm_examination = db.Column(db.Integer, nullable=True)
    project_work = db.Column(db.Integer, nullable=True)
    subtotal = db.Column(db.Integer, nullable=True)
    end_of_term_examination = db.Column(db.Integer, nullable=True)
    half_subtotal = db.Column(db.Integer, nullable=True)
    half_examination = db.Column(db.Integer, nullable=True)
    grand_total = db.Column(db.Integer, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)


class ThirdTermJHS3CareerTechnology(UserMixin, db.Model):
    __tablename__ = 'Third Term JHS 3 Career Technology Assessment'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(250), nullable=True)
    classtest = db.Column(db.Integer, nullable=True)
    midterm_examination = db.Column(db.Integer, nullable=True)
    project_work = db.Column(db.Integer, nullable=True)
    subtotal = db.Column(db.Integer, nullable=True)
    end_of_term_examination = db.Column(db.Integer, nullable=True)
    half_subtotal = db.Column(db.Integer, nullable=True)
    half_examination = db.Column(db.Integer, nullable=True)
    grand_total = db.Column(db.Integer, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)


class FirstTermJHS1CreativeArtsAndDesign(UserMixin, db.Model):
    __tablename__ = 'First Term JHS 1 Creative Arts and Design'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(250), nullable=True)
    classtest = db.Column(db.Integer, nullable=True)
    midterm_examination = db.Column(db.Integer, nullable=True)
    project_work = db.Column(db.Integer, nullable=True)
    subtotal = db.Column(db.Integer, nullable=True)
    end_of_term_examination = db.Column(db.Integer, nullable=True)
    half_subtotal = db.Column(db.Integer, nullable=True)
    half_examination = db.Column(db.Integer, nullable=True)
    grand_total = db.Column(db.Integer, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)


class SecondTermJHS1CreativeArtsAndDesign(UserMixin, db.Model):
    __tablename__ = 'Second Term JHS 1 Creative Arts and Design'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(250), nullable=True)
    classtest = db.Column(db.Integer, nullable=True)
    midterm_examination = db.Column(db.Integer, nullable=True)
    project_work = db.Column(db.Integer, nullable=True)
    subtotal = db.Column(db.Integer, nullable=True)
    end_of_term_examination = db.Column(db.Integer, nullable=True)
    half_subtotal = db.Column(db.Integer, nullable=True)
    half_examination = db.Column(db.Integer, nullable=True)
    grand_total = db.Column(db.Integer, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)


class ThirdTermJHS1CreativeArtsAndDesign(UserMixin, db.Model):
    __tablename__ = 'Third Term JHS 1 Creative Arts and Design'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(250), nullable=True)
    classtest = db.Column(db.Integer, nullable=True)
    midterm_examination = db.Column(db.Integer, nullable=True)
    project_work = db.Column(db.Integer, nullable=True)
    subtotal = db.Column(db.Integer, nullable=True)
    end_of_term_examination = db.Column(db.Integer, nullable=True)
    half_subtotal = db.Column(db.Integer, nullable=True)
    half_examination = db.Column(db.Integer, nullable=True)
    grand_total = db.Column(db.Integer, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)


class FirstTermJHS2CreativeArtsAndDesign(UserMixin, db.Model):
    __tablename__ = 'First Term JHS 2 Creative Arts and Design'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(250), nullable=True)
    classtest = db.Column(db.Integer, nullable=True)
    midterm_examination = db.Column(db.Integer, nullable=True)
    project_work = db.Column(db.Integer, nullable=True)
    subtotal = db.Column(db.Integer, nullable=True)
    end_of_term_examination = db.Column(db.Integer, nullable=True)
    half_subtotal = db.Column(db.Integer, nullable=True)
    half_examination = db.Column(db.Integer, nullable=True)
    grand_total = db.Column(db.Integer, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)


class SecondTermJHS2CreativeArtsAndDesign(UserMixin, db.Model):
    __tablename__ = 'Second Term JHS 2 Creative Arts and Design'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(250), nullable=True)
    classtest = db.Column(db.Integer, nullable=True)
    midterm_examination = db.Column(db.Integer, nullable=True)
    project_work = db.Column(db.Integer, nullable=True)
    subtotal = db.Column(db.Integer, nullable=True)
    end_of_term_examination = db.Column(db.Integer, nullable=True)
    half_subtotal = db.Column(db.Integer, nullable=True)
    half_examination = db.Column(db.Integer, nullable=True)
    grand_total = db.Column(db.Integer, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)


class ThirdTermJHS2CreativeArtsAndDesign(UserMixin, db.Model):
    __tablename__ = 'Third Term JHS 2 Creative Arts and Design'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(250), nullable=True)
    classtest = db.Column(db.Integer, nullable=True)
    midterm_examination = db.Column(db.Integer, nullable=True)
    project_work = db.Column(db.Integer, nullable=True)
    subtotal = db.Column(db.Integer, nullable=True)
    end_of_term_examination = db.Column(db.Integer, nullable=True)
    half_subtotal = db.Column(db.Integer, nullable=True)
    half_examination = db.Column(db.Integer, nullable=True)
    grand_total = db.Column(db.Integer, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)


class FirstTermJHS3CreativeArtsAndDesign(UserMixin, db.Model):
    __tablename__ = 'First Term JHS 3 Creative Arts and Design'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(250), nullable=True)
    classtest = db.Column(db.Integer, nullable=True)
    midterm_examination = db.Column(db.Integer, nullable=True)
    project_work = db.Column(db.Integer, nullable=True)
    subtotal = db.Column(db.Integer, nullable=True)
    end_of_term_examination = db.Column(db.Integer, nullable=True)
    half_subtotal = db.Column(db.Integer, nullable=True)
    half_examination = db.Column(db.Integer, nullable=True)
    grand_total = db.Column(db.Integer, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)


class SecondTermJHS3CreativeArtsAndDesign(UserMixin, db.Model):
    __tablename__ = 'Second Term JHS 3 Creative Arts and Design'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(250), nullable=True)
    classtest = db.Column(db.Integer, nullable=True)
    midterm_examination = db.Column(db.Integer, nullable=True)
    project_work = db.Column(db.Integer, nullable=True)
    subtotal = db.Column(db.Integer, nullable=True)
    end_of_term_examination = db.Column(db.Integer, nullable=True)
    half_subtotal = db.Column(db.Integer, nullable=True)
    half_examination = db.Column(db.Integer, nullable=True)
    grand_total = db.Column(db.Integer, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)


class ThirdTermJHS3CreativeArtsAndDesign(UserMixin, db.Model):
    __tablename__ = 'Third Term JHS 3 Creative Arts and Design'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(250), nullable=True)
    classtest = db.Column(db.Integer, nullable=True)
    midterm_examination = db.Column(db.Integer, nullable=True)
    project_work = db.Column(db.Integer, nullable=True)
    subtotal = db.Column(db.Integer, nullable=True)
    end_of_term_examination = db.Column(db.Integer, nullable=True)
    half_subtotal = db.Column(db.Integer, nullable=True)
    half_examination = db.Column(db.Integer, nullable=True)
    grand_total = db.Column(db.Integer, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)


# user app_context to create db and populate relevant data tables with data
with app.app_context():
    db.create_all()
    jhs1_students = JHSStudent.query.filter_by(current_class=7).all()
    jhs2_students = JHSStudent.query.filter_by(current_class=8).all()
    jhs3_students = JHSStudent.query.filter_by(current_class=9).all()

    # populate student into various class tables depending on their class from the main students table(i.e JHSStudent)
    for student in jhs1_students:
        check_student = JHS1Student.query.filter_by(full_name=student.full_name).first()
        if check_student:
            pass
        else:
            jhs1_student = JHS1Student(
                full_name=student.full_name,
                fathers_name=student.fathers_name,
                fathers_contact=student.fathers_contact,
                mothers_name=student.mothers_name,
                mothers_number=student.mothers_number,
                date_of_birth=student.date_of_birth
            )
            db.session.add(jhs1_student)
            check_maths = FirstTermJHS1Mathematics.query.filter_by(full_name=student.full_name).first()
            if not check_maths:
                first_term_maths = FirstTermJHS1Mathematics(
                    full_name=student.full_name
                )
                second_term_maths = SecondTermJHS1Mathematics(
                    full_name=student.full_name
                )
                third_term_maths = ThirdTermJHS1Mathematics(
                    full_name=student.full_name
                )
                db.session.add(first_term_maths)
                db.session.add(second_term_maths)
                db.session.add(third_term_maths)
                db.session.commit()

            check_english = FirstTermJHS1EnglishLanguage.query.filter_by(full_name=student.full_name).first()
            if not check_english:
                first_term = FirstTermJHS1EnglishLanguage(
                    full_name=student.full_name
                )
                second_term = SecondTermJHS1EnglishLanguage(
                    full_name=student.full_name
                )
                third_term = ThirdTermJHS1EnglishLanguage(
                    full_name=student.full_name
                )
                db.session.add(first_term)
                db.session.add(second_term)
                db.session.add(third_term)
                db.session.commit()

            check_science = FirstTermJHS1IntegratedScience.query.filter_by(full_name=student.full_name).first()
            if not check_science:
                first_term = FirstTermJHS1IntegratedScience(
                    full_name=student.full_name
                )
                second_term = SecondTermJHS1IntegratedScience(
                    full_name=student.full_name
                )
                third_term = ThirdTermJHS1IntegratedScience(
                    full_name=student.full_name
                )
                db.session.add(first_term)
                db.session.add(second_term)
                db.session.add(third_term)
                db.session.commit()

            check_social = FirstTermJHS1SocialStudies.query.filter_by(full_name=student.full_name).first()
            if not check_social:
                first_term = FirstTermJHS1SocialStudies(
                    full_name=student.full_name
                )
                second_term = SecondTermJHS1SocialStudies(
                    full_name=student.full_name
                )
                third_term = ThirdTermJHS1SocialStudies(
                    full_name=student.full_name
                )
                db.session.add(first_term)
                db.session.add(second_term)
                db.session.add(third_term)
                db.session.commit()

            check_computing = FirstTermJHS1Computing.query.filter_by(full_name=student.full_name).first()
            if not check_computing:
                first_term = FirstTermJHS1Computing(full_name=student.full_name)
                second_term = SecondTermJHS1Computing(full_name=student.full_name)
                third_term = ThirdTermJHS1Computing(full_name=student.full_name)
                db.session.add(first_term)
                db.session.add(second_term)
                db.session.add(third_term)
                db.session.commit()

            check_rme = FirstTermJHS1ReligiousMoralEducation.query.filter_by(full_name=student.full_name).first()
            if not check_rme:
                first_term = FirstTermJHS1ReligiousMoralEducation(full_name=student.full_name)
                second_term = SecondTermJHS1ReligiousMoralEducation(full_name=student.full_name)
                third_term = ThirdTermJHS1ReligiousMoralEducation(full_name=student.full_name)
                db.session.add(first_term)
                db.session.add(second_term)
                db.session.add(third_term)
                db.session.commit()

            check_cad = FirstTermJHS1CreativeArtsAndDesign.query.filter_by(full_name=student.full_name).first()
            if not check_cad:
                first_term = FirstTermJHS1CreativeArtsAndDesign(full_name=student.full_name)
                second_term = SecondTermJHS1CreativeArtsAndDesign(full_name=student.full_name)
                third_term = ThirdTermJHS1CreativeArtsAndDesign(full_name=student.full_name)
                db.session.add(first_term)
                db.session.add(second_term)
                db.session.add(third_term)
                db.session.commit()

            check_career_tech = FirstTermJHS1CareerTechnology.query.filter_by(full_name=student.full_name).first()
            if not check_career_tech:
                first_term = FirstTermJHS1CareerTechnology(full_name=student.full_name)
                second_term = SecondTermJHS1CareerTechnology(full_name=student.full_name)
                third_term = ThirdTermJHS1CareerTechnology(full_name=student.full_name)
                db.session.add(first_term)
                db.session.add(second_term)
                db.session.add(third_term)
                db.session.commit()

    for student in jhs2_students:
        check_student = JHS2Student.query.filter_by(full_name=student.full_name).first()
        if check_student:
            pass
        else:
            jhs2_student = JHS2Student(
                full_name=student.full_name,
                fathers_name=student.fathers_name,
                fathers_contact=student.fathers_contact,
                mothers_name=student.mothers_name,
                mothers_number=student.mothers_number,
                date_of_birth=student.date_of_birth
            )
            db.session.add(jhs2_student)
            check_maths = FirstTermJHS2Mathematics.query.filter_by(full_name=student.full_name).first()
            if not check_maths:
                first_term_maths = FirstTermJHS2Mathematics(
                    full_name=student.full_name
                )
                second_term_maths = SecondTermJHS2Mathematics(
                    full_name=student.full_name
                )
                third_term_maths = ThirdTermJHS3Mathematics(
                    full_name=student.full_name
                )
                db.session.add(first_term_maths)
                db.session.add(second_term_maths)
                db.session.add(third_term_maths)
                db.session.commit()

            check_english = FirstTermJHS2EnglishLanguage.query.filter_by(full_name=student.full_name).first()
            if not check_english:
                first_term = FirstTermJHS2EnglishLanguage(
                    full_name=student.full_name
                )
                second_term = SecondTermJHS2EnglishLanguage(
                    full_name=student.full_name
                )
                third_term = ThirdTermJHS2EnglishLanguage(
                    full_name=student.full_name
                )
                db.session.add(first_term)
                db.session.add(second_term)
                db.session.add(third_term)
                db.session.commit()

            check_science = FirstTermJHS2IntegratedScience.query.filter_by(full_name=student.full_name).first()
            if not check_science:
                first_term = FirstTermJHS2IntegratedScience(
                    full_name=student.full_name
                )
                second_term = SecondTermJHS2IntegratedScience(
                    full_name=student.full_name
                )
                third_term = ThirdTermJHS2IntegratedScience(
                    full_name=student.full_name
                )
                db.session.add(first_term)
                db.session.add(second_term)
                db.session.add(third_term)
                db.session.commit()

            check_social = FirstTermJHS2SocialStudies.query.filter_by(full_name=student.full_name).first()
            if not check_social:
                first_term = FirstTermJHS2SocialStudies(
                    full_name=student.full_name
                )
                second_term = SecondTermJHS2SocialStudies(
                    full_name=student.full_name
                )
                third_term = ThirdTermJHS2SocialStudies(
                    full_name=student.full_name
                )
                db.session.add(first_term)
                db.session.add(second_term)
                db.session.add(third_term)
                db.session.commit()

            check_computing = FirstTermJHS2Computing.query.filter_by(full_name=student.full_name).first()
            if not check_computing:
                first_term = FirstTermJHS2Computing(full_name=student.full_name)
                second_term = SecondTermJHS2Computing(full_name=student.full_name)
                third_term = ThirdTermJHS2Computing(full_name=student.full_name)
                db.session.add(first_term)
                db.session.add(second_term)
                db.session.add(third_term)
                db.session.commit()

            check_rme = FirstTermJHS2ReligiousMoralEducation.query.filter_by(full_name=student.full_name).first()
            if not check_rme:
                first_term = FirstTermJHS2ReligiousMoralEducation(full_name=student.full_name)
                second_term = SecondTermJHS2ReligiousMoralEducation(full_name=student.full_name)
                third_term = ThirdTermJHS2ReligiousMoralEducation(full_name=student.full_name)
                db.session.add(first_term)
                db.session.add(second_term)
                db.session.add(third_term)
                db.session.commit()

            check_cad = FirstTermJHS2CreativeArtsAndDesign.query.filter_by(full_name=student.full_name).first()
            if not check_cad:
                first_term = FirstTermJHS2CreativeArtsAndDesign(full_name=student.full_name)
                second_term = SecondTermJHS2CreativeArtsAndDesign(full_name=student.full_name)
                third_term = ThirdTermJHS2CreativeArtsAndDesign(full_name=student.full_name)
                db.session.add(first_term)
                db.session.add(second_term)
                db.session.add(third_term)
                db.session.commit()

            check_career_tech = FirstTermJHS2CareerTechnology.query.filter_by(full_name=student.full_name).first()
            if not check_career_tech:
                first_term = FirstTermJHS2CareerTechnology(full_name=student.full_name)
                second_term = SecondTermJHS2CareerTechnology(full_name=student.full_name)
                third_term = ThirdTermJHS2CareerTechnology(full_name=student.full_name)
                db.session.add(first_term)
                db.session.add(second_term)
                db.session.add(third_term)
                db.session.commit()

    for student in jhs3_students:
        check_student = JHS3Student.query.filter_by(full_name=student.full_name).first()
        if check_student:
            pass
        else:
            jhs3_student = JHS3Student(
                full_name=student.full_name,
                fathers_name=student.fathers_name,
                fathers_contact=student.fathers_contact,
                mothers_name=student.mothers_name,
                mothers_number=student.mothers_number,
                date_of_birth=student.date_of_birth
            )
            db.session.add(jhs3_student)
            check_maths = FirstTermJHS3Mathematics.query.filter_by(full_name=student.full_name).first()
            if not check_maths:
                first_term_maths = FirstTermJHS3Mathematics(
                    full_name=student.full_name
                )
                second_term_maths = SecondTermJHS3Mathematics(
                    full_name=student.full_name
                )
                third_term_maths = ThirdTermJHS3Mathematics(
                    full_name=student.full_name
                )
                db.session.add(first_term_maths)
                db.session.add(second_term_maths)
                db.session.add(third_term_maths)
                db.session.commit()

            check_english = FirstTermJHS3EnglishLanguage.query.filter_by(full_name=student.full_name).first()
            if not check_english:
                first_term = FirstTermJHS3EnglishLanguage(
                    full_name=student.full_name
                )
                second_term = SecondTermJHS3EnglishLanguage(
                    full_name=student.full_name
                )
                third_term = ThirdTermJHS3EnglishLanguage(
                    full_name=student.full_name
                )
                db.session.add(first_term)
                db.session.add(second_term)
                db.session.add(third_term)
                db.session.commit()

            check_science = FirstTermJHS3IntegratedScience.query.filter_by(full_name=student.full_name).first()
            if not check_science:
                first_term = FirstTermJHS3IntegratedScience(
                    full_name=student.full_name
                )
                second_term = SecondTermJHS3IntegratedScience(
                    full_name=student.full_name
                )
                third_term = ThirdTermJHS3IntegratedScience(
                    full_name=student.full_name
                )
                db.session.add(first_term)
                db.session.add(second_term)
                db.session.add(third_term)
                db.session.commit()

            check_social = FirstTermJHS3SocialStudies.query.filter_by(full_name=student.full_name).first()
            if not check_social:
                first_term = FirstTermJHS3SocialStudies(
                    full_name=student.full_name
                )
                second_term = SecondTermJHS3SocialStudies(
                    full_name=student.full_name
                )
                third_term = ThirdTermJHS3SocialStudies(
                    full_name=student.full_name
                )
                db.session.add(first_term)
                db.session.add(second_term)
                db.session.add(third_term)
                db.session.commit()

            check_computing = FirstTermJHS3Computing.query.filter_by(full_name=student.full_name).first()
            if not check_computing:
                first_term = FirstTermJHS3Computing(full_name=student.full_name)
                second_term = SecondTermJHS3Computing(full_name=student.full_name)
                third_term = ThirdTermJHS3Computing(full_name=student.full_name)
                db.session.add(first_term)
                db.session.add(second_term)
                db.session.add(third_term)
                db.session.commit()

            check_rme = FirstTermJHS3ReligiousMoralEducation.query.filter_by(full_name=student.full_name).first()
            if not check_rme:
                first_term = FirstTermJHS3ReligiousMoralEducation(full_name=student.full_name)
                second_term = SecondTermJHS3ReligiousMoralEducation(full_name=student.full_name)
                third_term = ThirdTermJHS3ReligiousMoralEducation(full_name=student.full_name)
                db.session.add(first_term)
                db.session.add(second_term)
                db.session.add(third_term)
                db.session.commit()

            check_cad = FirstTermJHS3CreativeArtsAndDesign.query.filter_by(full_name=student.full_name).first()
            if not check_cad:
                first_term = FirstTermJHS3CreativeArtsAndDesign(full_name=student.full_name)
                second_term = SecondTermJHS3CreativeArtsAndDesign(full_name=student.full_name)
                third_term = ThirdTermJHS3CreativeArtsAndDesign(full_name=student.full_name)
                db.session.add(first_term)
                db.session.add(second_term)
                db.session.add(third_term)
                db.session.commit()

            check_career_tech = FirstTermJHS3CareerTechnology.query.filter_by(full_name=student.full_name).first()
            if not check_career_tech:
                first_term = FirstTermJHS3CareerTechnology(full_name=student.full_name)
                second_term = SecondTermJHS3CareerTechnology(full_name=student.full_name)
                third_term = ThirdTermJHS3CareerTechnology(full_name=student.full_name)
                db.session.add(first_term)
                db.session.add(second_term)
                db.session.add(third_term)
                db.session.commit()

    # # Populate form 1 subject tables with form 1 students
    # for student in jhs1_students:
    #     check_maths = JHS1Mathematics.query.filter_by(full_name=student.full_name).first()
    #     if not check_maths:
    #         jhs1_maths = JHS1Mathematics(
    #             id = student.id,
    #             full_name = student.full_name
    #             )
    #         db.session.add(jhs1_maths)
    #     check_english = JHS1EnglishLanguage.query.filter_by(full_name=student.full_name).first()
    #     if not check_english:
    #         jhs1_english = JHS1EnglishLanguage(
    #             id = student.id,
    #             full_name =student.full_name
    #             )
    #         db.session.add(jhs1_english)
    #     check_science = JHS1IntegratedScience.query.filter_by(full_name=student.full_name).first()
    #     if not check_science:
    #         jhs1_science = JHS1IntegratedScience(
    #             id = student.id,
    #             full_name =student.full_name
    #             )
    #         db.session.add(jhs1_science)
    #     check_social = JHS1SocialStudies.query.filter_by(full_name=student.full_name).first()
    #     if not check_social:
    #         social = JHS1SocialStudies(
    #             id = student.id,
    #             full_name =student.full_name
    #             )
    #         db.session.add(social)
    #     check_computing = JHS1Computing.query.filter_by(full_name=student.full_name).first()
    #     if not check_computing:
    #         computing = JHS1Computing(id=student.id, full_name=student.full_name)
    #         db.session.add(computing)
    #     check_rme = JHS1ReligiousMoralEducation.query.filter_by(fullname=student.full_name).first()
    #     if not check_rme:
    #         rme = JHS1ReligiousMoralEducation(id=student.id, full_name=student.full_name)
    #         db.session.add(rme)
    #     check_cad = JHS1CreativeArtsAndDesign.query.filter_by(fullname=student.full_name).first()
    #     if not check_cad:
    #         cad = JHS1CreativeArtsAndDesign(id=student.id, full_name=student.full_name)
    #         db.session.add(cad)
    #     check_career_tech = JHS1CareerTechnology.query.filter_by(full_name=student.full_name).first()
    #     if not check_career_tech:
    #         c_tech = JHS1CareerTechnology(id=student.id, full_name=student.full_name)
    #         db.session.add(c_tech)

    # Populate form 2 subjec tables with form 2 students
    # for student in jhs2_students:
    #     check_maths = JHS2Mathematics.query.filter_by(full_name=student.full_name).first()
    #     if not check_maths:
    #         jhs2_maths = JHS2Mathematics(
    #             id = student.id,
    #             full_name = student.full_name
    #             )
    #         db.session.add(jhs2_maths)
    #     check_english = JHS2EnglishLanguage.query.filter_by(full_name=student.full_name).first()
    #     if not check_english:            
    #         jhs2_english = JHS2EnglishLanguage(
    #             id = student.id,
    #             full_name =student.full_name
    #             )
    #         db.session.add(jhs2_english)
    #     check_science = JHS2IntegratedScience.query.filter_by(full_name=student.full_name).first()
    #     if not check_science:
    #         jhs2_science = JHS2IntegratedScience(
    #             id = student.id,
    #             full_name =student.full_name
    #             )
    #         db.session.add(jhs2_science)
    #     check_social = JHS2SocialStudies.query.filter_by(full_name=student.full_name).first()
    #     if not check_social:
    #         social = JHS2SocialStudies(
    #             id = student.id,
    #             full_name =student.full_name
    #             )
    #         db.session.add(social)
    #     check_computing = JHS2Computing.query.filter_by(full_name=student.full_name).first()
    #     if not check_computing:
    #         computing = JHS2Computing(id=student.id, full_name=student.full_name)
    #         db.session.add(computing)
    #     check_rme = JHS2ReligiousMoralEducation.query.filter_by(full_name=student.full_name).first()
    #     if not check_rme:
    #         rme = JHS2ReligiousMoralEducation(id=student.id, full_name=student.full_name)
    #         db.session.add(rme)
    #     check_cad = JHS2CreativeArtsAndDesign.query.filter_by(full_name=student.full_name).first()
    #     if not check_cad:
    #         cad = JHS2CreativeArtsAndDesign(id=student.id, full_name=student.full_name)
    #         db.session.add(cad)
    #     check_career_tech = JHS2CareerTechnology.query.filter_by(full_name=student.full_name).first()
    #     if not check_career_tech:
    #         c_tech = JHS2CareerTechnology(id=student.id, full_name=student.full_name)
    #         db.session.add(c_tech)

    # # Populate form 3 subjec tables with form 3 students
    # for student in jhs3_students:
    #     check_maths = JHS3Mathematics.query.filter_by(full_name=student.full_name).first()
    #     if not check_maths:
    #         maths = JHS3Mathematics(
    #             id = student.id,
    #             full_name = student.full_name
    #             )
    #         db.session.add(maths)
    #     check_english = JHS3EnglishLanguage.query.filter_by(full_name=student.full_name).first()
    #     if not check_english:
    #         english = JHS3EnglishLanguage(
    #             id = student.id,
    #             full_name =student.full_name
    #             )
    #         db.session.add(english)
    #     check_science = JHS3IntegratedScience.query.filter_by(full_name=student.full_name).first()
    #     if not check_science:
    #         science = JHS3IntegratedScience(
    #             id = student.id,
    #             full_name =student.full_name
    #             )
    #         db.session.add(science)
    #     check_social = JHS3SocialStudies.query.filter_by(full_name=student.full_name).first()
    #     if not check_social:
    #         social = JHS3SocialStudies(
    #             id = student.id,
    #             full_name =student.full_name
    #             )
    #         db.session.add(social)
    #     check_computing = JHS3Computing.query.filter_by(full_name=student.full_name).first()
    #     if not check_computing:
    #         computing = JHS3Computing(id=student.id, full_name=student.full_name)
    #         db.session.add(computing)
    #     check_rme = JHS3ReligiousMoralEducation.query.filter_by(full_name=student.full_name).first()
    #     if not check_rme:
    #         rme = JHS3ReligiousMoralEducation(id=student.id, full_name=student.full_name)
    #         db.session.add(rme)
    #     check_cad = JHS3CreativeArtsAndDesign.query.filter_by(full_name=student.full_name).first()
    #     if not check_cad:
    #         cad = JHS3CreativeArtsAndDesign(id=student.id, full_name=student.full_name)
    #         db.session.add(cad)
    #     check_career_tech = JHS3CareerTechnology.query.filter_by(full_name=student.full_name).first()
    #     if not check_career_tech:
    #         c_tech = JHS3CareerTechnology(id=student.id, full_name=student.full_name)
    #         db.session.add(c_tech)
    db.session.commit()


# function to give admin privileges other users don't have
def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if current_user.id != 1:
            return abort(403)
        # Otherwise continue with the route function
        return f(*args, **kwargs)

    return decorated_function


# use login_manager to load authenticated users
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# route to render html pages of websites
@app.route('/home')
def home():
    return render_template('index.html', current_user=current_user)


@app.route('/courses')
def subjects():
    return render_template('courses.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')


@app.route('/teachers_portal')
def teachers_portal():
    return render_template('portal.html')


# route to register admin
@app.route('/admin-register', methods=['GET', 'POST'])
def administrator_register():
    form = NewAdminForm()
    if form.validate_on_submit():
        name = form.name.data.title()
        email = form.email.data
        confirm_password = form.confirm_password.data
        subject = form.subject.data
        hashed_password = generate_password_hash(confirm_password)
        new_teacher = User()
        new_teacher.name = name
        new_teacher.email = email
        new_teacher.subject = subject
        new_teacher.password = hashed_password
        db.session.add(new_teacher)
        db.session.commit()
        login_user(new_teacher)
        next_page = request.args.get('next')
        return redirect(url_for(next_page) if next_page else '/')
    return render_template('register.html', form=form)


# route to register teaching staff
@app.route('/teaching-staff-registration', methods=['GET', 'POST'])
def register_teaching_staff():
    form = TeacherRegisterForm()
    if form.validate_on_submit():
        name = form.name.data.title()
        email = form.email.data
        confirm_password = form.confirm_password.data
        subject = form.subject.data
        hashed_password = generate_password_hash(confirm_password)
        check_user = User.query.filter_by(email=email).first()
        if check_user:
            flash('Email already registered with Blog! Log In Instead?')
            return redirect(url_for('teaching_staff'))
        else:
            confirm_teacher = Teacher().query.filter_by(name=name).first()
            if confirm_teacher:
                new_teacher = User(
                    name=name,
                    email=email,
                    password=hashed_password,
                    subject=subject
                )

                db.session.add(new_teacher)
                db.session.commit()
                login_user(new_teacher)
                next_page = request.args.get('next')
                return redirect(url_for(next_page) if next_page else 'home')
            else:
                flash('Identity not confirmed! See administration!')
                return redirect(url_for('register_teaching_staff'))
    return render_template('register.html', form=form)


# route for registered teaching staff to login
@app.route('/teaching-staff-sign-in', methods=['GET', 'POST'])
def teaching_staff():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = TeacherSignInForm()
    if form.validate_on_submit():
        subject = form.subject.data
        email = form.email.data
        password = form.password.data
        check_teacher = User.query.filter_by(email=email).first()
        if check_teacher:
            if check_password_hash(check_teacher.password, password):
                login_user(check_teacher)
                next_page = request.args.get('next')  # Corrected variable name
                return redirect(url_for(next_page) if next_page else 'home')
            else:
                flash('Wrong Password')
                return redirect(url_for('teaching_staff'))
        else:
            flash('Email does not exist! Create an account instead?')
            return redirect(url_for('teaching_staff'))
    return render_template('sign-in.html', form=form)


# route for admin only to register a new student into the schools database table for students
@app.route('/add_new_student', methods=['GET', 'POST'])
@admin_only
def new_student():
    form = NewStudentForm()
    if form.validate_on_submit():
        name = form.full_name.data
        father = form.father_name.data
        mother = form.mother_name.data
        father_contact = form.father_contact.data
        mother_contact = form.mother_number.data
        date_of_birth = form.date_of_birth.data
        grade = form.current_class.data
        school_fees = form.fees.data
        amount_paid = form.paid.data
        new_jhs_student = JHSStudent(
            full_name=name,
            fathers_name=father,
            fathers_contact=father_contact,
            mothers_name=mother,
            mothers_number=mother_contact,
            date_of_birth=date_of_birth,
            current_class=grade,
            school_fees=school_fees,
            amount_paid=amount_paid,
            school_fees_debt=int(school_fees - amount_paid)
        )
        db.session.add(new_jhs_student)
        db.session.commit()

        if grade == 7:
            jhs1_student = JHS1Student(
                full_name=name,
                fathers_name=father,
                fathers_contact=father_contact,
                mothers_name=mother,
                mothers_number=mother_contact,
                date_of_birth=date_of_birth
            )
            db.session.add(jhs1_student)
            db.session.commit()

            check_maths = FirstTermJHS1Mathematics.query.filter_by(full_name=name).first()
            if not check_maths:
                first_term_maths = FirstTermJHS1Mathematics(
                    full_name=name
                )
                second_term_maths = SecondTermJHS1Mathematics(
                    full_name=name
                )
                third_term_maths = ThirdTermJHS1Mathematics(
                    full_name=name
                )
                db.session.add(first_term_maths)
                db.session.add(second_term_maths)
                db.session.add(third_term_maths)
                db.session.commit()

            check_english = FirstTermJHS1EnglishLanguage.query.filter_by(full_name=name).first()
            if not check_english:
                first_term = FirstTermJHS1EnglishLanguage(
                    full_name=name
                )
                second_term = SecondTermJHS1EnglishLanguage(
                    full_name=name
                )
                third_term = ThirdTermJHS1EnglishLanguage(
                    full_name=name
                )
                db.session.add(first_term)
                db.session.add(second_term)
                db.session.add(third_term)
                db.session.commit()

            check_science = FirstTermJHS1IntegratedScience.query.filter_by(full_name=name).first()
            if not check_science:
                first_term = FirstTermJHS1IntegratedScience(
                    full_name=name
                )
                second_term = SecondTermJHS1IntegratedScience(
                    full_name=name
                )
                third_term = ThirdTermJHS1IntegratedScience(
                    full_name=name
                )
                db.session.add(first_term)
                db.session.add(second_term)
                db.session.add(third_term)
                db.session.commit()

            check_social = FirstTermJHS1SocialStudies.query.filter_by(full_name=name).first()
            if not check_social:
                first_term = FirstTermJHS1SocialStudies(
                    full_name=name
                )
                second_term = SecondTermJHS1SocialStudies(
                    full_name=name
                )
                third_term = ThirdTermJHS1SocialStudies(
                    full_name=name
                )
                db.session.add(first_term)
                db.session.add(second_term)
                db.session.add(third_term)
                db.session.commit()

            check_computing = FirstTermJHS1Computing.query.filter_by(full_name=name).first()
            if not check_computing:
                first_term = FirstTermJHS1Computing(full_name=name)
                second_term = SecondTermJHS1Computing(full_name=name)
                third_term = ThirdTermJHS1Computing(full_name=name)
                db.session.add(first_term)
                db.session.add(second_term)
                db.session.add(third_term)
                db.session.commit()

            check_rme = FirstTermJHS1ReligiousMoralEducation.query.filter_by(full_name=name).first()
            if not check_rme:
                first_term = FirstTermJHS1ReligiousMoralEducation(full_name=name)
                second_term = SecondTermJHS1ReligiousMoralEducation(full_name=name)
                third_term = ThirdTermJHS1ReligiousMoralEducation(full_name=name)
                db.session.add(first_term)
                db.session.add(second_term)
                db.session.add(third_term)
                db.session.commit()

            check_cad = FirstTermJHS1CreativeArtsAndDesign.query.filter_by(full_name=name).first()
            if not check_cad:
                first_term = FirstTermJHS1CreativeArtsAndDesign(full_name=name)
                second_term = SecondTermJHS1CreativeArtsAndDesign(full_name=name)
                third_term = ThirdTermJHS1CreativeArtsAndDesign(full_name=name)
                db.session.add(first_term)
                db.session.add(second_term)
                db.session.add(third_term)
                db.session.commit()

            check_career_tech = FirstTermJHS1CareerTechnology.query.filter_by(full_name=name).first()
            if not check_career_tech:
                first_term = FirstTermJHS1CareerTechnology(full_name=name)
                second_term = SecondTermJHS1CareerTechnology(full_name=name)
                third_term = ThirdTermJHS1CareerTechnology(full_name=name)
                db.session.add(first_term)
                db.session.add(second_term)
                db.session.add(third_term)
                db.session.commit()


        elif grade == 8:
            jhs2_student = JHS2Student(
                full_name=name,
                fathers_name=father,
                fathers_contact=father_contact,
                mothers_name=mother,
                mothers_number=mother_contact,
                date_of_birth=date_of_birth
            )
            db.session.add(jhs2_student)
            db.session.commit()

            check_maths = FirstTermJHS2Mathematics.query.filter_by(full_name=name).first()
            if not check_maths:
                first_term_maths = FirstTermJHS2Mathematics(
                    full_name=name
                )
                second_term_maths = SecondTermJHS2Mathematics(
                    full_name=name
                )
                third_term_maths = ThirdTermJHS3Mathematics(
                    full_name=name
                )
                db.session.add(first_term_maths)
                db.session.add(second_term_maths)
                db.session.add(third_term_maths)
                db.session.commit()

            check_english = FirstTermJHS2EnglishLanguage.query.filter_by(full_name=name).first()
            if not check_english:
                first_term = FirstTermJHS2EnglishLanguage(
                    full_name=name
                )
                second_term = SecondTermJHS2EnglishLanguage(
                    full_name=name
                )
                third_term = ThirdTermJHS2EnglishLanguage(
                    full_name=name
                )
                db.session.add(first_term)
                db.session.add(second_term)
                db.session.add(third_term)
                db.session.commit()

            check_science = FirstTermJHS2IntegratedScience.query.filter_by(full_name=name).first()
            if not check_science:
                first_term = FirstTermJHS2IntegratedScience(
                    full_name=name
                )
                second_term = SecondTermJHS2IntegratedScience(
                    full_name=name
                )
                third_term = ThirdTermJHS2IntegratedScience(
                    full_name=name
                )
                db.session.add(first_term)
                db.session.add(second_term)
                db.session.add(third_term)
                db.session.commit()

            check_social = FirstTermJHS2SocialStudies.query.filter_by(full_name=name).first()
            if not check_social:
                first_term = FirstTermJHS2SocialStudies(
                    full_name=name
                )
                second_term = SecondTermJHS2SocialStudies(
                    full_name=name
                )
                third_term = ThirdTermJHS2SocialStudies(
                    full_name=name
                )
                db.session.add(first_term)
                db.session.add(second_term)
                db.session.add(third_term)
                db.session.commit()

            check_computing = FirstTermJHS2Computing.query.filter_by(full_name=name).first()
            if not check_computing:
                first_term = FirstTermJHS2Computing(full_name=name)
                second_term = SecondTermJHS2Computing(full_name=name)
                third_term = ThirdTermJHS2Computing(full_name=name)
                db.session.add(first_term)
                db.session.add(second_term)
                db.session.add(third_term)
                db.session.commit()

            check_rme = FirstTermJHS2ReligiousMoralEducation.query.filter_by(full_name=name).first()
            if not check_rme:
                first_term = FirstTermJHS2ReligiousMoralEducation(full_name=name)
                second_term = SecondTermJHS2ReligiousMoralEducation(full_name=name)
                third_term = ThirdTermJHS2ReligiousMoralEducation(full_name=name)
                db.session.add(first_term)
                db.session.add(second_term)
                db.session.add(third_term)
                db.session.commit()

            check_cad = FirstTermJHS2CreativeArtsAndDesign.query.filter_by(full_name=name).first()
            if not check_cad:
                first_term = FirstTermJHS2CreativeArtsAndDesign(full_name=name)
                second_term = SecondTermJHS2CreativeArtsAndDesign(full_name=name)
                third_term = ThirdTermJHS2CreativeArtsAndDesign(full_name=name)
                db.session.add(first_term)
                db.session.add(second_term)
                db.session.add(third_term)
                db.session.commit()

            check_career_tech = FirstTermJHS2CareerTechnology.query.filter_by(full_name=name).first()
            if not check_career_tech:
                first_term = FirstTermJHS2CareerTechnology(full_name=name)
                second_term = SecondTermJHS2CareerTechnology(full_name=name)
                third_term = ThirdTermJHS2CareerTechnology(full_name=name)
                db.session.add(first_term)
                db.session.add(second_term)
                db.session.add(third_term)
                db.session.commit()



        elif grade == 9:
            jhs3_student = JHS3Student(
                full_name=name,
                fathers_name=father,
                fathers_contact=father_contact,
                mothers_name=mother,
                mothers_number=mother_contact,
                date_of_birth=date_of_birth
            )
            db.session.add(jhs3_student)
            db.session.commit()

            check_maths = FirstTermJHS3Mathematics.query.filter_by(full_name=name).first()
            if not check_maths:
                first_term_maths = FirstTermJHS3Mathematics(
                    full_name=name
                )
                second_term_maths = SecondTermJHS3Mathematics(
                    full_name=name
                )
                third_term_maths = ThirdTermJHS3Mathematics(
                    full_name=name
                )
                db.session.add(first_term_maths)
                db.session.add(second_term_maths)
                db.session.add(third_term_maths)
                db.session.commit()

            check_english = FirstTermJHS3EnglishLanguage.query.filter_by(full_name=name).first()
            if not check_english:
                first_term = FirstTermJHS3EnglishLanguage(
                    full_name=name
                )
                second_term = SecondTermJHS3EnglishLanguage(
                    full_name=name
                )
                third_term = ThirdTermJHS3EnglishLanguage(
                    full_name=name
                )
                db.session.add(first_term)
                db.session.add(second_term)
                db.session.add(third_term)
                db.session.commit()

            check_science = FirstTermJHS3IntegratedScience.query.filter_by(full_name=name).first()
            if not check_science:
                first_term = FirstTermJHS3IntegratedScience(
                    full_name=name
                )
                second_term = SecondTermJHS3IntegratedScience(
                    full_name=name
                )
                third_term = ThirdTermJHS3IntegratedScience(
                    full_name=name
                )
                db.session.add(first_term)
                db.session.add(second_term)
                db.session.add(third_term)
                db.session.commit()

            check_social = FirstTermJHS3SocialStudies.query.filter_by(full_name=name).first()
            if not check_social:
                first_term = FirstTermJHS3SocialStudies(
                    full_name=name
                )
                second_term = SecondTermJHS3SocialStudies(
                    full_name=name
                )
                third_term = ThirdTermJHS3SocialStudies(
                    full_name=name
                )
                db.session.add(first_term)
                db.session.add(second_term)
                db.session.add(third_term)
                db.session.commit()

            check_computing = FirstTermJHS3Computing.query.filter_by(full_name=name).first()
            if not check_computing:
                first_term = FirstTermJHS3Computing(full_name=name)
                second_term = SecondTermJHS3Computing(full_name=name)
                third_term = ThirdTermJHS3Computing(full_name=name)
                db.session.add(first_term)
                db.session.add(second_term)
                db.session.add(third_term)
                db.session.commit()

            check_rme = FirstTermJHS3ReligiousMoralEducation.query.filter_by(full_name=name).first()
            if not check_rme:
                first_term = FirstTermJHS3ReligiousMoralEducation(full_name=name)
                second_term = SecondTermJHS3ReligiousMoralEducation(full_name=name)
                third_term = ThirdTermJHS3ReligiousMoralEducation(full_name=name)
                db.session.add(first_term)
                db.session.add(second_term)
                db.session.add(third_term)
                db.session.commit()

            check_cad = FirstTermJHS3CreativeArtsAndDesign.query.filter_by(full_name=name).first()
            if not check_cad:
                first_term = FirstTermJHS3CreativeArtsAndDesign(full_name=name)
                second_term = SecondTermJHS3CreativeArtsAndDesign(full_name=name)
                third_term = ThirdTermJHS3CreativeArtsAndDesign(full_name=name)
                db.session.add(first_term)
                db.session.add(second_term)
                db.session.add(third_term)
                db.session.commit()

            check_career_tech = FirstTermJHS3CareerTechnology.query.filter_by(full_name=name).first()
            if not check_career_tech:
                first_term = FirstTermJHS3CareerTechnology(full_name=name)
                second_term = SecondTermJHS3CareerTechnology(full_name=name)
                third_term = ThirdTermJHS3CareerTechnology(full_name=name)
                db.session.add(first_term)
                db.session.add(second_term)
                db.session.add(third_term)
                db.session.commit()

        db.session.commit()
        return redirect(url_for('administrator'))
    return render_template('register_student.html', form=form)


# route for admin only to add a new teacher into the school's database table for teachers
@app.route('/add_new_teacher', methods=['GET', 'POST'])
@admin_only
def add_new_teaching_staff():
    form = NewTeacherForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        subject = form.subject.data
        number = form.number.data
        new_teacher = Teacher(
            name=name,
            email=email,
            subject=subject,
            number=number
        )

        db.session.add(new_teacher)
        db.session.commit()
        return redirect(url_for('administrator'))
    return render_template('register_teacher.html', form=form)


# route for subjects portal which will load up all students to have 
# their class, project and examinations scores to entered and saved into the database table
@app.route('/english-portal')
@login_required
def english():
    form_1_first_term_students = FirstTermJHS1EnglishLanguage.query.all()
    form_1_second_term_students = SecondTermJHS1EnglishLanguage.query.all()
    form_1_third_term_students = ThirdTermJHS1EnglishLanguage.query.all()
    form_2_first_term_students = FirstTermJHS2EnglishLanguage.query.all()
    form_2_second_term_students = SecondTermJHS2EnglishLanguage.query.all()
    form_2_third_term_students = ThirdTermJHS2EnglishLanguage.query.all()
    form_3_first_term_students = FirstTermJHS3EnglishLanguage.query.all()
    form_3_second_term_students = SecondTermJHS3EnglishLanguage.query.all()
    form_3_third_term_students = ThirdTermJHS3EnglishLanguage.query.all()
    return render_template('english_dashboard.html', form_1_first_term_students=form_1_first_term_students,
                           form_1_second_term_students=form_1_second_term_students,
                           form_1_third_term_students=form_1_third_term_students,
                           form_2_first_term_students=form_2_first_term_students,
                           form_2_second_term_students=form_2_second_term_students,
                           form_2_third_term_students=form_2_third_term_students,
                           form_3_first_term_students=form_3_first_term_students,
                           form_3_second_term_students=form_3_second_term_students, current_user=current_user)


@app.route('/first-term-jhs-1-english-student-assessment/<int:index>', methods=['GET', 'POST'])
@login_required
def edit_jhs1_english_student(index):
    student_id = index
    form_1_student = FirstTermJHS1EnglishLanguage.query.filter_by(id=student_id).first()
    form = StudentAssessmentForm()
    if form.validate_on_submit():
        if form_1_student:
            class_test = form.classtest.data
            mid_terms = form.midterms.data
            project_work = form.project_work.data
            examination = form.examinations.data
            form_1_student.classtest = class_test
            form_1_student.midterm_examination = mid_terms
            form_1_student.project_work = project_work
            form_1_student.end_of_term_examination = examination
            form_1_student.subtotal = float(class_test) + float(mid_terms) + float(project_work)
            form_1_student.half_subtotal = (float(class_test) + float(mid_terms) + float(project_work)) / 2
            form_1_student.half_examination = float(examination) / 2
            form_1_student.grand_total = ((float(class_test) + float(mid_terms) + float(project_work)) / 2) + (
                    float(examination) / 2)
            db.session.add(form_1_student)
            db.session.commit()
            return redirect(url_for('english'))
        else:
            flash('Student not found!')

    return render_template('student_assessment.html', form=form)


@app.route('/second-term-jhs-1-english-student-assessment/<int:index>', methods=['GET', 'POST'])
@login_required
def edit_second_term_jhs1_english_student(index):
    student_id = index
    form_1_student = SecondTermJHS1EnglishLanguage.query.filter_by(id=student_id).first()
    form = StudentAssessmentForm()
    if form.validate_on_submit():
        if form_1_student:
            class_test = form.classtest.data
            mid_terms = form.midterms.data
            project_work = form.project_work.data
            examination = form.examinations.data
            form_1_student.classtest = class_test
            form_1_student.midterm_examination = mid_terms
            form_1_student.project_work = project_work
            form_1_student.end_of_term_examination = examination
            form_1_student.subtotal = float(class_test) + float(mid_terms) + float(project_work)
            form_1_student.half_subtotal = (float(class_test) + float(mid_terms) + float(project_work)) / 2
            form_1_student.half_examination = float(examination) / 2
            form_1_student.grand_total = ((float(class_test) + float(mid_terms) + float(project_work)) / 2) + (
                    float(examination) / 2)
            db.session.add(form_1_student)
            db.session.commit()
            return redirect(url_for('english'))
        else:
            flash('Student not found!')

    return render_template('student_assessment.html', form=form)


@app.route('/third-term-jhs-1-english-student-assessment/<int:index>', methods=['GET', 'POST'])
@login_required
def edit_third_term_jhs1_english_student(index):
    student_id = index
    form_1_student = ThirdTermJHS1EnglishLanguage.query.filter_by(id=student_id).first()
    form = StudentAssessmentForm()
    if form.validate_on_submit():
        if form_1_student:
            class_test = form.classtest.data
            mid_terms = form.midterms.data
            project_work = form.project_work.data
            examination = form.examinations.data
            form_1_student.classtest = class_test
            form_1_student.midterm_examination = mid_terms
            form_1_student.project_work = project_work
            form_1_student.end_of_term_examination = examination
            form_1_student.subtotal = float(class_test) + float(mid_terms) + float(project_work)
            form_1_student.half_subtotal = (float(class_test) + float(mid_terms) + float(project_work)) / 2
            form_1_student.half_examination = float(examination) / 2
            form_1_student.grand_total = ((float(class_test) + float(mid_terms) + float(project_work)) / 2) + (
                    float(examination) / 2)
            db.session.add(form_1_student)
            db.session.commit()
            return redirect(url_for('english'))
        else:
            flash('Student not found!')

    return render_template('student_assessment.html', form=form)


@app.route('/first-term-jhs-2-english-student-assessment/<int:index>', methods=['GET', 'POST'])
@login_required
def edit_first_term_jhs2_english_student(index):
    student_id = index
    form_2_student = FirstTermJHS2EnglishLanguage.query.filter_by(id=student_id).first()
    form = StudentAssessmentForm()
    if form.validate_on_submit():
        if form_2_student:
            class_test = form.classtest.data
            mid_terms = form.midterms.data
            project_work = form.project_work.data
            examination = form.examinations.data
            form_2_student.classtest = class_test
            form_2_student.midterm_examination = mid_terms
            form_2_student.project_work = project_work
            form_2_student.end_of_term_examination = examination
            form_2_student.subtotal = float(class_test) + float(mid_terms) + float(project_work)
            form_2_student.half_subtotal = (float(class_test) + float(mid_terms) + float(project_work)) / 2
            form_2_student.half_examination = float(examination) / 2
            form_2_student.grand_total = ((float(class_test) + float(mid_terms) + float(project_work)) / 2) + (
                    float(examination) / 2)
            db.session.add(form_2_student)
            db.session.commit()
            return redirect(url_for('english'))
        else:
            flash('Student not found!')

    return render_template('student_assessment.html', form=form)


@app.route('/second-term-jhs-2-english-student-assessment/<int:index>', methods=['GET', 'POST'])
@login_required
def edit_second_term_jhs2_english_student(index):
    student_id = index
    form_2_student = SecondTermJHS2EnglishLanguage.query.filter_by(id=student_id).first()
    form = StudentAssessmentForm()
    if form.validate_on_submit():
        if form_2_student:
            class_test = form.classtest.data
            mid_terms = form.midterms.data
            project_work = form.project_work.data
            examination = form.examinations.data
            form_2_student.classtest = class_test
            form_2_student.midterm_examination = mid_terms
            form_2_student.project_work = project_work
            form_2_student.end_of_term_examination = examination
            form_2_student.subtotal = float(class_test) + float(mid_terms) + float(project_work)
            form_2_student.half_subtotal = (float(class_test) + float(mid_terms) + float(project_work)) / 2
            form_2_student.half_examination = float(examination) / 2
            form_2_student.grand_total = ((float(class_test) + float(mid_terms) + float(project_work)) / 2) + (
                    float(examination) / 2)
            db.session.add(form_2_student)
            db.session.commit()
            return redirect(url_for('english'))
        else:
            flash('Student not found!')

    return render_template('student_assessment.html', form=form)


@app.route('/third-term-jhs-2-english-student-assessment/<int:index>', methods=['GET', 'POST'])
@login_required
def edit_third_term_jhs2_english_student(index):
    student_id = index
    form_2_student = ThirdTermJHS2EnglishLanguage.query.filter_by(id=student_id).first()
    form = StudentAssessmentForm()
    if form.validate_on_submit():
        if form_2_student:
            class_test = form.classtest.data
            mid_terms = form.midterms.data
            project_work = form.project_work.data
            examination = form.examinations.data
            form_2_student.classtest = class_test
            form_2_student.midterm_examination = mid_terms
            form_2_student.project_work = project_work
            form_2_student.end_of_term_examination = examination
            form_2_student.subtotal = float(class_test) + float(mid_terms) + float(project_work)
            form_2_student.half_subtotal = (float(class_test) + float(mid_terms) + float(project_work)) / 2
            form_2_student.half_examination = float(examination) / 2
            form_2_student.grand_total = ((float(class_test) + float(mid_terms) + float(project_work)) / 2) + (
                    float(examination) / 2)
            db.session.add(form_2_student)
            db.session.commit()
            return redirect(url_for('english'))
        else:
            flash('Student not found!')

    return render_template('student_assessment.html', form=form)


@app.route('/first-term-jhs-3-english-student-assessment/<int:index>', methods=['GET', 'POST'])
@login_required
def edit_first_term_jhs3_english_student(index):
    student_id = index
    form_3_student = FirstTermJHS3EnglishLanguage.query.filter_by(id=student_id).first()
    form = StudentAssessmentForm()
    if form.validate_on_submit():
        if form_3_student:
            class_test = form.classtest.data
            mid_terms = form.midterms.data
            project_work = form.project_work.data
            examination = form.examinations.data
            form_3_student.classtest = class_test
            form_3_student.midterm_examination = mid_terms
            form_3_student.project_work = project_work
            form_3_student.end_of_term_examination = examination
            form_3_student.subtotal = float(class_test) + float(mid_terms) + float(project_work)
            form_3_student.half_subtotal = (float(class_test) + float(mid_terms) + float(project_work)) / 2
            form_3_student.half_examination = float(examination) / 2
            form_3_student.grand_total = ((float(class_test) + float(mid_terms) + float(project_work)) / 2) + (
                    float(examination) / 2)
            db.session.add(form_3_student)
            db.session.commit()
            return redirect(url_for('english'))
        else:
            flash('Student not found!')

    return render_template('student_assessment.html', form=form)


@app.route('/first-term-jhs-3-english-student-assessment/<int:index>', methods=['GET', 'POST'])
@login_required
def edit_first_term_jhs3_english_student(index):
    student_id = index
    form_3_student = FirstTermJHS3EnglishLanguage.query.filter_by(id=student_id).first()
    form = StudentAssessmentForm()
    if form.validate_on_submit():
        if form_3_student:
            class_test = form.classtest.data
            mid_terms = form.midterms.data
            project_work = form.project_work.data
            examination = form.examinations.data
            form_3_student.classtest = class_test
            form_3_student.midterm_examination = mid_terms
            form_3_student.project_work = project_work
            form_3_student.end_of_term_examination = examination
            form_3_student.subtotal = float(class_test) + float(mid_terms) + float(project_work)
            form_3_student.half_subtotal = (float(class_test) + float(mid_terms) + float(project_work)) / 2
            form_3_student.half_examination = float(examination) / 2
            form_3_student.grand_total = ((float(class_test) + float(mid_terms) + float(project_work)) / 2) + (
                    float(examination) / 2)
            db.session.add(form_3_student)
            db.session.commit()
            return redirect(url_for('english'))
        else:
            flash('Student not found!')

    return render_template('student_assessment.html', form=form)


@app.route('/second-term-jhs-3-english-student-assessment/<int:index>', methods=['GET', 'POST'])
@login_required
def edit_second_term_jhs3_english_student(index):
    student_id = index
    form_3_student = SecondTermJHS3EnglishLanguage.query.filter_by(id=student_id).first()
    form = StudentAssessmentForm()
    if form.validate_on_submit():
        if form_3_student:
            class_test = form.classtest.data
            mid_terms = form.midterms.data
            project_work = form.project_work.data
            examination = form.examinations.data
            form_3_student.classtest = class_test
            form_3_student.midterm_examination = mid_terms
            form_3_student.project_work = project_work
            form_3_student.end_of_term_examination = examination
            form_3_student.subtotal = float(class_test) + float(mid_terms) + float(project_work)
            form_3_student.half_subtotal = (float(class_test) + float(mid_terms) + float(project_work)) / 2
            form_3_student.half_examination = float(examination) / 2
            form_3_student.grand_total = ((float(class_test) + float(mid_terms) + float(project_work)) / 2) + (
                    float(examination) / 2)
            db.session.add(form_3_student)
            db.session.commit()
            return redirect(url_for('english'))
        else:
            flash('Student not found!')

    return render_template('student_assessment.html', form=form)


@app.route('/third-term-jhs-3-english-student-assessment/<int:index>', methods=['GET', 'POST'])
@login_required
def edit_third_term_jhs3_english_student(index):
    student_id = index
    form_3_student = ThirdTermJHS3EnglishLanguage.query.filter_by(id=student_id).first()
    form = StudentAssessmentForm()
    if form.validate_on_submit():
        if form_3_student:
            class_test = form.classtest.data
            mid_terms = form.midterms.data
            project_work = form.project_work.data
            examination = form.examinations.data
            form_3_student.classtest = class_test
            form_3_student.midterm_examination = mid_terms
            form_3_student.project_work = project_work
            form_3_student.end_of_term_examination = examination
            form_3_student.subtotal = float(class_test) + float(mid_terms) + float(project_work)
            form_3_student.half_subtotal = (float(class_test) + float(mid_terms) + float(project_work)) / 2
            form_3_student.half_examination = float(examination) / 2
            form_3_student.grand_total = ((float(class_test) + float(mid_terms) + float(project_work)) / 2) + (
                    float(examination) / 2)
            db.session.add(form_3_student)
            db.session.commit()
            return redirect(url_for('english'))
        else:
            flash('Student not found!')

    return render_template('student_assessment.html', form=form)


@app.route('/mathematics-portal')
@login_required
def mathematics():
    form_1_first_term_students = FirstTermJHS1Mathematics.query.all()
    form_1_second_term_students = SecondTermJHS1Mathematics.query.all()
    form_1_third_term_students = ThirdTermJHS1Mathematics.query.all()
    form_2_first_term_students = FirstTermJHS2Mathematics.query.all()
    form_2_second_term_students = SecondTermJHS2Mathematics.query.all()
    form_2_third_term_students = ThirdTermJHS2Mathematics.query.all()
    form_3_first_term_students = FirstTermJHS3Mathematics.query.all()
    form_3_second_term_students = SecondTermJHS3Mathematics.query.all()
    form_3_third_term_students = ThirdTermJHS3Mathematics.query.all()
    return render_template('english_dashboard.html', form_1_first_term_students=form_1_first_term_students,
                           form_1_second_term_students=form_1_second_term_students,
                           form_1_third_term_students=form_1_third_term_students,
                           form_2_first_term_students=form_2_first_term_students,
                           form_2_second_term_students=form_2_second_term_students,
                           form_2_third_term_students=form_2_third_term_students,
                           form_3_first_term_students=form_3_first_term_students,
                           form_3_second_term_students=form_3_second_term_students, current_user=current_user)


@app.route('/first-term-jhs-1-maths-student-assessment/<int:index>', methods=['GET', 'POST'])
@login_required
def edit_first_term_jhs1_maths_student(index):
    student_id = index
    form_1_student = FirstTermJHS1Mathematics.query.filter_by(id=student_id).first()
    form = StudentAssessmentForm()
    if form.validate_on_submit():
        if form_1_student:
            class_test = form.classtest.data
            mid_terms = form.midterms.data
            project_work = form.project_work.data
            examination = form.examinations.data
            form_1_student.classtest = class_test
            form_1_student.midterm_examination = mid_terms
            form_1_student.project_work = project_work
            form_1_student.end_of_term_examination = examination
            form_1_student.subtotal = float(class_test) + float(mid_terms) + float(project_work)
            form_1_student.half_subtotal = (float(class_test) + float(mid_terms) + float(project_work)) / 2
            form_1_student.half_examination = float(examination) / 2
            form_1_student.grand_total = ((float(class_test) + float(mid_terms) + float(project_work)) / 2) + (
                    float(examination) / 2)
            db.session.add(form_1_student)
            db.session.commit()
            return redirect(url_for('mathematics'))
        else:
            flash('Student not found!')

    return render_template('student_assessment.html', form=form)


@app.route('/second-term-jhs-1-maths-student-assessment/<int:index>', methods=['GET', 'POST'])
@login_required
def edit_second_term_jhs1_maths_student(index):
    student_id = index
    form_1_student = SecondTermJHS1Mathematics.query.filter_by(id=student_id).first()
    form = StudentAssessmentForm()
    if form.validate_on_submit():
        if form_1_student:
            class_test = form.classtest.data
            mid_terms = form.midterms.data
            project_work = form.project_work.data
            examination = form.examinations.data
            form_1_student.classtest = class_test
            form_1_student.midterm_examination = mid_terms
            form_1_student.project_work = project_work
            form_1_student.end_of_term_examination = examination
            form_1_student.subtotal = float(class_test) + float(mid_terms) + float(project_work)
            form_1_student.half_subtotal = (float(class_test) + float(mid_terms) + float(project_work)) / 2
            form_1_student.half_examination = float(examination) / 2
            form_1_student.grand_total = ((float(class_test) + float(mid_terms) + float(project_work)) / 2) + (
                    float(examination) / 2)
            db.session.add(form_1_student)
            db.session.commit()
            return redirect(url_for('mathematics'))
        else:
            flash('Student not found!')

    return render_template('student_assessment.html', form=form)


@app.route('/third-term-jhs-1-maths-student-assessment/<int:index>', methods=['GET', 'POST'])
@login_required
def edit_third_term_jhs1_maths_student(index):
    student_id = index
    form_1_student = ThirdTermJHS1Mathematics.query.filter_by(id=student_id).first()
    form = StudentAssessmentForm()
    if form.validate_on_submit():
        if form_1_student:
            class_test = form.classtest.data
            mid_terms = form.midterms.data
            project_work = form.project_work.data
            examination = form.examinations.data
            form_1_student.classtest = class_test
            form_1_student.midterm_examination = mid_terms
            form_1_student.project_work = project_work
            form_1_student.end_of_term_examination = examination
            form_1_student.subtotal = float(class_test) + float(mid_terms) + float(project_work)
            form_1_student.half_subtotal = (float(class_test) + float(mid_terms) + float(project_work)) / 2
            form_1_student.half_examination = float(examination) / 2
            form_1_student.grand_total = ((float(class_test) + float(mid_terms) + float(project_work)) / 2) + (
                    float(examination) / 2)
            db.session.add(form_1_student)
            db.session.commit()
            return redirect(url_for('mathematics'))
        else:
            flash('Student not found!')

    return render_template('student_assessment.html', form=form)


@app.route('/first-term-jhs-2-maths-student-assessment/<int:index>', methods=['GET', 'POST'])
@login_required
def edit_first_term_jhs2_maths_student(index):
    student_id = index
    form_2_student = FirstTermJHS2Mathematics.query.filter_by(id=student_id).first()
    form = StudentAssessmentForm()
    if form.validate_on_submit():
        if form_2_student:
            class_test = form.classtest.data
            mid_terms = form.midterms.data
            project_work = form.project_work.data
            examination = form.examinations.data
            form_2_student.classtest = class_test
            form_2_student.midterm_examination = mid_terms
            form_2_student.project_work = project_work
            form_2_student.end_of_term_examination = examination
            form_2_student.subtotal = float(class_test) + float(mid_terms) + float(project_work)
            form_2_student.half_subtotal = (float(class_test) + float(mid_terms) + float(project_work)) / 2
            form_2_student.half_examination = float(examination) / 2
            form_2_student.grand_total = ((float(class_test) + float(mid_terms) + float(project_work)) / 2) + (
                    float(examination) / 2)
            db.session.add(form_2_student)
            db.session.commit()
            return redirect(url_for('mathematics'))
        else:
            flash('Student not found!')
            return redirect(url_for('mathematics'))

    return render_template('student_assessment.html', form=form)


@app.route('/second-term-jhs-2-maths-student-assessment/<int:index>', methods=['GET', 'POST'])
@login_required
def edit_second_term_jhs2_maths_student(index):
    student_id = index
    form_2_student = SecondTermJHS2Mathematics.query.filter_by(id=student_id).first()
    form = StudentAssessmentForm()
    if form.validate_on_submit():
        if form_2_student:
            class_test = form.classtest.data
            mid_terms = form.midterms.data
            project_work = form.project_work.data
            examination = form.examinations.data
            form_2_student.classtest = class_test
            form_2_student.midterm_examination = mid_terms
            form_2_student.project_work = project_work
            form_2_student.end_of_term_examination = examination
            form_2_student.subtotal = float(class_test) + float(mid_terms) + float(project_work)
            form_2_student.half_subtotal = (float(class_test) + float(mid_terms) + float(project_work)) / 2
            form_2_student.half_examination = float(examination) / 2
            form_2_student.grand_total = ((float(class_test) + float(mid_terms) + float(project_work)) / 2) + (
                    float(examination) / 2)
            db.session.add(form_2_student)
            db.session.commit()
            return redirect(url_for('mathematics'))
        else:
            flash('Student not found!')
            return redirect(url_for('mathematics'))

    return render_template('student_assessment.html', form=form)


@app.route('/third-term-jhs-2-maths-student-assessment/<int:index>', methods=['GET', 'POST'])
@login_required
def edit_third_term_jhs2_maths_student(index):
    student_id = index
    form_2_student = ThirdTermJHS2Mathematics.query.filter_by(id=student_id).first()
    form = StudentAssessmentForm()
    if form.validate_on_submit():
        if form_2_student:
            class_test = form.classtest.data
            mid_terms = form.midterms.data
            project_work = form.project_work.data
            examination = form.examinations.data
            form_2_student.classtest = class_test
            form_2_student.midterm_examination = mid_terms
            form_2_student.project_work = project_work
            form_2_student.end_of_term_examination = examination
            form_2_student.subtotal = float(class_test) + float(mid_terms) + float(project_work)
            form_2_student.half_subtotal = (float(class_test) + float(mid_terms) + float(project_work)) / 2
            form_2_student.half_examination = float(examination) / 2
            form_2_student.grand_total = ((float(class_test) + float(mid_terms) + float(project_work)) / 2) + (
                    float(examination) / 2)
            db.session.add(form_2_student)
            db.session.commit()
            return redirect(url_for('mathematics'))
        else:
            flash('Student not found!')
            return redirect(url_for('mathematics'))

    return render_template('student_assessment.html', form=form)


@app.route('/first-term-jhs-3-maths-student-assessment/<int:index>', methods=['GET', 'POST'])
@login_required
def edit_first_term_jhs3_maths_student(index):
    student_id = index
    form_3_student = FirstTermJHS3Mathematics.query.filter_by(id=student_id).first()
    form = StudentAssessmentForm()
    if form.validate_on_submit():
        if form_3_student:
            class_test = form.classtest.data
            mid_terms = form.midterms.data
            project_work = form.project_work.data
            examination = form.examinations.data
            form_3_student.classtest = class_test
            form_3_student.midterm_examination = mid_terms
            form_3_student.project_work = project_work
            form_3_student.end_of_term_examination = examination
            form_3_student.subtotal = float(class_test) + float(mid_terms) + float(project_work)
            form_3_student.half_subtotal = (float(class_test) + float(mid_terms) + float(project_work)) / 2
            form_3_student.half_examination = float(examination) / 2
            form_3_student.grand_total = ((float(class_test) + float(mid_terms) + float(project_work)) / 2) + (
                    float(examination) / 2)
            db.session.add(form_3_student)
            db.session.commit()
            return redirect(url_for('mathematics'))
        else:
            flash('Student not found!')
            return redirect(url_for('mathematics'))

    return render_template('student_assessment.html', form=form)


@app.route('/second-term-jhs-3-maths-student-assessment/<int:index>', methods=['GET', 'POST'])
@login_required
def edit_second_term_jhs3_maths_student(index):
    student_id = index
    form_3_student = SecondTermJHS3Mathematics.query.filter_by(id=student_id).first()
    form = StudentAssessmentForm()
    if form.validate_on_submit():
        if form_3_student:
            class_test = form.classtest.data
            mid_terms = form.midterms.data
            project_work = form.project_work.data
            examination = form.examinations.data
            form_3_student.classtest = class_test
            form_3_student.midterm_examination = mid_terms
            form_3_student.project_work = project_work
            form_3_student.end_of_term_examination = examination
            form_3_student.subtotal = float(class_test) + float(mid_terms) + float(project_work)
            form_3_student.half_subtotal = (float(class_test) + float(mid_terms) + float(project_work)) / 2
            form_3_student.half_examination = float(examination) / 2
            form_3_student.grand_total = ((float(class_test) + float(mid_terms) + float(project_work)) / 2) + (
                    float(examination) / 2)
            db.session.add(form_3_student)
            db.session.commit()
            return redirect(url_for('mathematics'))
        else:
            flash('Student not found!')
            return redirect(url_for('mathematics'))

    return render_template('student_assessment.html', form=form)


@app.route('/third-term-jhs-3-maths-student-assessment/<int:index>', methods=['GET', 'POST'])
@login_required
def edit_third_term_jhs3_maths_student(index):
    student_id = index
    form_3_student = ThirdTermJHS3Mathematics.query.filter_by(id=student_id).first()
    form = StudentAssessmentForm()
    if form.validate_on_submit():
        if form_3_student:
            class_test = form.classtest.data
            mid_terms = form.midterms.data
            project_work = form.project_work.data
            examination = form.examinations.data
            form_3_student.classtest = class_test
            form_3_student.midterm_examination = mid_terms
            form_3_student.project_work = project_work
            form_3_student.end_of_term_examination = examination
            form_3_student.subtotal = float(class_test) + float(mid_terms) + float(project_work)
            form_3_student.half_subtotal = (float(class_test) + float(mid_terms) + float(project_work)) / 2
            form_3_student.half_examination = float(examination) / 2
            form_3_student.grand_total = ((float(class_test) + float(mid_terms) + float(project_work)) / 2) + (
                    float(examination) / 2)
            db.session.add(form_3_student)
            db.session.commit()
            return redirect(url_for('mathematics'))
        else:
            flash('Student not found!')
            return redirect(url_for('mathematics'))

    return render_template('student_assessment.html', form=form)


@app.route('/integrated_science-portal')
@login_required
def science():
    form_1_first_term_students = FirstTermJHS1IntegratedScience.query.all()
    form_1_second_term_students = SecondTermJHS1IntegratedScience.query.all()
    form_1_third_term_students = ThirdTermJHS1IntegratedScience.query.all()
    form_2_first_term_students = FirstTermJHS2IntegratedScience.query.all()
    form_2_second_term_students = SecondTermJHS2IntegratedScience.query.all()
    form_2_third_term_students = ThirdTermJHS2IntegratedScience.query.all()
    form_3_first_term_students = FirstTermJHS3IntegratedScience.query.all()
    form_3_second_term_students = SecondTermJHS3IntegratedScience.query.all()
    form_3_third_term_students = ThirdTermJHS3IntegratedScience.query.all()
    return render_template('english_dashboard.html', form_1_first_term_students=form_1_first_term_students,
                           form_1_second_term_students=form_1_second_term_students,
                           form_1_third_term_students=form_1_third_term_students,
                           form_2_first_term_students=form_2_first_term_students,
                           form_2_second_term_students=form_2_second_term_students,
                           form_2_third_term_students=form_2_third_term_students,
                           form_3_first_term_students=form_3_first_term_students,
                           form_3_second_term_students=form_3_second_term_students, current_user=current_user)


@app.route('/first-term-jhs-1-science-student-assessment/<int:index>', methods=['GET', 'POST'])
@login_required
def edit_first_term_jhs1_science_student(index):
    student_id = index
    form_1_student = FirstTermJHS1IntegratedScience.query.filter_by(id=student_id).first()
    form = StudentAssessmentForm()
    if form.validate_on_submit():
        if form_1_student:
            class_test = form.classtest.data
            mid_terms = form.midterms.data
            project_work = form.project_work.data
            examination = form.examinations.data
            form_1_student.classtest = class_test
            form_1_student.midterm_examination = mid_terms
            form_1_student.project_work = project_work
            form_1_student.end_of_term_examination = examination
            form_1_student.subtotal = float(class_test) + float(mid_terms) + float(project_work)
            form_1_student.half_subtotal = (float(class_test) + float(mid_terms) + float(project_work)) / 2
            form_1_student.half_examination = float(examination) / 2
            form_1_student.grand_total = ((float(class_test) + float(mid_terms) + float(project_work)) / 2) + (
                    float(examination) / 2)
            db.session.add(form_1_student)
            db.session.commit()
            return redirect(url_for('science'))
        else:
            flash('Student not found!')

    return render_template('student_assessment.html', form=form)


@app.route('/second-term-jhs-1-science-student-assessment/<int:index>', methods=['GET', 'POST'])
@login_required
def edit_second_term_jhs1_science_student(index):
    student_id = index
    form_1_student = SecondTermJHS1IntegratedScience.query.filter_by(id=student_id).first()
    form = StudentAssessmentForm()
    if form.validate_on_submit():
        if form_1_student:
            class_test = form.classtest.data
            mid_terms = form.midterms.data
            project_work = form.project_work.data
            examination = form.examinations.data
            form_1_student.classtest = class_test
            form_1_student.midterm_examination = mid_terms
            form_1_student.project_work = project_work
            form_1_student.end_of_term_examination = examination
            form_1_student.subtotal = float(class_test) + float(mid_terms) + float(project_work)
            form_1_student.half_subtotal = (float(class_test) + float(mid_terms) + float(project_work)) / 2
            form_1_student.half_examination = float(examination) / 2
            form_1_student.grand_total = ((float(class_test) + float(mid_terms) + float(project_work)) / 2) + (
                    float(examination) / 2)
            db.session.add(form_1_student)
            db.session.commit()
            return redirect(url_for('science'))
        else:
            flash('Student not found!')

    return render_template('student_assessment.html', form=form)


@app.route('/third-term-jhs-1-science-student-assessment/<int:index>', methods=['GET', 'POST'])
@login_required
def edit_third_term_jhs1_science_student(index):
    student_id = index
    form_1_student = ThirdTermJHS1IntegratedScience.query.filter_by(id=student_id).first()
    form = StudentAssessmentForm()
    if form.validate_on_submit():
        if form_1_student:
            class_test = form.classtest.data
            mid_terms = form.midterms.data
            project_work = form.project_work.data
            examination = form.examinations.data
            form_1_student.classtest = class_test
            form_1_student.midterm_examination = mid_terms
            form_1_student.project_work = project_work
            form_1_student.end_of_term_examination = examination
            form_1_student.subtotal = float(class_test) + float(mid_terms) + float(project_work)
            form_1_student.half_subtotal = (float(class_test) + float(mid_terms) + float(project_work)) / 2
            form_1_student.half_examination = float(examination) / 2
            form_1_student.grand_total = ((float(class_test) + float(mid_terms) + float(project_work)) / 2) + (
                    float(examination) / 2)
            db.session.add(form_1_student)
            db.session.commit()
            return redirect(url_for('science'))
        else:
            flash('Student not found!')

    return render_template('student_assessment.html', form=form)


@app.route('/first-term-jhs-2-science-student-assessment/<int:index>', methods=['GET', 'POST'])
@login_required
def edit_first_term_jhs2_science_student(index):
    student_id = index
    form_2_student = FirstTermJHS2IntegratedScience.query.filter_by(id=student_id).first()
    form = StudentAssessmentForm()
    if form.validate_on_submit():
        if form_2_student:
            class_test = form.classtest.data
            mid_terms = form.midterms.data
            project_work = form.project_work.data
            examination = form.examinations.data
            form_2_student.classtest = class_test
            form_2_student.midterm_examination = mid_terms
            form_2_student.project_work = project_work
            form_2_student.end_of_term_examination = examination
            form_2_student.subtotal = float(class_test) + float(mid_terms) + float(project_work)
            form_2_student.half_subtotal = (float(class_test) + float(mid_terms) + float(project_work)) / 2
            form_2_student.half_examination = float(examination) / 2
            form_2_student.grand_total = ((float(class_test) + float(mid_terms) + float(project_work)) / 2) + (
                    float(examination) / 2)
            db.session.add(form_2_student)
            db.session.commit()
            return redirect(url_for('science'))
        else:
            flash('Student not found!')

    return render_template('student_assessment.html', form=form)


@app.route('/second-term-jhs-2-science-student-assessment/<int:index>', methods=['GET', 'POST'])
@login_required
def edit_first_term_jhs2_science_student(index):
    student_id = index
    form_2_student = SecondTermJHS2IntegratedScience.query.filter_by(id=student_id).first()
    form = StudentAssessmentForm()
    if form.validate_on_submit():
        if form_2_student:
            class_test = form.classtest.data
            mid_terms = form.midterms.data
            project_work = form.project_work.data
            examination = form.examinations.data
            form_2_student.classtest = class_test
            form_2_student.midterm_examination = mid_terms
            form_2_student.project_work = project_work
            form_2_student.end_of_term_examination = examination
            form_2_student.subtotal = float(class_test) + float(mid_terms) + float(project_work)
            form_2_student.half_subtotal = (float(class_test) + float(mid_terms) + float(project_work)) / 2
            form_2_student.half_examination = float(examination) / 2
            form_2_student.grand_total = ((float(class_test) + float(mid_terms) + float(project_work)) / 2) + (
                    float(examination) / 2)
            db.session.add(form_2_student)
            db.session.commit()
            return redirect(url_for('science'))
        else:
            flash('Student not found!')

    return render_template('student_assessment.html', form=form)


@app.route('/third-term-jhs-2-science-student-assessment/<int:index>', methods=['GET', 'POST'])
@login_required
def edit_third_term_jhs2_science_student(index):
    student_id = index
    form_2_student = ThirdTermJHS2IntegratedScience.query.filter_by(id=student_id).first()
    form = StudentAssessmentForm()
    if form.validate_on_submit():
        if form_2_student:
            class_test = form.classtest.data
            mid_terms = form.midterms.data
            project_work = form.project_work.data
            examination = form.examinations.data
            form_2_student.classtest = class_test
            form_2_student.midterm_examination = mid_terms
            form_2_student.project_work = project_work
            form_2_student.end_of_term_examination = examination
            form_2_student.subtotal = float(class_test) + float(mid_terms) + float(project_work)
            form_2_student.half_subtotal = (float(class_test) + float(mid_terms) + float(project_work)) / 2
            form_2_student.half_examination = float(examination) / 2
            form_2_student.grand_total = ((float(class_test) + float(mid_terms) + float(project_work)) / 2) + (
                    float(examination) / 2)
            db.session.add(form_2_student)
            db.session.commit()
            return redirect(url_for('science'))
        else:
            flash('Student not found!')

    return render_template('student_assessment.html', form=form)


@app.route('/first-term-jhs-3-science-student-assessment/<int:index>', methods=['GET', 'POST'])
@login_required
def edit_first_term_jhs3_science_student(index):
    student_id = index
    form_3_student = FirstTermJHS1IntegratedScience.query.filter_by(id=student_id).first()
    form = StudentAssessmentForm()
    if form.validate_on_submit():
        if form_3_student:
            class_test = form.classtest.data
            mid_terms = form.midterms.data
            project_work = form.project_work.data
            examination = form.examinations.data
            form_3_student.classtest = class_test
            form_3_student.midterm_examination = mid_terms
            form_3_student.project_work = project_work
            form_3_student.end_of_term_examination = examination
            form_3_student.subtotal = float(class_test) + float(mid_terms) + float(project_work)
            form_3_student.half_subtotal = (float(class_test) + float(mid_terms) + float(project_work)) / 2
            form_3_student.half_examination = float(examination) / 2
            form_3_student.grand_total = ((float(class_test) + float(mid_terms) + float(project_work)) / 2) + (
                    float(examination) / 2)
            db.session.add(form_3_student)
            db.session.commit()
            return redirect(url_for('science'))
        else:
            flash('Student not found!')

    return render_template('student_assessment.html', form=form)


@app.route('/second-term-jhs-3-science-student-assessment/<int:index>', methods=['GET', 'POST'])
@login_required
def edit_second_term_jhs3_science_student(index):
    student_id = index
    form_3_student = SecondTermJHS1IntegratedScience.query.filter_by(id=student_id).first()
    form = StudentAssessmentForm()
    if form.validate_on_submit():
        if form_3_student:
            class_test = form.classtest.data
            mid_terms = form.midterms.data
            project_work = form.project_work.data
            examination = form.examinations.data
            form_3_student.classtest = class_test
            form_3_student.midterm_examination = mid_terms
            form_3_student.project_work = project_work
            form_3_student.end_of_term_examination = examination
            form_3_student.subtotal = float(class_test) + float(mid_terms) + float(project_work)
            form_3_student.half_subtotal = (float(class_test) + float(mid_terms) + float(project_work)) / 2
            form_3_student.half_examination = float(examination) / 2
            form_3_student.grand_total = ((float(class_test) + float(mid_terms) + float(project_work)) / 2) + (
                    float(examination) / 2)
            db.session.add(form_3_student)
            db.session.commit()
            return redirect(url_for('science'))
        else:
            flash('Student not found!')

    return render_template('student_assessment.html', form=form)


@app.route('/third-term-jhs-3-science-student-assessment/<int:index>', methods=['GET', 'POST'])
@login_required
def edit_third_term_jhs3_science_student(index):
    student_id = index
    form_3_student = ThirdTermJHS1IntegratedScience.query.filter_by(id=student_id).first()
    form = StudentAssessmentForm()
    if form.validate_on_submit():
        if form_3_student:
            class_test = form.classtest.data
            mid_terms = form.midterms.data
            project_work = form.project_work.data
            examination = form.examinations.data
            form_3_student.classtest = class_test
            form_3_student.midterm_examination = mid_terms
            form_3_student.project_work = project_work
            form_3_student.end_of_term_examination = examination
            form_3_student.subtotal = float(class_test) + float(mid_terms) + float(project_work)
            form_3_student.half_subtotal = (float(class_test) + float(mid_terms) + float(project_work)) / 2
            form_3_student.half_examination = float(examination) / 2
            form_3_student.grand_total = ((float(class_test) + float(mid_terms) + float(project_work)) / 2) + (
                    float(examination) / 2)
            db.session.add(form_3_student)
            db.session.commit()
            return redirect(url_for('science'))
        else:
            flash('Student not found!')

    return render_template('student_assessment.html', form=form)


@app.route('/social-studies-portal')
@login_required
def social():
    form_1_first_term_students = FirstTermJHS1SocialStudies.query.all()
    form_1_second_term_students = SecondTermJHS1SocialStudies.query.all()
    form_1_third_term_students = ThirdTermJHS1SocialStudies.query.all()
    form_2_first_term_students = FirstTermJHS2SocialStudies.query.all()
    form_2_second_term_students = SecondTermJHS2SocialStudies.query.all()
    form_2_third_term_students = ThirdTermJHS2SocialStudies.query.all()
    form_3_first_term_students = FirstTermJHS3SocialStudies.query.all()
    form_3_second_term_students = SecondTermJHS3SocialStudies.query.all()
    form_3_third_term_students = ThirdTermJHS3SocialStudies.query.all()
    return render_template('english_dashboard.html', form_1_first_term_students=form_1_first_term_students,
                           form_1_second_term_students=form_1_second_term_students,
                           form_1_third_term_students=form_1_third_term_students,
                           form_2_first_term_students=form_2_first_term_students,
                           form_2_second_term_students=form_2_second_term_students,
                           form_2_third_term_students=form_2_third_term_students,
                           form_3_first_term_students=form_3_first_term_students,
                           form_3_second_term_students=form_3_second_term_students, current_user=current_user)


@app.route('/first-term-jhs-1-social-studies-student-assessment/<int:index>', methods=['GET', 'POST'])
@login_required
def edit_first_term_jhs1_social_studies_student(index):
    student_id = index
    form_1_student = FirstTermJHS1SocialStudies.query.filter_by(id=student_id).first()
    form = StudentAssessmentForm()
    if form.validate_on_submit():
        if form_1_student:
            class_test = form.classtest.data
            mid_terms = form.midterms.data
            project_work = form.project_work.data
            examination = form.examinations.data
            form_1_student.classtest = class_test
            form_1_student.midterm_examination = mid_terms
            form_1_student.project_work = project_work
            form_1_student.end_of_term_examination = examination
            form_1_student.subtotal = float(class_test) + float(mid_terms) + float(project_work)
            form_1_student.half_subtotal = (float(class_test) + float(mid_terms) + float(project_work)) / 2
            form_1_student.half_examination = float(examination) / 2
            form_1_student.grand_total = ((float(class_test) + float(mid_terms) + float(project_work)) / 2) + (
                    float(examination) / 2)
            db.session.add(form_1_student)
            db.session.commit()
            return redirect(url_for('social'))
        else:
            flash('Student not found!')

    return render_template('student_assessment.html', form=form)


@app.route('/second-term-jhs-1-social-studies-student-assessment/<int:index>', methods=['GET', 'POST'])
@login_required
def edit_second_term_jhs1_social_studies_student(index):
    student_id = index
    form_1_student = SecondTermJHS1SocialStudies.query.filter_by(id=student_id).first()
    form = StudentAssessmentForm()
    if form.validate_on_submit():
        if form_1_student:
            class_test = form.classtest.data
            mid_terms = form.midterms.data
            project_work = form.project_work.data
            examination = form.examinations.data
            form_1_student.classtest = class_test
            form_1_student.midterm_examination = mid_terms
            form_1_student.project_work = project_work
            form_1_student.end_of_term_examination = examination
            form_1_student.subtotal = float(class_test) + float(mid_terms) + float(project_work)
            form_1_student.half_subtotal = (float(class_test) + float(mid_terms) + float(project_work)) / 2
            form_1_student.half_examination = float(examination) / 2
            form_1_student.grand_total = ((float(class_test) + float(mid_terms) + float(project_work)) / 2) + (
                    float(examination) / 2)
            db.session.add(form_1_student)
            db.session.commit()
            return redirect(url_for('social'))
        else:
            flash('Student not found!')

    return render_template('student_assessment.html', form=form)


@app.route('/third-term-jhs-1-social-studies-student-assessment/<int:index>', methods=['GET', 'POST'])
@login_required
def edit_third_term_jhs1_social_studies_student(index):
    student_id = index
    form_1_student = ThirdTermJHS1SocialStudies.query.filter_by(id=student_id).first()
    form = StudentAssessmentForm()
    if form.validate_on_submit():
        if form_1_student:
            class_test = form.classtest.data
            mid_terms = form.midterms.data
            project_work = form.project_work.data
            examination = form.examinations.data
            form_1_student.classtest = class_test
            form_1_student.midterm_examination = mid_terms
            form_1_student.project_work = project_work
            form_1_student.end_of_term_examination = examination
            form_1_student.subtotal = float(class_test) + float(mid_terms) + float(project_work)
            form_1_student.half_subtotal = (float(class_test) + float(mid_terms) + float(project_work)) / 2
            form_1_student.half_examination = float(examination) / 2
            form_1_student.grand_total = ((float(class_test) + float(mid_terms) + float(project_work)) / 2) + (
                    float(examination) / 2)
            db.session.add(form_1_student)
            db.session.commit()
            return redirect(url_for('social'))
        else:
            flash('Student not found!')

    return render_template('student_assessment.html', form=form)


@app.route('/first-term_jhs-2-social-studies-student-assessment/<int:index>', methods=['GET', 'POST'])
@login_required
def edit_first_term_jhs2_social_studies_student(index):
    student_id = index
    form_2_student = FirstTermJHS2SocialStudies.query.filter_by(id=student_id).first()
    form = StudentAssessmentForm()
    if form.validate_on_submit():
        if form_2_student:
            class_test = form.classtest.data
            mid_terms = form.midterms.data
            project_work = form.project_work.data
            examination = form.examinations.data
            form_2_student.classtest = class_test
            form_2_student.midterm_examination = mid_terms
            form_2_student.project_work = project_work
            form_2_student.end_of_term_examination = examination
            form_2_student.subtotal = float(class_test) + float(mid_terms) + float(project_work)
            form_2_student.half_subtotal = (float(class_test) + float(mid_terms) + float(project_work)) / 2
            form_2_student.half_examination = float(examination) / 2
            form_2_student.grand_total = ((float(class_test) + float(mid_terms) + float(project_work)) / 2) + (
                    float(examination) / 2)
            db.session.add(form_2_student)
            db.session.commit()
            return redirect(url_for('social'))
        else:
            flash('Student not found!')

    return render_template('student_assessment.html', form=form)


@app.route('/second-term_jhs-2-social-studies-student-assessment/<int:index>', methods=['GET', 'POST'])
@login_required
def edit_second_term_jhs2_social_studies_student(index):
    student_id = index
    form_2_student = SecondTermJHS2SocialStudies.query.filter_by(id=student_id).first()
    form = StudentAssessmentForm()
    if form.validate_on_submit():
        if form_2_student:
            class_test = form.classtest.data
            mid_terms = form.midterms.data
            project_work = form.project_work.data
            examination = form.examinations.data
            form_2_student.classtest = class_test
            form_2_student.midterm_examination = mid_terms
            form_2_student.project_work = project_work
            form_2_student.end_of_term_examination = examination
            form_2_student.subtotal = float(class_test) + float(mid_terms) + float(project_work)
            form_2_student.half_subtotal = (float(class_test) + float(mid_terms) + float(project_work)) / 2
            form_2_student.half_examination = float(examination) / 2
            form_2_student.grand_total = ((float(class_test) + float(mid_terms) + float(project_work)) / 2) + (
                    float(examination) / 2)
            db.session.add(form_2_student)
            db.session.commit()
            return redirect(url_for('social'))
        else:
            flash('Student not found!')

    return render_template('student_assessment.html', form=form)


@app.route('/third-term_jhs-2-social-studies-student-assessment/<int:index>', methods=['GET', 'POST'])
@login_required
def edit_third_term_jhs2_social_studies_student(index):
    student_id = index
    form_2_student = ThirdTermJHS2SocialStudies.query.filter_by(id=student_id).first()
    form = StudentAssessmentForm()
    if form.validate_on_submit():
        if form_2_student:
            class_test = form.classtest.data
            mid_terms = form.midterms.data
            project_work = form.project_work.data
            examination = form.examinations.data
            form_2_student.classtest = class_test
            form_2_student.midterm_examination = mid_terms
            form_2_student.project_work = project_work
            form_2_student.end_of_term_examination = examination
            form_2_student.subtotal = float(class_test) + float(mid_terms) + float(project_work)
            form_2_student.half_subtotal = (float(class_test) + float(mid_terms) + float(project_work)) / 2
            form_2_student.half_examination = float(examination) / 2
            form_2_student.grand_total = ((float(class_test) + float(mid_terms) + float(project_work)) / 2) + (
                    float(examination) / 2)
            db.session.add(form_2_student)
            db.session.commit()
            return redirect(url_for('social'))
        else:
            flash('Student not found!')

    return render_template('student_assessment.html', form=form)


@app.route('/first-term-jhs-3-social-studies-student-assessment/<int:index>', methods=['GET', 'POST'])
@login_required
def edit_first_term_jhs3_social_studies_student(index):
    student_id = index
    form_3_student = FirstTermJHS3SocialStudies.query.filter_by(id=student_id).first()
    form = StudentAssessmentForm()
    if form.validate_on_submit():
        if form_3_student:
            class_test = form.classtest.data
            mid_terms = form.midterms.data
            project_work = form.project_work.data
            examination = form.examinations.data
            form_3_student.classtest = class_test
            form_3_student.midterm_examination = mid_terms
            form_3_student.project_work = project_work
            form_3_student.end_of_term_examination = examination
            form_3_student.subtotal = float(class_test) + float(mid_terms) + float(project_work)
            form_3_student.half_subtotal = (float(class_test) + float(mid_terms) + float(project_work)) / 2
            form_3_student.half_examination = float(examination) / 2
            form_3_student.grand_total = ((float(class_test) + float(mid_terms) + float(project_work)) / 2) + (
                    float(examination) / 2)
            db.session.add(form_3_student)
            db.session.commit()
            return redirect(url_for('social'))
        else:
            flash('Student not found!')

    return render_template('student_assessment.html', form=form)


@app.route('/second-term-jhs-3-social-studies-student-assessment/<int:index>', methods=['GET', 'POST'])
@login_required
def edit_second_term_jhs3_social_studies_student(index):
    student_id = index
    form_3_student = SecondTermJHS3SocialStudies.query.filter_by(id=student_id).first()
    form = StudentAssessmentForm()
    if form.validate_on_submit():
        if form_3_student:
            class_test = form.classtest.data
            mid_terms = form.midterms.data
            project_work = form.project_work.data
            examination = form.examinations.data
            form_3_student.classtest = class_test
            form_3_student.midterm_examination = mid_terms
            form_3_student.project_work = project_work
            form_3_student.end_of_term_examination = examination
            form_3_student.subtotal = float(class_test) + float(mid_terms) + float(project_work)
            form_3_student.half_subtotal = (float(class_test) + float(mid_terms) + float(project_work)) / 2
            form_3_student.half_examination = float(examination) / 2
            form_3_student.grand_total = ((float(class_test) + float(mid_terms) + float(project_work)) / 2) + (
                    float(examination) / 2)
            db.session.add(form_3_student)
            db.session.commit()
            return redirect(url_for('social'))
        else:
            flash('Student not found!')

    return render_template('student_assessment.html', form=form)


@app.route('/third-term-jhs-3-social-studies-student-assessment/<int:index>', methods=['GET', 'POST'])
@login_required
def edit_third_term_jhs3_social_studies_student(index):
    student_id = index
    form_3_student = ThirdTermJHS3SocialStudies.query.filter_by(id=student_id).first()
    form = StudentAssessmentForm()
    if form.validate_on_submit():
        if form_3_student:
            class_test = form.classtest.data
            mid_terms = form.midterms.data
            project_work = form.project_work.data
            examination = form.examinations.data
            form_3_student.classtest = class_test
            form_3_student.midterm_examination = mid_terms
            form_3_student.project_work = project_work
            form_3_student.end_of_term_examination = examination
            form_3_student.subtotal = float(class_test) + float(mid_terms) + float(project_work)
            form_3_student.half_subtotal = (float(class_test) + float(mid_terms) + float(project_work)) / 2
            form_3_student.half_examination = float(examination) / 2
            form_3_student.grand_total = ((float(class_test) + float(mid_terms) + float(project_work)) / 2) + (
                    float(examination) / 2)
            db.session.add(form_3_student)
            db.session.commit()
            return redirect(url_for('social'))
        else:
            flash('Student not found!')

    return render_template('student_assessment.html', form=form)


@app.route('/computing-portal')
@login_required
def computing():
    form_1_first_term_students = FirstTermJHS1Computing.query.all()
    form_1_second_term_students = SecondTermJHS1Computing.query.all()
    form_1_third_term_students = ThirdTermJHS1Computing.query.all()
    form_2_first_term_students = FirstTermJHS2Computing.query.all()
    form_2_second_term_students = SecondTermJHS2Computing.query.all()
    form_2_third_term_students = ThirdTermJHS2Computing.query.all()
    form_3_first_term_students = FirstTermJHS3Computing.query.all()
    form_3_second_term_students = SecondTermJHS3Computing.query.all()
    form_3_third_term_students = ThirdTermJHS3Computing.query.all()
    return render_template('english_dashboard.html', form_1_first_term_students=form_1_first_term_students,
                           form_1_second_term_students=form_1_second_term_students,
                           form_1_third_term_students=form_1_third_term_students,
                           form_2_first_term_students=form_2_first_term_students,
                           form_2_second_term_students=form_2_second_term_students,
                           form_2_third_term_students=form_2_third_term_students,
                           form_3_first_term_students=form_3_first_term_students,
                           form_3_second_term_students=form_3_second_term_students, current_user=current_user)


@app.route('/first-term-jhs-1-computing-student-assessment/<int:index>', methods=['GET', 'POST'])
@login_required
def edit_first_term_jhs1_computing_student(index):
    student_id = index
    form_1_student = FirstTermJHS1Computing.query.filter_by(id=student_id).first()
    form = StudentAssessmentForm()
    if form.validate_on_submit():
        if form_1_student:
            class_test = form.classtest.data
            mid_terms = form.midterms.data
            project_work = form.project_work.data
            examination = form.examinations.data
            form_1_student.classtest = class_test
            form_1_student.midterm_examination = mid_terms
            form_1_student.project_work = project_work
            form_1_student.end_of_term_examination = examination
            form_1_student.subtotal = float(class_test) + float(mid_terms) + float(project_work)
            form_1_student.half_subtotal = (float(class_test) + float(mid_terms) + float(project_work)) / 2
            form_1_student.half_examination = float(examination) / 2
            form_1_student.grand_total = ((float(class_test) + float(mid_terms) + float(project_work)) / 2) + (
                    float(examination) / 2)
            db.session.add(form_1_student)
            db.session.commit()
            return redirect(url_for('computing'))
        else:
            flash('Student not found!')

    return render_template('student_assessment.html', form=form)


@app.route('/second-term-jhs-1-computing-student-assessment/<int:index>', methods=['GET', 'POST'])
@login_required
def edit_second_term_jhs1_computing_student(index):
    student_id = index
    form_1_student = SecondTermJHS1Computing.query.filter_by(id=student_id).first()
    form = StudentAssessmentForm()
    if form.validate_on_submit():
        if form_1_student:
            class_test = form.classtest.data
            mid_terms = form.midterms.data
            project_work = form.project_work.data
            examination = form.examinations.data
            form_1_student.classtest = class_test
            form_1_student.midterm_examination = mid_terms
            form_1_student.project_work = project_work
            form_1_student.end_of_term_examination = examination
            form_1_student.subtotal = float(class_test) + float(mid_terms) + float(project_work)
            form_1_student.half_subtotal = (float(class_test) + float(mid_terms) + float(project_work)) / 2
            form_1_student.half_examination = float(examination) / 2
            form_1_student.grand_total = ((float(class_test) + float(mid_terms) + float(project_work)) / 2) + (
                    float(examination) / 2)
            db.session.add(form_1_student)
            db.session.commit()
            return redirect(url_for('computing'))
        else:
            flash('Student not found!')

    return render_template('student_assessment.html', form=form)


@app.route('/third-term-jhs-1-computing-student-assessment/<int:index>', methods=['GET', 'POST'])
@login_required
def edit_third_term_jhs1_computing_student(index):
    student_id = index
    form_1_student = ThirdTermJHS1Computing.query.filter_by(id=student_id).first()
    form = StudentAssessmentForm()
    if form.validate_on_submit():
        if form_1_student:
            class_test = form.classtest.data
            mid_terms = form.midterms.data
            project_work = form.project_work.data
            examination = form.examinations.data
            form_1_student.classtest = class_test
            form_1_student.midterm_examination = mid_terms
            form_1_student.project_work = project_work
            form_1_student.end_of_term_examination = examination
            form_1_student.subtotal = float(class_test) + float(mid_terms) + float(project_work)
            form_1_student.half_subtotal = (float(class_test) + float(mid_terms) + float(project_work)) / 2
            form_1_student.half_examination = float(examination) / 2
            form_1_student.grand_total = ((float(class_test) + float(mid_terms) + float(project_work)) / 2) + (
                    float(examination) / 2)
            db.session.add(form_1_student)
            db.session.commit()
            return redirect(url_for('computing'))
        else:
            flash('Student not found!')

    return render_template('student_assessment.html', form=form)


@app.route('/first-term-jhs-2-computing-student-assessment/<int:index>', methods=['GET', 'POST'])
@login_required
def edit_first_term_jhs2_computing_student(index):
    student_id = index
    form_2_student = FirstTermJHS2Computing.query.filter_by(id=student_id).first()
    form = StudentAssessmentForm()
    if form.validate_on_submit():
        if form_2_student:
            class_test = form.classtest.data
            mid_terms = form.midterms.data
            project_work = form.project_work.data
            examination = form.examinations.data
            form_2_student.classtest = class_test
            form_2_student.midterm_examination = mid_terms
            form_2_student.project_work = project_work
            form_2_student.end_of_term_examination = examination
            form_2_student.subtotal = float(class_test) + float(mid_terms) + float(project_work)
            form_2_student.half_subtotal = (float(class_test) + float(mid_terms) + float(project_work)) / 2
            form_2_student.half_examination = float(examination) / 2
            form_2_student.grand_total = ((float(class_test) + float(mid_terms) + float(project_work)) / 2) + (
                    float(examination) / 2)
            db.session.add(form_2_student)
            db.session.commit()
            return redirect(url_for('computing'))
        else:
            flash('Student not found!')

    return render_template('student_assessment.html', form=form)


@app.route('/second-term-jhs-2-computing-student-assessment/<int:index>', methods=['GET', 'POST'])
@login_required
def edit_second_term_jhs2_computing_student(index):
    student_id = index
    form_2_student = SecondTermJHS2Computing.query.filter_by(id=student_id).first()
    form = StudentAssessmentForm()
    if form.validate_on_submit():
        if form_2_student:
            class_test = form.classtest.data
            mid_terms = form.midterms.data
            project_work = form.project_work.data
            examination = form.examinations.data
            form_2_student.classtest = class_test
            form_2_student.midterm_examination = mid_terms
            form_2_student.project_work = project_work
            form_2_student.end_of_term_examination = examination
            form_2_student.subtotal = float(class_test) + float(mid_terms) + float(project_work)
            form_2_student.half_subtotal = (float(class_test) + float(mid_terms) + float(project_work)) / 2
            form_2_student.half_examination = float(examination) / 2
            form_2_student.grand_total = ((float(class_test) + float(mid_terms) + float(project_work)) / 2) + (
                    float(examination) / 2)
            db.session.add(form_2_student)
            db.session.commit()
            return redirect(url_for('computing'))
        else:
            flash('Student not found!')

    return render_template('student_assessment.html', form=form)


@app.route('/third-term-jhs-2-computing-student-assessment/<int:index>', methods=['GET', 'POST'])
@login_required
def edit_third_term_jhs2_computing_student(index):
    student_id = index
    form_2_student = ThirdTermJHS2Computing.query.filter_by(id=student_id).first()
    form = StudentAssessmentForm()
    if form.validate_on_submit():
        if form_2_student:
            class_test = form.classtest.data
            mid_terms = form.midterms.data
            project_work = form.project_work.data
            examination = form.examinations.data
            form_2_student.classtest = class_test
            form_2_student.midterm_examination = mid_terms
            form_2_student.project_work = project_work
            form_2_student.end_of_term_examination = examination
            form_2_student.subtotal = float(class_test) + float(mid_terms) + float(project_work)
            form_2_student.half_subtotal = (float(class_test) + float(mid_terms) + float(project_work)) / 2
            form_2_student.half_examination = float(examination) / 2
            form_2_student.grand_total = ((float(class_test) + float(mid_terms) + float(project_work)) / 2) + (
                    float(examination) / 2)
            db.session.add(form_2_student)
            db.session.commit()
            return redirect(url_for('computing'))
        else:
            flash('Student not found!')

    return render_template('student_assessment.html', form=form)


@app.route('/first-term-jhs-3-computing-student-assessment/<int:index>', methods=['GET', 'POST'])
@login_required
def edit_first_term_jhs3_computing_student(index):
    student_id = index
    form_3_student = FirstTermJHS3Computing.query.filter_by(id=student_id).first()
    form = StudentAssessmentForm()
    if form.validate_on_submit():
        if form_3_student:
            class_test = form.classtest.data
            mid_terms = form.midterms.data
            project_work = form.project_work.data
            examination = form.examinations.data
            form_3_student.classtest = class_test
            form_3_student.midterm_examination = mid_terms
            form_3_student.project_work = project_work
            form_3_student.end_of_term_examination = examination
            form_3_student.subtotal = float(class_test) + float(mid_terms) + float(project_work)
            form_3_student.half_subtotal = (float(class_test) + float(mid_terms) + float(project_work)) / 2
            form_3_student.half_examination = float(examination) / 2
            form_3_student.grand_total = ((float(class_test) + float(mid_terms) + float(project_work)) / 2) + (
                    float(examination) / 2)
            db.session.add(form_3_student)
            db.session.commit()
            return redirect(url_for('computing'))
        else:
            flash('Student not found!')

    return render_template('student_assessment.html', form=form)


@app.route('/second-term-jhs-3-computing-student-assessment/<int:index>', methods=['GET', 'POST'])
@login_required
def edit_second_term_jhs3_computing_student(index):
    student_id = index
    form_3_student = SecondTermJHS3Computing.query.filter_by(id=student_id).first()
    form = StudentAssessmentForm()
    if form.validate_on_submit():
        if form_3_student:
            class_test = form.classtest.data
            mid_terms = form.midterms.data
            project_work = form.project_work.data
            examination = form.examinations.data
            form_3_student.classtest = class_test
            form_3_student.midterm_examination = mid_terms
            form_3_student.project_work = project_work
            form_3_student.end_of_term_examination = examination
            form_3_student.subtotal = float(class_test) + float(mid_terms) + float(project_work)
            form_3_student.half_subtotal = (float(class_test) + float(mid_terms) + float(project_work)) / 2
            form_3_student.half_examination = float(examination) / 2
            form_3_student.grand_total = ((float(class_test) + float(mid_terms) + float(project_work)) / 2) + (
                    float(examination) / 2)
            db.session.add(form_3_student)
            db.session.commit()
            return redirect(url_for('computing'))
        else:
            flash('Student not found!')

    return render_template('student_assessment.html', form=form)


@app.route('/third-term-jhs-3-computing-student-assessment/<int:index>', methods=['GET', 'POST'])
@login_required
def edit_third_term_jhs3_computing_student(index):
    student_id = index
    form_3_student = ThirdTermJHS3Computing.query.filter_by(id=student_id).first()
    form = StudentAssessmentForm()
    if form.validate_on_submit():
        if form_3_student:
            class_test = form.classtest.data
            mid_terms = form.midterms.data
            project_work = form.project_work.data
            examination = form.examinations.data
            form_3_student.classtest = class_test
            form_3_student.midterm_examination = mid_terms
            form_3_student.project_work = project_work
            form_3_student.end_of_term_examination = examination
            form_3_student.subtotal = float(class_test) + float(mid_terms) + float(project_work)
            form_3_student.half_subtotal = (float(class_test) + float(mid_terms) + float(project_work)) / 2
            form_3_student.half_examination = float(examination) / 2
            form_3_student.grand_total = ((float(class_test) + float(mid_terms) + float(project_work)) / 2) + (
                    float(examination) / 2)
            db.session.add(form_3_student)
            db.session.commit()
            return redirect(url_for('computing'))
        else:
            flash('Student not found!')

    return render_template('student_assessment.html', form=form)


@app.route('/rme-portal')
@login_required
def rme():
    form_1_first_term_students = FirstTermJHS1ReligiousMoralEducation.query.all()
    form_1_second_term_students = SecondTermJHS1ReligiousMoralEducation.query.all()
    form_1_third_term_students = ThirdTermJHS1ReligiousMoralEducation.query.all()
    form_2_first_term_students = FirstTermJHS2ReligiousMoralEducation.query.all()
    form_2_second_term_students = SecondTermJHS2ReligiousMoralEducation.query.all()
    form_2_third_term_students = ThirdTermJHS2ReligiousMoralEducation.query.all()
    form_3_first_term_students = FirstTermJHS3ReligiousMoralEducation.query.all()
    form_3_second_term_students = SecondTermJHS3ReligiousMoralEducation.query.all()
    form_3_third_term_students = ThirdTermJHS3ReligiousMoralEducation.query.all()
    return render_template('english_dashboard.html', form_1_first_term_students=form_1_first_term_students,
                           form_1_second_term_students=form_1_second_term_students,
                           form_1_third_term_students=form_1_third_term_students,
                           form_2_first_term_students=form_2_first_term_students,
                           form_2_second_term_students=form_2_second_term_students,
                           form_2_third_term_students=form_2_third_term_students,
                           form_3_first_term_students=form_3_first_term_students,
                           form_3_second_term_students=form_3_second_term_students, current_user=current_user)


@app.route('/first-term-jhs-1-rme-student-assessment/<int:index>', methods=['GET', 'POST'])
@login_required
def edit_first_term_jhs1_rme_student(index):
    student_id = index
    form_1_student = FirstTermJHS1ReligiousMoralEducation.query.filter_by(id=student_id).first()
    form = StudentAssessmentForm()
    if form.validate_on_submit():
        if form_1_student:
            class_test = form.classtest.data
            mid_terms = form.midterms.data
            project_work = form.project_work.data
            examination = form.examinations.data
            form_1_student.classtest = class_test
            form_1_student.midterm_examination = mid_terms
            form_1_student.project_work = project_work
            form_1_student.end_of_term_examination = examination
            form_1_student.subtotal = float(class_test) + float(mid_terms) + float(project_work)
            form_1_student.half_subtotal = (float(class_test) + float(mid_terms) + float(project_work)) / 2
            form_1_student.half_examination = float(examination) / 2
            form_1_student.grand_total = ((float(class_test) + float(mid_terms) + float(project_work)) / 2) + (
                    float(examination) / 2)
            db.session.add(form_1_student)
            db.session.commit()
            return redirect(url_for('rme'))
        else:
            flash('Student not found!')

    return render_template('student_assessment.html', form=form)


@app.route('/second-term-jhs-1-rme-student-assessment/<int:index>', methods=['GET', 'POST'])
@login_required
def edit_second_term_jhs1_rme_student(index):
    student_id = index
    form_1_student = SecondTermJHS1ReligiousMoralEducation.query.filter_by(id=student_id).first()
    form = StudentAssessmentForm()
    if form.validate_on_submit():
        if form_1_student:
            class_test = form.classtest.data
            mid_terms = form.midterms.data
            project_work = form.project_work.data
            examination = form.examinations.data
            form_1_student.classtest = class_test
            form_1_student.midterm_examination = mid_terms
            form_1_student.project_work = project_work
            form_1_student.end_of_term_examination = examination
            form_1_student.subtotal = float(class_test) + float(mid_terms) + float(project_work)
            form_1_student.half_subtotal = (float(class_test) + float(mid_terms) + float(project_work)) / 2
            form_1_student.half_examination = float(examination) / 2
            form_1_student.grand_total = ((float(class_test) + float(mid_terms) + float(project_work)) / 2) + (
                    float(examination) / 2)
            db.session.add(form_1_student)
            db.session.commit()
            return redirect(url_for('rme'))
        else:
            flash('Student not found!')

    return render_template('student_assessment.html', form=form)


@app.route('/third-term-jhs-1-rme-student-assessment/<int:index>', methods=['GET', 'POST'])
@login_required
def edit_third_term_jhs1_rme_student(index):
    student_id = index
    form_1_student = ThirdTermJHS1ReligiousMoralEducation.query.filter_by(id=student_id).first()
    form = StudentAssessmentForm()
    if form.validate_on_submit():
        if form_1_student:
            class_test = form.classtest.data
            mid_terms = form.midterms.data
            project_work = form.project_work.data
            examination = form.examinations.data
            form_1_student.classtest = class_test
            form_1_student.midterm_examination = mid_terms
            form_1_student.project_work = project_work
            form_1_student.end_of_term_examination = examination
            form_1_student.subtotal = float(class_test) + float(mid_terms) + float(project_work)
            form_1_student.half_subtotal = (float(class_test) + float(mid_terms) + float(project_work)) / 2
            form_1_student.half_examination = float(examination) / 2
            form_1_student.grand_total = ((float(class_test) + float(mid_terms) + float(project_work)) / 2) + (
                    float(examination) / 2)
            db.session.add(form_1_student)
            db.session.commit()
            return redirect(url_for('rme'))
        else:
            flash('Student not found!')

    return render_template('student_assessment.html', form=form)


@app.route('/first-term-jhs-2-rme-student-assessment/<int:index>', methods=['GET', 'POST'])
@login_required
def edit_first_term_jhs2_rme_student(index):
    student_id = index
    form_2_student = FirstTermJHS2ReligiousMoralEducation.query.filter_by(id=student_id).first()
    form = StudentAssessmentForm()
    if form.validate_on_submit():
        if form_2_student:
            class_test = form.classtest.data
            mid_terms = form.midterms.data
            project_work = form.project_work.data
            examination = form.examinations.data
            form_2_student.classtest = class_test
            form_2_student.midterm_examination = mid_terms
            form_2_student.project_work = project_work
            form_2_student.end_of_term_examination = examination
            form_2_student.subtotal = float(class_test) + float(mid_terms) + float(project_work)
            form_2_student.half_subtotal = (float(class_test) + float(mid_terms) + float(project_work)) / 2
            form_2_student.half_examination = float(examination) / 2
            form_2_student.grand_total = ((float(class_test) + float(mid_terms) + float(project_work)) / 2) + (
                    float(examination) / 2)
            db.session.add(form_2_student)
            db.session.commit()
            return redirect(url_for('rme'))
        else:
            flash('Student not found!')

    return render_template('student_assessment.html', form=form)


@app.route('/second-term-jhs-2-rme-student-assessment/<int:index>', methods=['GET', 'POST'])
@login_required
def edit_second_term_jhs2_rme_student(index):
    student_id = index
    form_2_student = SecondTermJHS2ReligiousMoralEducation.query.filter_by(id=student_id).first()
    form = StudentAssessmentForm()
    if form.validate_on_submit():
        if form_2_student:
            class_test = form.classtest.data
            mid_terms = form.midterms.data
            project_work = form.project_work.data
            examination = form.examinations.data
            form_2_student.classtest = class_test
            form_2_student.midterm_examination = mid_terms
            form_2_student.project_work = project_work
            form_2_student.end_of_term_examination = examination
            form_2_student.subtotal = float(class_test) + float(mid_terms) + float(project_work)
            form_2_student.half_subtotal = (float(class_test) + float(mid_terms) + float(project_work)) / 2
            form_2_student.half_examination = float(examination) / 2
            form_2_student.grand_total = ((float(class_test) + float(mid_terms) + float(project_work)) / 2) + (
                    float(examination) / 2)
            db.session.add(form_2_student)
            db.session.commit()
            return redirect(url_for('rme'))
        else:
            flash('Student not found!')

    return render_template('student_assessment.html', form=form)


@app.route('/third-term-jhs-2-rme-student-assessment/<int:index>', methods=['GET', 'POST'])
@login_required
def edit_third_term_jhs2_rme_student(index):
    student_id = index
    form_2_student = ThirdTermJHS2ReligiousMoralEducation.query.filter_by(id=student_id).first()
    form = StudentAssessmentForm()
    if form.validate_on_submit():
        if form_2_student:
            class_test = form.classtest.data
            mid_terms = form.midterms.data
            project_work = form.project_work.data
            examination = form.examinations.data
            form_2_student.classtest = class_test
            form_2_student.midterm_examination = mid_terms
            form_2_student.project_work = project_work
            form_2_student.end_of_term_examination = examination
            form_2_student.subtotal = float(class_test) + float(mid_terms) + float(project_work)
            form_2_student.half_subtotal = (float(class_test) + float(mid_terms) + float(project_work)) / 2
            form_2_student.half_examination = float(examination) / 2
            form_2_student.grand_total = ((float(class_test) + float(mid_terms) + float(project_work)) / 2) + (
                    float(examination) / 2)
            db.session.add(form_2_student)
            db.session.commit()
            return redirect(url_for('rme'))
        else:
            flash('Student not found!')

    return render_template('student_assessment.html', form=form)


@app.route('/first-term-jhs-3-rme-student-assessment/<int:index>', methods=['GET', 'POST'])
@login_required
def edit_first_term_jhs3_rme_student(index):
    student_id = index
    form_3_student = FirstTermJHS3ReligiousMoralEducation.query.filter_by(id=student_id).first()
    form = StudentAssessmentForm()
    if form.validate_on_submit():
        if form_3_student:
            class_test = form.classtest.data
            mid_terms = form.midterms.data
            project_work = form.project_work.data
            examination = form.examinations.data
            form_3_student.classtest = class_test
            form_3_student.midterm_examination = mid_terms
            form_3_student.project_work = project_work
            form_3_student.end_of_term_examination = examination
            form_3_student.subtotal = float(class_test) + float(mid_terms) + float(project_work)
            form_3_student.half_subtotal = (float(class_test) + float(mid_terms) + float(project_work)) / 2
            form_3_student.half_examination = float(examination) / 2
            form_3_student.grand_total = ((float(class_test) + float(mid_terms) + float(project_work)) / 2) + (
                    float(examination) / 2)
            db.session.add(form_3_student)
            db.session.commit()
            return redirect(url_for('rme'))
        else:
            flash('Student not found!')

    return render_template('student_assessment.html', form=form)


@app.route('/second-term-jhs-3-rme-student-assessment/<int:index>', methods=['GET', 'POST'])
@login_required
def edit_second_term_jhs3_rme_student(index):
    student_id = index
    form_3_student = SecondTermJHS3ReligiousMoralEducation.query.filter_by(id=student_id).first()
    form = StudentAssessmentForm()
    if form.validate_on_submit():
        if form_3_student:
            class_test = form.classtest.data
            mid_terms = form.midterms.data
            project_work = form.project_work.data
            examination = form.examinations.data
            form_3_student.classtest = class_test
            form_3_student.midterm_examination = mid_terms
            form_3_student.project_work = project_work
            form_3_student.end_of_term_examination = examination
            form_3_student.subtotal = float(class_test) + float(mid_terms) + float(project_work)
            form_3_student.half_subtotal = (float(class_test) + float(mid_terms) + float(project_work)) / 2
            form_3_student.half_examination = float(examination) / 2
            form_3_student.grand_total = ((float(class_test) + float(mid_terms) + float(project_work)) / 2) + (
                    float(examination) / 2)
            db.session.add(form_3_student)
            db.session.commit()
            return redirect(url_for('rme'))
        else:
            flash('Student not found!')

    return render_template('student_assessment.html', form=form)


@app.route('/third-term-jhs-3-rme-student-assessment/<int:index>', methods=['GET', 'POST'])
@login_required
def edit_third_term_jhs3_rme_student(index):
    student_id = index
    form_3_student = ThirdTermJHS3ReligiousMoralEducation.query.filter_by(id=student_id).first()
    form = StudentAssessmentForm()
    if form.validate_on_submit():
        if form_3_student:
            class_test = form.classtest.data
            mid_terms = form.midterms.data
            project_work = form.project_work.data
            examination = form.examinations.data
            form_3_student.classtest = class_test
            form_3_student.midterm_examination = mid_terms
            form_3_student.project_work = project_work
            form_3_student.end_of_term_examination = examination
            form_3_student.subtotal = float(class_test) + float(mid_terms) + float(project_work)
            form_3_student.half_subtotal = (float(class_test) + float(mid_terms) + float(project_work)) / 2
            form_3_student.half_examination = float(examination) / 2
            form_3_student.grand_total = ((float(class_test) + float(mid_terms) + float(project_work)) / 2) + (
                    float(examination) / 2)
            db.session.add(form_3_student)
            db.session.commit()
            return redirect(url_for('rme'))
        else:
            flash('Student not found!')

    return render_template('student_assessment.html', form=form)


@app.route('/cad-portal')
@login_required
def cad():
    form_1_first_term_students = FirstTermJHS1CreativeArtsAndDesign.query.all()
    form_1_second_term_students = SecondTermJHS1CreativeArtsAndDesign.query.all()
    form_1_third_term_students = ThirdTermJHS1CreativeArtsAndDesign.query.all()
    form_2_first_term_students = FirstTermJHS2CreativeArtsAndDesign.query.all()
    form_2_second_term_students = SecondTermJHS2CreativeArtsAndDesign.query.all()
    form_2_third_term_students = ThirdTermJHS2CreativeArtsAndDesign.query.all()
    form_3_first_term_students = FirstTermJHS3CreativeArtsAndDesign.query.all()
    form_3_second_term_students = SecondTermJHS3CreativeArtsAndDesign.query.all()
    form_3_third_term_students = ThirdTermJHS3CreativeArtsAndDesign.query.all()
    return render_template('english_dashboard.html', form_1_first_term_students=form_1_first_term_students,
                           form_1_second_term_students=form_1_second_term_students,
                           form_1_third_term_students=form_1_third_term_students,
                           form_2_first_term_students=form_2_first_term_students,
                           form_2_second_term_students=form_2_second_term_students,
                           form_2_third_term_students=form_2_third_term_students,
                           form_3_first_term_students=form_3_first_term_students,
                           form_3_second_term_students=form_3_second_term_students, current_user=current_user)


@app.route('/first-term-jhs-1-cad-student-assessment/<int:index>', methods=['GET', 'POST'])
@login_required
def edit_first_term_jhs1_cad_student(index):
    student_id = index
    form_1_student = FirstTermJHS1CreativeArtsAndDesign.query.filter_by(id=student_id).first()
    form = StudentAssessmentForm()
    if form.validate_on_submit():
        if form_1_student:
            class_test = form.classtest.data
            mid_terms = form.midterms.data
            project_work = form.project_work.data
            examination = form.examinations.data
            form_1_student.classtest = class_test
            form_1_student.midterm_examination = mid_terms
            form_1_student.project_work = project_work
            form_1_student.end_of_term_examination = examination
            form_1_student.subtotal = float(class_test) + float(mid_terms) + float(project_work)
            form_1_student.half_subtotal = (float(class_test) + float(mid_terms) + float(project_work)) / 2
            form_1_student.half_examination = float(examination) / 2
            form_1_student.grand_total = ((float(class_test) + float(mid_terms) + float(project_work)) / 2) + (
                    float(examination) / 2)
            db.session.add(form_1_student)
            db.session.commit()
            return redirect(url_for('cad'))
        else:
            flash('Student not found!')

    return render_template('student_assessment.html', form=form)


@app.route('/second-term-jhs-1-cad-student-assessment/<int:index>', methods=['GET', 'POST'])
@login_required
def edit_second_term_jhs1_cad_student(index):
    student_id = index
    form_1_student = SecondTermJHS1CreativeArtsAndDesign.query.filter_by(id=student_id).first()
    form = StudentAssessmentForm()
    if form.validate_on_submit():
        if form_1_student:
            class_test = form.classtest.data
            mid_terms = form.midterms.data
            project_work = form.project_work.data
            examination = form.examinations.data
            form_1_student.classtest = class_test
            form_1_student.midterm_examination = mid_terms
            form_1_student.project_work = project_work
            form_1_student.end_of_term_examination = examination
            form_1_student.subtotal = float(class_test) + float(mid_terms) + float(project_work)
            form_1_student.half_subtotal = (float(class_test) + float(mid_terms) + float(project_work)) / 2
            form_1_student.half_examination = float(examination) / 2
            form_1_student.grand_total = ((float(class_test) + float(mid_terms) + float(project_work)) / 2) + (
                    float(examination) / 2)
            db.session.add(form_1_student)
            db.session.commit()
            return redirect(url_for('cad'))
        else:
            flash('Student not found!')

    return render_template('student_assessment.html', form=form)


@app.route('/third-term-jhs-1-cad-student-assessment/<int:index>', methods=['GET', 'POST'])
@login_required
def edit_third_term_jhs1_cad_student(index):
    student_id = index
    form_1_student = ThirdTermJHS1CreativeArtsAndDesign.query.filter_by(id=student_id).first()
    form = StudentAssessmentForm()
    if form.validate_on_submit():
        if form_1_student:
            class_test = form.classtest.data
            mid_terms = form.midterms.data
            project_work = form.project_work.data
            examination = form.examinations.data
            form_1_student.classtest = class_test
            form_1_student.midterm_examination = mid_terms
            form_1_student.project_work = project_work
            form_1_student.end_of_term_examination = examination
            form_1_student.subtotal = float(class_test) + float(mid_terms) + float(project_work)
            form_1_student.half_subtotal = (float(class_test) + float(mid_terms) + float(project_work)) / 2
            form_1_student.half_examination = float(examination) / 2
            form_1_student.grand_total = ((float(class_test) + float(mid_terms) + float(project_work)) / 2) + (
                    float(examination) / 2)
            db.session.add(form_1_student)
            db.session.commit()
            return redirect(url_for('cad'))
        else:
            flash('Student not found!')

    return render_template('student_assessment.html', form=form)


@app.route('/first-term-jhs-2-cad-student-assessment/<int:index>', methods=['GET', 'POST'])
@login_required
def edit_first_term_jhs2_cad_student(index):
    student_id = index
    form_2_student = FirstTermJHS2CreativeArtsAndDesign.query.filter_by(id=student_id).first()
    form = StudentAssessmentForm()
    if form.validate_on_submit():
        if form_2_student:
            class_test = form.classtest.data
            mid_terms = form.midterms.data
            project_work = form.project_work.data
            examination = form.examinations.data
            form_2_student.classtest = class_test
            form_2_student.midterm_examination = mid_terms
            form_2_student.project_work = project_work
            form_2_student.end_of_term_examination = examination
            form_2_student.subtotal = float(class_test) + float(mid_terms) + float(project_work)
            form_2_student.half_subtotal = (float(class_test) + float(mid_terms) + float(project_work)) / 2
            form_2_student.half_examination = float(examination) / 2
            form_2_student.grand_total = ((float(class_test) + float(mid_terms) + float(project_work)) / 2) + (
                    float(examination) / 2)
            db.session.add(form_2_student)
            db.session.commit()
            return redirect(url_for('cad'))
        else:
            flash('Student not found!')

    return render_template('student_assessment.html', form=form)


@app.route('/second-term-jhs-2-cad-student-assessment/<int:index>', methods=['GET', 'POST'])
@login_required
def edit_second_term_jhs2_cad_student(index):
    student_id = index
    form_2_student = SecondTermJHS2CreativeArtsAndDesign.query.filter_by(id=student_id).first()
    form = StudentAssessmentForm()
    if form.validate_on_submit():
        if form_2_student:
            class_test = form.classtest.data
            mid_terms = form.midterms.data
            project_work = form.project_work.data
            examination = form.examinations.data
            form_2_student.classtest = class_test
            form_2_student.midterm_examination = mid_terms
            form_2_student.project_work = project_work
            form_2_student.end_of_term_examination = examination
            form_2_student.subtotal = float(class_test) + float(mid_terms) + float(project_work)
            form_2_student.half_subtotal = (float(class_test) + float(mid_terms) + float(project_work)) / 2
            form_2_student.half_examination = float(examination) / 2
            form_2_student.grand_total = ((float(class_test) + float(mid_terms) + float(project_work)) / 2) + (
                    float(examination) / 2)
            db.session.add(form_2_student)
            db.session.commit()
            return redirect(url_for('cad'))
        else:
            flash('Student not found!')

    return render_template('student_assessment.html', form=form)


@app.route('/third-term-jhs-2-cad-student-assessment/<int:index>', methods=['GET', 'POST'])
@login_required
def edit_third_term_jhs2_cad_student(index):
    student_id = index
    form_2_student = ThirdTermJHS2CreativeArtsAndDesign.query.filter_by(id=student_id).first()
    form = StudentAssessmentForm()
    if form.validate_on_submit():
        if form_2_student:
            class_test = form.classtest.data
            mid_terms = form.midterms.data
            project_work = form.project_work.data
            examination = form.examinations.data
            form_2_student.classtest = class_test
            form_2_student.midterm_examination = mid_terms
            form_2_student.project_work = project_work
            form_2_student.end_of_term_examination = examination
            form_2_student.subtotal = float(class_test) + float(mid_terms) + float(project_work)
            form_2_student.half_subtotal = (float(class_test) + float(mid_terms) + float(project_work)) / 2
            form_2_student.half_examination = float(examination) / 2
            form_2_student.grand_total = ((float(class_test) + float(mid_terms) + float(project_work)) / 2) + (
                    float(examination) / 2)
            db.session.add(form_2_student)
            db.session.commit()
            return redirect(url_for('cad'))
        else:
            flash('Student not found!')

    return render_template('student_assessment.html', form=form)


@app.route('/first-term-jhs-3-cad-student-assessment/<int:index>', methods=['GET', 'POST'])
@login_required
def edit_first_term_jhs3_cad_student(index):
    student_id = index
    form_3_student = FirstTermJHS3CreativeArtsAndDesign.query.filter_by(id=student_id).first()
    form = StudentAssessmentForm()
    if form.validate_on_submit():
        if form_3_student:
            class_test = form.classtest.data
            mid_terms = form.midterms.data
            project_work = form.project_work.data
            examination = form.examinations.data
            form_3_student.classtest = class_test
            form_3_student.midterm_examination = mid_terms
            form_3_student.project_work = project_work
            form_3_student.end_of_term_examination = examination
            form_3_student.subtotal = float(class_test) + float(mid_terms) + float(project_work)
            form_3_student.half_subtotal = (float(class_test) + float(mid_terms) + float(project_work)) / 2
            form_3_student.half_examination = float(examination) / 2
            form_3_student.grand_total = ((float(class_test) + float(mid_terms) + float(project_work)) / 2) + (
                    float(examination) / 2)
            db.session.add(form_3_student)
            db.session.commit()
            return redirect(url_for('cad'))
        else:
            flash('Student not found!')

    return render_template('student_assessment.html', form=form)


@app.route('/second-term-jhs-3-cad-student-assessment/<int:index>', methods=['GET', 'POST'])
@login_required
def edit_second_term_jhs3_cad_student(index):
    student_id = index
    form_3_student = SecondTermJHS3CreativeArtsAndDesign.query.filter_by(id=student_id).first()
    form = StudentAssessmentForm()
    if form.validate_on_submit():
        if form_3_student:
            class_test = form.classtest.data
            mid_terms = form.midterms.data
            project_work = form.project_work.data
            examination = form.examinations.data
            form_3_student.classtest = class_test
            form_3_student.midterm_examination = mid_terms
            form_3_student.project_work = project_work
            form_3_student.end_of_term_examination = examination
            form_3_student.subtotal = float(class_test) + float(mid_terms) + float(project_work)
            form_3_student.half_subtotal = (float(class_test) + float(mid_terms) + float(project_work)) / 2
            form_3_student.half_examination = float(examination) / 2
            form_3_student.grand_total = ((float(class_test) + float(mid_terms) + float(project_work)) / 2) + (
                    float(examination) / 2)
            db.session.add(form_3_student)
            db.session.commit()
            return redirect(url_for('cad'))
        else:
            flash('Student not found!')

    return render_template('student_assessment.html', form=form)


@app.route('/third-term-jhs-3-cad-student-assessment/<int:index>', methods=['GET', 'POST'])
@login_required
def edit_third_term_jhs3_cad_student(index):
    student_id = index
    form_3_student = ThirdTermJHS3CreativeArtsAndDesign.query.filter_by(id=student_id).first()
    form = StudentAssessmentForm()
    if form.validate_on_submit():
        if form_3_student:
            class_test = form.classtest.data
            mid_terms = form.midterms.data
            project_work = form.project_work.data
            examination = form.examinations.data
            form_3_student.classtest = class_test
            form_3_student.midterm_examination = mid_terms
            form_3_student.project_work = project_work
            form_3_student.end_of_term_examination = examination
            form_3_student.subtotal = float(class_test) + float(mid_terms) + float(project_work)
            form_3_student.half_subtotal = (float(class_test) + float(mid_terms) + float(project_work)) / 2
            form_3_student.half_examination = float(examination) / 2
            form_3_student.grand_total = ((float(class_test) + float(mid_terms) + float(project_work)) / 2) + (
                    float(examination) / 2)
            db.session.add(form_3_student)
            db.session.commit()
            return redirect(url_for('cad'))
        else:
            flash('Student not found!')

    return render_template('student_assessment.html', form=form)


@app.route('/career-technology-portal')
@login_required
def career_tech():
    form_1_first_term_students = FirstTermJHS1CareerTechnology.query.all()
    form_1_second_term_students = SecondTermJHS1CareerTechnology.query.all()
    form_1_third_term_students = ThirdTermJHS1CareerTechnology.query.all()
    form_2_first_term_students = FirstTermJHS2CareerTechnology.query.all()
    form_2_second_term_students = SecondTermJHS2CareerTechnology.query.all()
    form_2_third_term_students = ThirdTermJHS2CareerTechnology.query.all()
    form_3_first_term_students = FirstTermJHS3CareerTechnology.query.all()
    form_3_second_term_students = SecondTermJHS3CareerTechnology.query.all()
    form_3_third_term_students = ThirdTermJHS3CareerTechnology.query.all()
    return render_template('english_dashboard.html', form_1_first_term_students=form_1_first_term_students,
                           form_1_second_term_students=form_1_second_term_students,
                           form_1_third_term_students=form_1_third_term_students,
                           form_2_first_term_students=form_2_first_term_students,
                           form_2_second_term_students=form_2_second_term_students,
                           form_2_third_term_students=form_2_third_term_students,
                           form_3_first_term_students=form_3_first_term_students,
                           form_3_second_term_students=form_3_second_term_students, current_user=current_user)


@app.route('/first-term-jhs-1-career-tech-student-assessment/<int:index>', methods=['GET', 'POST'])
@login_required
def edit_first_term_jhs1_career_tech_student(index):
    student_id = index
    form_1_student = FirstTermJHS1CareerTechnology.query.filter_by(id=student_id).first()
    form = StudentAssessmentForm()
    if form.validate_on_submit():
        if form_1_student:
            class_test = form.classtest.data
            mid_terms = form.midterms.data
            project_work = form.project_work.data
            examination = form.examinations.data
            form_1_student.classtest = class_test
            form_1_student.midterm_examination = mid_terms
            form_1_student.project_work = project_work
            form_1_student.end_of_term_examination = examination
            form_1_student.subtotal = float(class_test) + float(mid_terms) + float(project_work)
            form_1_student.half_subtotal = (float(class_test) + float(mid_terms) + float(project_work)) / 2
            form_1_student.half_examination = float(examination) / 2
            form_1_student.grand_total = ((float(class_test) + float(mid_terms) + float(project_work)) / 2) + (
                    float(examination) / 2)
            db.session.add(form_1_student)
            db.session.commit()
            return redirect(url_for('career_tech'))
        else:
            flash('Student not found!')

    return render_template('student_assessment.html', form=form)


@app.route('/second-term-jhs-1-career-tech-student-assessment/<int:index>', methods=['GET', 'POST'])
@login_required
def edit_second_term_jhs1_career_tech_student(index):
    student_id = index
    form_1_student = SecondTermJHS1CareerTechnology.query.filter_by(id=student_id).first()
    form = StudentAssessmentForm()
    if form.validate_on_submit():
        if form_1_student:
            class_test = form.classtest.data
            mid_terms = form.midterms.data
            project_work = form.project_work.data
            examination = form.examinations.data
            form_1_student.classtest = class_test
            form_1_student.midterm_examination = mid_terms
            form_1_student.project_work = project_work
            form_1_student.end_of_term_examination = examination
            form_1_student.subtotal = float(class_test) + float(mid_terms) + float(project_work)
            form_1_student.half_subtotal = (float(class_test) + float(mid_terms) + float(project_work)) / 2
            form_1_student.half_examination = float(examination) / 2
            form_1_student.grand_total = ((float(class_test) + float(mid_terms) + float(project_work)) / 2) + (
                    float(examination) / 2)
            db.session.add(form_1_student)
            db.session.commit()
            return redirect(url_for('career_tech'))
        else:
            flash('Student not found!')

    return render_template('student_assessment.html', form=form)


@app.route('/third-term-jhs-1-career-tech-student-assessment/<int:index>', methods=['GET', 'POST'])
@login_required
def edit_third_term_jhs1_career_tech_student(index):
    student_id = index
    form_1_student = ThirdTermJHS1CareerTechnology.query.filter_by(id=student_id).first()
    form = StudentAssessmentForm()
    if form.validate_on_submit():
        if form_1_student:
            class_test = form.classtest.data
            mid_terms = form.midterms.data
            project_work = form.project_work.data
            examination = form.examinations.data
            form_1_student.classtest = class_test
            form_1_student.midterm_examination = mid_terms
            form_1_student.project_work = project_work
            form_1_student.end_of_term_examination = examination
            form_1_student.subtotal = float(class_test) + float(mid_terms) + float(project_work)
            form_1_student.half_subtotal = (float(class_test) + float(mid_terms) + float(project_work)) / 2
            form_1_student.half_examination = float(examination) / 2
            form_1_student.grand_total = ((float(class_test) + float(mid_terms) + float(project_work)) / 2) + (
                    float(examination) / 2)
            db.session.add(form_1_student)
            db.session.commit()
            return redirect(url_for('career_tech'))
        else:
            flash('Student not found!')

    return render_template('student_assessment.html', form=form)


@app.route('/first-term-jhs-2-career-tech-student-assessment/<int:index>', methods=['GET', 'POST'])
@login_required
def edit_first_term_jhs2_career_tech_student(index):
    student_id = index
    form_2_student = FirstTermJHS2CareerTechnology.query.filter_by(id=student_id).first()
    form = StudentAssessmentForm()
    if form.validate_on_submit():
        if form_2_student:
            class_test = form.classtest.data
            mid_terms = form.midterms.data
            project_work = form.project_work.data
            examination = form.examinations.data
            form_2_student.classtest = class_test
            form_2_student.midterm_examination = mid_terms
            form_2_student.project_work = project_work
            form_2_student.end_of_term_examination = examination
            form_2_student.subtotal = float(class_test) + float(mid_terms) + float(project_work)
            form_2_student.half_subtotal = (float(class_test) + float(mid_terms) + float(project_work)) / 2
            form_2_student.half_examination = float(examination) / 2
            form_2_student.grand_total = ((float(class_test) + float(mid_terms) + float(project_work)) / 2) + (
                    float(examination) / 2)
            db.session.add(form_2_student)
            db.session.commit()
            return redirect(url_for('career_tech'))
        else:
            flash('Student not found!')

    return render_template('student_assessment.html', form=form)


@app.route('/second-term-jhs-2-career-tech-student-assessment/<int:index>', methods=['GET', 'POST'])
@login_required
def edit_second_term_jhs2_career_tech_student(index):
    student_id = index
    form_2_student = SecondTermJHS2CareerTechnology.query.filter_by(id=student_id).first()
    form = StudentAssessmentForm()
    if form.validate_on_submit():
        if form_2_student:
            class_test = form.classtest.data
            mid_terms = form.midterms.data
            project_work = form.project_work.data
            examination = form.examinations.data
            form_2_student.classtest = class_test
            form_2_student.midterm_examination = mid_terms
            form_2_student.project_work = project_work
            form_2_student.end_of_term_examination = examination
            form_2_student.subtotal = float(class_test) + float(mid_terms) + float(project_work)
            form_2_student.half_subtotal = (float(class_test) + float(mid_terms) + float(project_work)) / 2
            form_2_student.half_examination = float(examination) / 2
            form_2_student.grand_total = ((float(class_test) + float(mid_terms) + float(project_work)) / 2) + (
                    float(examination) / 2)
            db.session.add(form_2_student)
            db.session.commit()
            return redirect(url_for('career_tech'))
        else:
            flash('Student not found!')

    return render_template('student_assessment.html', form=form)


@app.route('/third-term-jhs-2-career-tech-student-assessment/<int:index>', methods=['GET', 'POST'])
@login_required
def edit_first_term_jhs2_career_tech_student(index):
    student_id = index
    form_2_student = ThirdTermJHS2CareerTechnology.query.filter_by(id=student_id).first()
    form = StudentAssessmentForm()
    if form.validate_on_submit():
        if form_2_student:
            class_test = form.classtest.data
            mid_terms = form.midterms.data
            project_work = form.project_work.data
            examination = form.examinations.data
            form_2_student.classtest = class_test
            form_2_student.midterm_examination = mid_terms
            form_2_student.project_work = project_work
            form_2_student.end_of_term_examination = examination
            form_2_student.subtotal = float(class_test) + float(mid_terms) + float(project_work)
            form_2_student.half_subtotal = (float(class_test) + float(mid_terms) + float(project_work)) / 2
            form_2_student.half_examination = float(examination) / 2
            form_2_student.grand_total = ((float(class_test) + float(mid_terms) + float(project_work)) / 2) + (
                    float(examination) / 2)
            db.session.add(form_2_student)
            db.session.commit()
            return redirect(url_for('career_tech'))
        else:
            flash('Student not found!')

    return render_template('student_assessment.html', form=form)


@app.route('/first-term-jhs-3-career-tech-student-assessment/<int:index>', methods=['GET', 'POST'])
@login_required
def edit_first_term_jhs3_career_tech_student(index):
    student_id = index
    form_3_student = FirstTermJHS3CareerTechnology.query.filter_by(id=student_id).first()
    form = StudentAssessmentForm()
    if form.validate_on_submit():
        if form_3_student:
            class_test = form.classtest.data
            mid_terms = form.midterms.data
            project_work = form.project_work.data
            examination = form.examinations.data
            form_3_student.classtest = class_test
            form_3_student.midterm_examination = mid_terms
            form_3_student.project_work = project_work
            form_3_student.end_of_term_examination = examination
            form_3_student.subtotal = float(class_test) + float(mid_terms) + float(project_work)
            form_3_student.half_subtotal = (float(class_test) + float(mid_terms) + float(project_work)) / 2
            form_3_student.half_examination = float(examination) / 2
            form_3_student.grand_total = ((float(class_test) + float(mid_terms) + float(project_work)) / 2) + (
                    float(examination) / 2)
            db.session.add(form_3_student)
            db.session.commit()
            return redirect(url_for('career_tech'))
        else:
            flash('Student not found!')

    return render_template('student_assessment.html', form=form)


@app.route('/second-term-jhs-3-career-tech-student-assessment/<int:index>', methods=['GET', 'POST'])
@login_required
def edit_second_term_jhs3_career_tech_student(index):
    student_id = index
    form_3_student = SecondTermJHS3CareerTechnology.query.filter_by(id=student_id).first()
    form = StudentAssessmentForm()
    if form.validate_on_submit():
        if form_3_student:
            class_test = form.classtest.data
            mid_terms = form.midterms.data
            project_work = form.project_work.data
            examination = form.examinations.data
            form_3_student.classtest = class_test
            form_3_student.midterm_examination = mid_terms
            form_3_student.project_work = project_work
            form_3_student.end_of_term_examination = examination
            form_3_student.subtotal = float(class_test) + float(mid_terms) + float(project_work)
            form_3_student.half_subtotal = (float(class_test) + float(mid_terms) + float(project_work)) / 2
            form_3_student.half_examination = float(examination) / 2
            form_3_student.grand_total = ((float(class_test) + float(mid_terms) + float(project_work)) / 2) + (
                    float(examination) / 2)
            db.session.add(form_3_student)
            db.session.commit()
            return redirect(url_for('career_tech'))
        else:
            flash('Student not found!')

    return render_template('student_assessment.html', form=form)


@app.route('/third-term-jhs-3-career-tech-student-assessment/<int:index>', methods=['GET', 'POST'])
@login_required
def edit_third_term_jhs3_career_tech_student(index):
    student_id = index
    form_3_student = ThirdTermJHS3CareerTechnology.query.filter_by(id=student_id).first()
    form = StudentAssessmentForm()
    if form.validate_on_submit():
        if form_3_student:
            class_test = form.classtest.data
            mid_terms = form.midterms.data
            project_work = form.project_work.data
            examination = form.examinations.data
            form_3_student.classtest = class_test
            form_3_student.midterm_examination = mid_terms
            form_3_student.project_work = project_work
            form_3_student.end_of_term_examination = examination
            form_3_student.subtotal = float(class_test) + float(mid_terms) + float(project_work)
            form_3_student.half_subtotal = (float(class_test) + float(mid_terms) + float(project_work)) / 2
            form_3_student.half_examination = float(examination) / 2
            form_3_student.grand_total = ((float(class_test) + float(mid_terms) + float(project_work)) / 2) + (
                    float(examination) / 2)
            db.session.add(form_3_student)
            db.session.commit()
            return redirect(url_for('career_tech'))
        else:
            flash('Student not found!')

    return render_template('student_assessment.html', form=form)


@app.route('/fante_language')
@login_required
def fante():
    pass


# route to subject portal which contains links to all the subjects and their respective dashboards html pages
@app.route('/subject-portal')
@login_required
def subject_portal():
    return render_template('subjects.html', name=current_user.name)


# route to admin dashboard
@app.route('/admin', methods=['GET', 'POST'])
@admin_only
def administrator():
    all_teachers = Teacher.query.all()
    all_students = JHSStudent.query.all()
    return render_template('admin_dashboard.html', teachers=all_teachers, students=all_students)


# route for admin only to delete a teacher from the database
@app.route('/delete_teacher/<int:index>')
@admin_only
def delete_teacher(index):
    teacher_id = index
    teacher = Teacher.query.get(teacher_id)
    db.session.delete(teacher)
    db.session.commit()
    return redirect(url_for('administrator'))


# route for admin only to delete student from student database
@app.route('/delete_student/<int:index>')
@admin_only
def delete_student(index):
    student_id = index
    remove_student = JHSStudent.query.get(student_id)
    check_jss1 = JHS1Student.query.get(student_id)
    if check_jss1:
        db.session.delete(check_jss1)
    check_jss2 = JHS2Student.query.get(student_id)
    if check_jss2:
        db.session.delete(check_jss2)
    check_jss3 = JHS3Student.query.get(student_id)
    if check_jss3:
        db.session.delete(check_jss3)
    db.session.delete(remove_student)
    db.session.commit()
    return redirect(url_for('administrator'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
