from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import *
import datetime
from . import db
views = Blueprint('views', __name__)


@views.route('/', methods=["GET", "POST"])
@login_required
def home():
    if request.method == "POST":
        title = note=request.form.get("title")
        note=request.form.get("note")
        date = request.form.get("date")
        time = request.form.get("time")
        flag_every = request.form.get("Flag_every")=="1"
        flag_singl = request.form.get("Flag_singl")=="1"

        if len(title)<1:
            flash("Напиши хотя-бы один символ, лол", category="error")

        elif len(note) < 1:
            flash("Напиши хотя-бы один символ, лол", category="error")

        elif len(date)!=10 and len(date)!=9 and len(date)!=8:
            flash("Ну ты не попал ни в какие рамки даты)", category="error")

        elif len(time)<3 or len(time)>5:
            flash("Ну ты не попал ни в какие временные рамки)", category="error")

        else:
            date = list(map(int, date.split(':')))
            time = list(map(int, time.split(':')))
            if flag_every:
                flag=1
            elif flag_singl:
                flag=0
            date = datetime.datetime(year = date[2],
                                     month = date[1],
                                     day  = date[0],
                                     hour = time[0],
                                     minute = time[1])
            new_note=Note(title = title, data=note, date = date, flag=flag, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash("Kакой молодчинка, твоя запись была добавлена)", category="success")
    day = datetime.datetime.now()
    delta_day = datetime.timedelta(days=1)
    user = current_user
    today_notes=[]
    for note in user.notes:
        if abs(note.date-day) < delta_day:
            today_notes.append(note)
    return render_template("home.html",user=current_user, day=day, delta_day=delta_day, today_notes=today_notes, key=really_secret_key())


@views.route("/userpost/<int:days>/")
def posts_view(days):
    day = datetime.datetime.now()+datetime.timedelta(days=days)
    delta_day = datetime.timedelta(days=1)
    user = current_user
    today_notes=[]
    for note in user.notes:
        if note.flag==1:
            if abs(note.date-day).days%7 < delta_day.days:
                today_notes.append(note)


        elif note.flag==0:
            if abs(note.date-day) < delta_day:
                today_notes.append(note)


    return render_template("PostWithDateView.html",user=current_user, day=day, delta_day=delta_day, today_notes=today_notes, key=really_secret_key())

@views.route("/userpost/<int:noteId>/delete")
def post_del(noteId):
    note=Note.query.get(noteId)
    if note:
        if note.user_id==current_user.id:
            db.session.delete(note)
            db.session.commit()
        else:
            flash("Ты чорт, чо делаешь не в своём аккаунте?", category="error")
    return redirect(url_for("views.home"))

@views.route("/userlist")
def userlist():
    users=User.query.order_by(User.id).all()
    return render_template("userlist.html", user= current_user, users=users, key=really_secret_key())




@views.route("/user/<int:userId>/delete")
def user_del(userId):
    user = User.query.get(userId)
    if user:
        if current_user.email==really_secret_key():
            db.session.delite(user)
            db.session.commit()
        else:
            flash("Ты чорт, чо делаешь не в своём аккаунте?", category="error")
    return redirect(url_for("views.userlist"))
