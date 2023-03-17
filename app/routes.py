from app import app, db, User, Achievement
from flask import render_template, redirect, request, session, url_for
from app.website_processing import get_user_data, add_user, change_user_info, random_count_coins, take_bonus
from app.settings import get_settings, get_interface_text
from app.interaction import Console

from forms import *


consoles = {}


@app.route('/')
@app.route('/index')
def index():
    if 'username' in session:
        return redirect(url_for('user_profile', user_id=get_user_data(db, User, session["username"]).id))
    interface = get_interface_text("en")
    return render_template("index.html", interface=interface)


@app.route('/register', methods=["GET", "POST"])
def register():
    if 'username' in session:
        return redirect(url_for('user_profile', user_id=get_user_data(db, User, session["username"]).id))
    form = RegisterForm()
    interface = get_interface_text("en")
    if form.validate_on_submit():
        # Adding user without checking, because validators already check it.
        add_user(db, User, username=request.form["username"], email=request.form["email"], password=request.form["password"])
        session['username'] = request.form["username"]
        return redirect(url_for('user_profile', user_id=get_user_data(db, User, request.form["username"]).id))
    return render_template('register.html', form=form, interface=interface)


@app.route('/login', methods=["GET", "POST"])
def login():
    if 'username' in session:
        return redirect(url_for('user_profile', user_id=get_user_data(db, User, session["username"]).id))
    form = LoginForm()
    interface = get_interface_text("en")
    if form.validate_on_submit():
        # Adding user without checking, because validators already check it.
        user = User.query.filter_by(username=request.form["username"]).first()
        session['username'] = request.form["username"]
        return redirect(url_for('user_profile', user_id=get_user_data(db, User, request.form["username"]).id))
    return render_template('login.html', form=form, interface=interface)


@app.route('/logout')
def logout():
    if 'username' in session:
        session.clear()
    return redirect(url_for('index'))


@app.route('/users')
def user_list():
    if 'username' not in session:
        return redirect(url_for("login"))
    user = get_user_data(db, User, session['username'])
    interface = get_interface_text(user.language)
    return render_template('user_list.html', users=User.query.all(), user=user, interface=interface)


@app.route('/top')
def top_users():
    if 'username' not in session:
        return redirect(url_for("login"))
    user = get_user_data(db, User, session['username'])
    interface = get_interface_text(user.language)
    return render_template('top_users.html', users=User.query.order_by(User.coins.desc()).all()[:get_settings("top_users_count")], user=get_user_data(db, User, session["username"]), interface=interface)


@app.route('/user/<int:user_id>')
def user_profile(user_id: int):
    if 'username' not in session:
        return redirect(url_for("login"))
    profile_owner=User.query.get(user_id)
    user = get_user_data(db, User, session['username'])
    interface = get_interface_text(user.language)
    achievements = Achievement.query.filter_by(author=profile_owner.username).all()
    return render_template('user_profile.html', user=user, achievements=achievements, profile_owner=profile_owner, interface=interface, get_settings=get_settings)


@app.route('/console', methods=["GET", "POST"])
def console():
    if 'username' not in session:
        return redirect(url_for("login"))
    user = get_user_data(db, User, session["username"])
    if user.rank == "Moderator":
        form = ConsoleForm()
        interface = get_interface_text(user.language)
        _console = consoles.get(user.id)
        if not _console:
            _console = Console()
            consoles[user.id] = _console
        if request.method == "POST":
            command = request.form["command"]
            _console.dispatcher(command)
            consoles[user.id] = _console
        return render_template("console.html", user=user, form=form, console=_console, interface=interface)
    else:
        return "No such permissions"


@app.route('/bank', methods=["GET", "POST"])
def bank():
    if 'username' not in session:
        return redirect(url_for("login"))
    form = CoinsForm()
    user = get_user_data(db, User, session["username"])
    interface = get_interface_text(user.language)
    if request.method == "POST":
        new_coins = random_count_coins()
        indent = take_bonus(db, Achievement, user, new_coins)
        remain = ""
        if indent:
            new_coins = None
            remain = interface.get("bank_remain").format(indent)
        return render_template('bank.html', form=form, user=user, new_coins=new_coins, remain=remain, interface=interface)
    return render_template('bank.html', form=form, user=user, interface=interface)


@app.route('/settings', methods=["GET", "POST"])
def settings():
    if 'username' not in session:
        return redirect(url_for("login"))
    user=get_user_data(db, User, session["username"])
    form = SettingsForm()
    if form.validate_on_submit():
        if request.form["language"] != "-":
            change_user_info(db, user, language=request.form["language"])
    interface = get_interface_text(user.language)
    return render_template("settings.html", form=form, user=user, interface=interface)
