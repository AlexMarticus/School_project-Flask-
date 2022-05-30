import datetime as dt
import json
from flask import Flask, render_template, redirect
from flask_login import current_user, LoginManager, login_user, login_required, logout_user
from data import db_session
from data.class_ import Class
from data.events import Events
from data.users import User
from forms.change_adm import MakeAdmin, MakeUnAdmin
from forms.change_lessons import ChangeLessons
from forms.event import AddEvents
from forms.user import RegisterForm, LoginForm, LoggedForm
import requests

app = Flask(__name__)
app.config["SECRET_KEY"] = "yandexlyceum_secret_key"
app.config['PERMANENT_SESSION_LIFETIME'] = dt.timedelta(
    days=365
)
login_manager = LoginManager()
login_manager.init_app(app)
user_progress = {}


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/10b")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', form=form)


@app.route('/make_admin', methods=['GET', 'POST'])
def make_ad():
    form = MakeAdmin()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        # user = User()
        user.is_admin = 1
        db_sess.commit()
        return redirect('/admin')
    return render_template('make_admins.html', form=form)


@app.route('/change_lessons', methods=['GET', 'POST'])
def ch_lessons():
    form = ChangeLessons()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        class_ = db_sess.query(Class).filter(Class.name == form.class_.data).first()
        if form.is_constant.data:
            class_.timetable = json.dumps({
                'Понедельник': [form.mon1.data, form.mon2.data, form.mon3.data, form.mon4.data, form.mon5.data,
                                form.mon6.data, form.mon7.data],
                'Вторник': [form.tue1.data, form.tue2.data, form.tue3.data, form.tue4.data, form.tue5.data,
                            form.tue6.data, form.tue7.data],
                'Среда': [form.wed1.data, form.wed2.data, form.wed3.data, form.wed4.data, form.wed5.data,
                          form.wed6.data, form.wed7.data],
                'Четверг': [form.thu1.data, form.thu2.data, form.thu3.data, form.thu4.data, form.thu5.data,
                            form.thu6.data, form.thu7.data],
                'Пятница': [form.fri1.data, form.fri2.data, form.fri3.data, form.fri4.data, form.fri5.data,
                            form.fri6.data, form.fri7.data],
                'Суббота': [form.sat1.data, form.sat2.data, form.sat3.data, form.sat4.data, form.sat5.data,
                            form.sat6.data, form.sat7.data],
                'DATE': str(dt.date.today())
            }, ensure_ascii=False)
        else:
            class_.changed_lessons = json.dumps({
                form.day.data: [form.mon1.data, form.mon2.data, form.mon3.data, form.mon4.data, form.mon5.data,
                                form.mon6.data, form.mon7.data],
                'DATE': str(dt.date.today())
            }, ensure_ascii=False)
        text = f"""Изменения на: {form.day.data}
1-{form.mon1.data}
2-{form.mon2.data}
3-{form.mon3.data}
4-{form.mon4.data}
5-{form.mon5.data}
6-{form.mon6.data}
7-{form.mon7.data}"""
        for i in class_.tg_s.split():
            i = int(i)
            url1 = "https://api.telegram.org/bot5457122671:AAGlJPnZ2evD5qUtC9FW3L7wkhmOAbiAXnE/sendMessage?"
            r1 = requests.post(url1, data={'chat_id': i, "text": text})
            if r1.status_code != 200:
                pass
        db_sess.commit()
        return redirect('/admin')
    return render_template('ch_lessons.html', form=form)


@app.route('/add_events', methods=['GET', 'POST'])
def add_event():
    form = AddEvents()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        event = Events()
        event.name = form.name.data
        event.responsible = form.responsible.data
        event.date_time_place = form.date_time_place.data
        db_sess.add(event)
        db_sess.commit()
        return render_template('add_events.html', form=form, message='ОК')
    return render_template('add_events.html', form=form)


@app.route('/del_admin', methods=['GET', 'POST'])
def del_ad():
    form = MakeUnAdmin()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        # user = User()
        user.is_admin = 0
        db_sess.commit()
        return redirect('/admin')
    return render_template('del_admin.html', form=form)


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    form = LoggedForm()
    print(form.validate_on_submit())
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == current_user.id).first()
        user.telegram = form.tg.data
        user.class_ = form.class_.data
        db_sess.commit()
        return render_template('profile.html',
                               form=form, surname=current_user.surname, name=current_user.name,
                               email=current_user.email, tg=current_user.telegram, class_=current_user.class_,
                               message='ОК')
    return render_template('profile.html',
                           form=form, surname=current_user.surname, name=current_user.name,
                           email=current_user.email, tg=current_user.telegram, class_=current_user.class_)


@app.route('/registration', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User()
        user.name = form.name.data
        user.email = form.email.data
        user.surname = form.surname.data
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/test')
def test():
    return render_template('test.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/admin')
@login_required
def admin_panel():
    db_sess = db_session.create_session()
    is_admin = db_sess.query(User).filter(User.id == current_user.id)[0].is_admin
    if is_admin == 1:
        return render_template('admin.html')
    else:
        return redirect('/')


@app.route("/call_schedule")
def events():
    return render_template("call_schedule.html")


@app.route("/events")
def callschedule():
    db_sess = db_session.create_session()
    events = db_sess.query(Events)
    return render_template("events.html", events=events)


def name_of_class(name):
    if name == '10b':
        name = '10Б'
    return name


@app.route("/<class_name>", methods=["GET", "POST"])
def index_w_s(class_name):
    class_name = name_of_class(class_name)
    db_sess = db_session.create_session()
    timetable = db_sess.query(Class).filter(Class.name == class_name)[0].timetable
    temporary_timetable = db_sess.query(Class).filter(Class.name == class_name)[0].changed_lessons
    try:
        temporary_timetable = json.loads(temporary_timetable)
        if temporary_timetable is not None and dt.datetime.strptime(temporary_timetable['DATE'], '%Y-%m-%d') > \
                dt.datetime.today():
            temporary_timetable = json.loads(temporary_timetable)
    except Exception:
        temporary_timetable = 0
    timetable = json.loads(timetable)
    return render_template("timetable.html", class_=class_name, timetable=timetable,
                           temporary_timetable=temporary_timetable)


@app.route('/')
def index():
    return render_template('start.html')


def main():
    db_session.global_init("db/blogs.db")
    app.run()


if __name__ == '__main__':
    main()
