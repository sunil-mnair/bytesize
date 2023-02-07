
from datetime import *
from pytz import timezone
uae = timezone('Asia/Dubai')

from flask_login import UserMixin,current_user,login_user,logout_user
from flask_admin import Admin,AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask import url_for,redirect,request

from flask_admin import BaseView, expose

from wtforms import TextAreaField
from wtforms.widgets import TextArea


from sqlalchemy import inspect
from sqlalchemy.orm import backref

from .app import db

# Enable Rich Text Editor
class CKTextAreaWidget(TextArea):
    def __call__(self, field, **kwargs):
        if kwargs.get('class'):
            kwargs['class'] += ' ckeditor'
        else:
            kwargs.setdefault('class', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)

# Enable Rich Text Editor
class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    def __repr__(self):
        return self.username

class Author(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    author = db.Column(db.String,nullable = False)

    def __repr__(self):
        return self.author
    
class Blog(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    blogTitle = db.Column(db.String,nullable = False)
    blogDescription = db.Column(db.Text(),nullable = False)
    blogImage = db.Column(db.String,nullable = True)

    author_id = db.Column(db.Integer,db.ForeignKey('author.id'))

    author = db.relationship('Author', backref=db.backref('blog', lazy='dynamic'))
    
    created_dt = db.Column(db.DateTime, nullable = True,
    default = datetime.now(uae))
    modified_dt = db.Column(db.DateTime, nullable = True,
    default = datetime.now(uae))

    def __repr__(self):
        return self.blogTitle

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    studentName = db.Column(db.String(100), unique=True)

    email = db.Column(db.String(100), unique=True)
    
    company = db.Column(db.String(100))
    profession = db.Column(db.String(100))

    created_dt = db.Column(db.DateTime, nullable = False,
    default = datetime.now(uae))

class Course(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    courseName = db.Column(db.String,nullable = True)
    courseDescription = db.Column(db.Text(),nullable = True)
    courseImage = db.Column(db.String,nullable = False)

    assignment = db.Column(db.Boolean)
    assignment_frequency = db.Column(db.Integer)

    created_dt = db.Column(db.DateTime, nullable = True,
    default = datetime.now(uae))
    modified_dt = db.Column(db.DateTime, nullable = True,
    default = datetime.now(uae))

    def __repr__(self):
        return self.courseName

class UserCourse(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    userId = db.Column(db.Integer,db.ForeignKey('user.id'))
    courseId = db.Column(db.Integer,db.ForeignKey('course.id'))

    course = db.relationship('Course', backref=db.backref('user', lazy='dynamic'))
    user = db.relationship('User', backref=db.backref('course', lazy='dynamic'))
    
    created_dt = db.Column(db.DateTime, nullable = False,
    default = datetime.now(uae))
    modified_dt = db.Column(db.DateTime, nullable = False,
    default = datetime.now(uae))


class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    courseId = db.Column(db.Integer,db.ForeignKey('course.id'))

    lessonName = db.Column(db.String,nullable = True)
    lessonDescription = db.Column(db.Text(),nullable = True)

    game = db.Column(db.String,nullable = True)

    sampleCode1 = db.Column(db.String,nullable = True)
    sampleCode2 = db.Column(db.String,nullable = True)
    sampleCode3 = db.Column(db.String,nullable = True)
    sampleCode4 = db.Column(db.String,nullable = True)
    resources = db.Column(db.String,nullable = True)

    lessonOrder = db.Column(db.Integer, nullable = False)

    course = db.relationship('Course', backref=db.backref('lesson', lazy='dynamic'))

    created_dt = db.Column(db.DateTime, nullable = True,
    default = datetime.now(uae))
    modified_dt = db.Column(db.DateTime, nullable = True,
    default = datetime.now(uae))

    def __repr__(self):
        return self.lessonName


class QuizMaster(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    question = db.Column(db.String,nullable = False)

    created_dt = db.Column(db.DateTime, nullable = True,
    default = datetime.now(uae))
    modified_dt = db.Column(db.DateTime, nullable = True,
    default = datetime.now(uae))

class QuizResults(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    question_id = db.Column(db.Integer)

    student_id  = db.Column(db.Integer,nullable = False)
    course_id  = db.Column(db.Integer,nullable = False)
    
    response = db.Column(db.Integer,nullable = False)

    created_dt = db.Column(db.DateTime, nullable = False,
    default = datetime.now(uae))
    modified_dt = db.Column(db.DateTime, nullable = False,
    default = datetime.now(uae))

class Activity(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    activityName  = db.Column(db.String,nullable = False)
    activityImage = db.Column(db.String,nullable = False)
    activityURL = db.Column(db.String,nullable = False)


class FeedbackRating(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    student_id = db.Column(db.Integer)
    rating = db.Column(db.Integer)
    objective = db.Column(db.Integer)
    comments = db.Column(db.String(500))

    created_dt = db.Column(db.DateTime, nullable = False,
    default = datetime.now(uae))
    modified_dt = db.Column(db.DateTime, nullable = False,
    default = datetime.now(uae))

class FeedbackFeature(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    feature = db.Column(db.String(100))

class FeedbackFeatureOutcome(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    student_id = db.Column(db.Integer)
    feature_id = db.Column(db.Integer)
    outcome = db.Column(db.Integer)

    created_dt = db.Column(db.DateTime, nullable = False,
    default = datetime.now(uae))
    modified_dt = db.Column(db.DateTime, nullable = False,
    default = datetime.now(uae))

class CourseAssignment(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    courseId = db.Column(db.Integer,db.ForeignKey('course.id'))
    
    assignmentTitle = db.Column(db.String,nullable = False)
    assignmentDescription = db.Column(db.Text(),nullable = True)
    assignmentOrder = db.Column(db.Integer,nullable = False)

    file_url = db.Column(db.String,nullable = False)
    file_url_solution = db.Column(db.String,nullable = True)

    course = db.relationship('Course', backref=db.backref('course_assignment', lazy='dynamic'))

    def __repr__(self):
        return self.assignmentTitle

class CourseAssignmentSubscription(db.Model):
    id = db.Column(db.Integer, primary_key = True)

    courseId = db.Column(db.Integer,db.ForeignKey('course.id'))
    studentId = db.Column(db.Integer,db.ForeignKey('student.id'))

    assignmentOrderNo = db.Column(db.Integer)

    course = db.relationship('Course', backref=db.backref('course_assignment_subscription', lazy='dynamic'))
    student = db.relationship('Student', backref=db.backref('course_assignment_subscription', lazy='dynamic'))

    subscription = db.Column(db.Boolean)

    created_dt = db.Column(db.DateTime, nullable = True,
    default = datetime.now(uae))
    modified_dt = db.Column(db.DateTime, nullable = True,
    default = datetime.now(uae))

    def __repr__(self):
        return str(self.id)

class CourseAssignmentSent(db.Model):
    id = db.Column(db.Integer, primary_key = True)

    courseId = db.Column(db.Integer,db.ForeignKey('course.id'))
    studentId = db.Column(db.Integer,db.ForeignKey('student.id'))

    assignmentOrderNo = db.Column(db.Integer)

    course = db.relationship('Course', backref=db.backref('course_assignment_sent', lazy='dynamic'))
    student = db.relationship('Student', backref=db.backref('course_assignment_sent', lazy='dynamic'))

    sent_dt = db.Column(db.DateTime, nullable = True,
    default = datetime.now(uae))

    def __repr__(self):
        return str(self.id)



class Poll(db.Model):
    id = db.Column(db.Integer, primary_key = True)

    name  = db.Column(db.String,nullable = False)
    theme = db.Column(db.String,nullable = False)
    question = db.Column(db.String,nullable = False)
    response = db.Column(db.Integer,nullable = False)

    created_dt = db.Column(db.DateTime, nullable = False,
    default = datetime.now(uae))
    modified_dt = db.Column(db.DateTime, nullable = False,
    default = datetime.now(uae))

class GameParticipation(db.Model):
    id = db.Column(db.Integer, primary_key = True)

    name  = db.Column(db.String,nullable = False)
    created_dt = db.Column(db.DateTime, nullable = False,
    default = datetime.now(uae))


class AllModelView(ModelView):

    can_delete = True
    page_size = 50
    column_display_pk = True # optional, but I like to see the IDs in the list
    column_hide_backrefs = False
    can_export = True

    form_excluded_columns = ['created_dt', 'modified_dt']

    def is_accessible(self):
        if current_user.username == 'sunil.nair':
            return current_user.is_authenticated
        else:
            return current_user.is_anonymous

    def inaccessible_callback(self,name,**kwargs):
        return redirect(url_for('login'))


class LessonView(ModelView):

    can_delete = True
    page_size = 50
    column_searchable_list = ['courseId','lessonName','lessonDescription']
    column_filters = ['courseId','lessonName']
    column_hide_backrefs = False

    form_excluded_columns = ['created_dt', 'modified_dt']

    # With Model View, it does not show Rich Text Editor
    # create_modal = True
    # edit_modal = True

    form_args = {
    'lessonName': {
        'label': 'Lesson'
    },
    'lessonDescription': {
        'label': 'Description'
    }
    }

    form_widget_args = {
    'lessonDescription': {
        'rows': 30
    }
    }

    extra_js = ['https://cdn.ckeditor.com/4.6.0/standard/ckeditor.js']

    form_overrides = {
        'lessonDescription': CKTextAreaField
    }

    def is_accessible(self):
        if current_user.username == 'sunil.nair':
            return current_user.is_authenticated
        else:
            return current_user.is_anonymous

    def inaccessible_callback(self,name,**kwargs):
        return redirect(url_for('login'))

class BlogView(ModelView):

    can_delete = True
    page_size = 50
    column_searchable_list = ['blogTitle','blogDescription']
    column_filters = ['blogTitle']
    column_hide_backrefs = False

    form_excluded_columns = ['created_dt', 'modified_dt']

    # With Model View, it does not show Rich Text Editor
    # create_modal = True
    # edit_modal = True

    form_args = {
    'blogTitle': {
        'label': 'Title'
    },
    'blogDescription': {
        'label': 'Description'
    }
    }

    form_widget_args = {
    'blogDescription': {
        'rows': 50
    }
    }

    extra_js = ['https://cdn.ckeditor.com/4.6.0/standard/ckeditor.js']

    form_overrides = {
        'blogDescription': CKTextAreaField
    }

    def is_accessible(self):
        if current_user.username == 'sunil.nair':
            return current_user.is_authenticated
        else:
            return current_user.is_anonymous

    def inaccessible_callback(self,name,**kwargs):
        return redirect(url_for('login'))

class AssignmentView(ModelView):

    can_delete = True
    page_size = 50
    column_searchable_list = ['courseId']
    column_filters = ['courseId']
    column_hide_backrefs = False

    form_excluded_columns = ['created_dt', 'modified_dt']

    # With Model View, it does not show Rich Text Editor
    # create_modal = True
    # edit_modal = True

    
    form_widget_args = {
    'assignmentDescription': {
        'rows': 30
    }
    }

    extra_js = ['https://cdn.ckeditor.com/4.6.0/standard/ckeditor.js']

    form_overrides = {
        'assignmentDescription': CKTextAreaField
    }

    def is_accessible(self):
        if current_user.username == 'sunil.nair':
            return current_user.is_authenticated
        else:
            return current_user.is_anonymous

    def inaccessible_callback(self,name,**kwargs):
        return redirect(url_for('login'))



class MainAdminIndexView(AdminIndexView):
    def is_accessible(self):
        if current_user.username == 'sunil.nair':
            return current_user.is_authenticated
        else:
            return current_user.is_anonymous

    def inaccessible_callback(self,name,**kwargs):
        return redirect(url_for('login'))

class LessonOrderView(BaseView):
    @expose('/')
    def index_(self):
        lesson_order_url = url_for('lesson_order')
        return self.render('lesson_order.html', lesson_order_url = lesson_order_url)