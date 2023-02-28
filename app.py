import os,json,markdown, pandas as pd,re
import os.path as op
from datetime import *

from flask import Flask,render_template,request, redirect,url_for,Response,jsonify,flash,send_file,session
from flask_sqlalchemy import SQLAlchemy

from flask_login import LoginManager,login_required, login_user,logout_user,current_user
from flask_admin import Admin
# Enable File Upload in Admin
from flask_admin.contrib.fileadmin import FileAdmin
from flask_mail import Mail,Message

from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

from forms import *
# from bs4 import BeautifulSoup

getcwd = os.getcwd()

if 'home' in getcwd:
    getcwd += '/mysite'

with open(getcwd+'/'+'trainings.json') as file:
    trainings = json.load(file)

with open(getcwd+'/'+'testimonials.json') as file:
    testimonials = json.load(file)

with open(getcwd+'/'+'schedules.json') as file:
    schedules = json.load(file)
    schedules = [schedule for schedule in schedules if schedule['Status']=='Confirmed']

with open(getcwd+'/'+'res.json') as file:
    res = json.load(file)

def get_clients():
    clients = []
    for dir in os.scandir(getcwd+'/static/images/logos'):
        if ".png" in dir.name:
            clients.append(dir.name)
   
    return clients

def get_counters():

    return {
        "Focus Areas":len([t for t in trainings.keys()]),
        "Courses":sum(([len(t) for t in trainings.values()])),
        "Sessions":142,
        "Students":2203
    }



app = Flask(__name__,static_url_path='/static')


project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "bytesize.db"))

app.config['SECRET_KEY'] = 'bytesize_2023_02'
app.config['SQLALCHEMY_DATABASE_URI'] = database_file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# set optional bootswatch theme - bootswatch.com/3/
app.config['FLASK_ADMIN_SWATCH'] = 'sandstone'

db = SQLAlchemy(app)

from models import *

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
# since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))

admin = Admin(app,index_view=MainAdminIndexView(),template_mode='bootstrap3')
admin.add_view(AllModelView(User,db.session))
admin.add_view(AllModelView(Author,db.session,category="Blog"))
admin.add_view(BlogView(Blog,db.session,category="Blog"))
admin.add_view(AllModelView(Course,db.session,category="Course"))
admin.add_view(LessonView(Lesson,db.session,category="Course"))
admin.add_view(AllModelView(UserCourse,db.session,category="Course"))

@app.template_filter()
def tens(x):
    return (x//10)*10


@app.template_filter()
def summary(text):
    CLEANR = re.compile('<.*?>') 
    cleantext = re.sub(CLEANR, '', text)
    return cleantext[0:150]+'...'


@app.template_filter()
def thehtml(text):
    text = markdown.markdown(text)
    return text

@app.template_filter()
def duration(mod_dt):
    elapsed = datetime.now() - mod_dt
    
    if elapsed.days >= 1 and elapsed.days <=30:
        return  f'{elapsed.days} days ago'
    elif elapsed.days >=30:
        return  f'{elapsed.days//30} months ago'
    elif elapsed.days >=365:
        return  f'{elapsed.days//365} years ago'
    else:
        if elapsed.seconds//3600 <= 1:
            return f'{elapsed.seconds//60} minutes ago'
        elif elapsed.seconds//3600 <= 23:
            return f'{elapsed.seconds//3600} hours ago'
        
@app.template_filter()
def pluralize(number):
    if int(number) <= 1:
        return 'min.'
    else:
        return 'mins'

@app.template_filter()
def makeID(name):
    name = name.replace(" ","_")
    return name

@app.route('/login',methods=['GET','POST'])
def login():

    title = "Login"

    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(username=form.username.data).first()

        # check if the user actually exists
        # take the user-supplied password, hash it, and compare it to the hashed password in the database
        if not user or not check_password_hash(user.password, form.password.data):
            flash('Please check your login details and try again.')
            return redirect(url_for('login')) # if the user doesn't exist or password is wrong, reload the page

        # if the above check passes, then we know the user has the right credentials
        login_user(user,remember=form.remember.data)
        return redirect(url_for('index'))

    return render_template('login.html',title = title,form=form)


@app.route("/")
@app.route("/index")
def index():

    return render_template('index.html', 
    clients = get_clients(),
    counters = get_counters(),
    trainings = trainings,
    testimonials = testimonials,
    schedules = schedules)


@app.route("/blog")
def blog():

    blogs = db.session.query(Blog,Author)\
        .filter(Author.id == Blog.author_id).all()

   
    return render_template('blog.html',
    blogs = blogs)

@app.route("/blog_post/<int:id>")
def blog_post(id):

    blog = db.session.query(Blog,Author)\
        .filter(Blog.id == id,Author.id == Blog.author_id).first()

    # other 5 blogs
    blogs = db.session.query(Blog.id,Blog.blogTitle)\
        .filter(Blog.id != id).limit(5).all()

    return render_template('blog_post.html',
    blog = blog,blogs = blogs)


@app.route("/resources")
def resources():
    
    return render_template('/resources.html',res=res)

@app.route('/courses',methods=['GET','POST'])
def courses():

    courses = db.session.query(Course)\
        .filter(Course.courseName == 'Javascript Fundamentals').all()

    return render_template("courses.html",
    courses = courses,
    title="Courses on ByteSize")


@app.route('/course/<string:name>',methods=['GET','POST'])
def selected_course(name):

    name = name.replace("_"," ")
    course = db.session.query(Course)\
        .filter(Course.courseName == name).first()
   
    session["course"] = course.id

    html = markdown.markdown(course.courseDescription)

    lessons = db.session.query(Lesson)\
        .join(Course, Course.id == Lesson.courseId)\
        .filter(Course.courseName == name)\
        .order_by(Lesson.lessonOrder).all()
   
    return render_template("course.html",
    lessons = lessons, course = course,
    html = html,
    title = course.courseName)


@app.route('/lesson/<string:name>',methods=['GET','POST'])
def viewlesson(name):
    
    name = name.replace("_"," ")
    #lesson = Lesson.query.get_or_404(id)
    lesson = db.session.query(Lesson).filter(Lesson.lessonName == name).first()

    course = Course.query.get_or_404(lesson.courseId)
    # courseid = lesson.courseId

    lessons = db.session.query(Lesson)\
        .join(Course, Course.id == Lesson.courseId)\
        .filter(Course.id == course.id)\
        .order_by(Lesson.lessonOrder).all()
    
    # soup = BeautifulSoup(lesson.lessonDescription, 'html.parser')

    # Find all h2 headings for ToC
    # h2s = [h2.text.strip() for h2 in soup.find_all('h2')]    

    session["lessonNM"] = lesson.lessonName

    html = markdown.markdown(lesson.lessonDescription)

    return render_template("lesson.html",
    course = course, lesson = lesson,lessons = lessons,html = html,
    title = lesson.lessonName)


if __name__ == "__main__":
    app.run(debug=True)