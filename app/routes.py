from flask import Blueprint, render_template, request, redirect, url_for, session
from datetime import datetime, timezone
import random

from app import db
from app.models import User, Spin

main = Blueprint("main", __name__)


quotes = {
    1: "Believe in yourself.",
    2: "Every day is a new opportunity.",
    3: "Small steps lead to big results.",
    4: "Stay positive and keep going.",
    5: "Your effort will pay off.",
    6: "Great things take time.",
    7: "Dream big and work hard.",
    8: "You are capable of amazing things.",
    9: "Success starts with consistency.",
    10: "Keep learning, keep growing.",
    11: "Your future is created by what you do today.",
    12: "Never stop improving.",
    13: "Focus on progress, not perfection.",
    14: "Believe that you can.",
    15: "Make today count.",
    16: "Stay curious.",
    17: "Challenges make you stronger.",
    18: "Be proud of your progress.",
    19: "Keep moving forward.",
    20: "Your hard work matters.",
    21: "Good things are coming.",
    22: "Turn obstacles into opportunities.",
    23: "You have the power to change your story.",
    24: "Consistency creates results.",
    25: "Today is your chance to shine."
}


@main.route("/")
def home():
    return render_template("index.html")


@main.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        name = request.form.get("name")
        dob_string = request.form.get("dob")

        if not name or not dob_string:
            return "Name and date of birth are required", 400

        dob = datetime.strptime(
            dob_string,
            "%Y-%m-%d"
        ).date()

        user = User.query.filter_by(
            name=name,
            date_of_birth=dob
        ).first()

        if not user:
            user = User(
                name=name,
                date_of_birth=dob
            )

            db.session.add(user)
            db.session.commit()

        session["user_id"] = user.id

        return redirect(url_for("main.dashboard"))

    return render_template("login.html")


@main.route("/dashboard")
def dashboard():

    user_id = session.get("user_id")

    if not user_id:
        return redirect(url_for("main.login"))

    user = User.query.get(user_id)

    today = datetime.now(timezone.utc).date()

    spins_today = Spin.query.filter(
        Spin.user_id == user_id,
        Spin.spun_at >= datetime.combine(
            today,
            datetime.min.time(),
            tzinfo=timezone.utc
        )
    ).count()

    spins_remaining = max(0, 3 - spins_today)

    return render_template(
        "dashboard.html",
        user=user,
        spins_used=spins_today,
        spins_remaining=spins_remaining
    )


@main.route("/spin", methods=["POST"])
def spin():

    user_id = session.get("user_id")

    if not user_id:
        return redirect(url_for("main.login"))

    today = datetime.now(timezone.utc).date()

    spins_today = Spin.query.filter(
        Spin.user_id == user_id,
        Spin.spun_at >= datetime.combine(
            today,
            datetime.min.time(),
            tzinfo=timezone.utc
        )
    ).count()

    if spins_today >= 3:
        return render_template(
            "result.html",
            success=False,
            message="You have used all 3 spins for today."
        )

    number = random.randint(1, 25)
    quote = quotes[number]

    new_spin = Spin(
        user_id=user_id,
        number=number,
        quote=quote
    )

    db.session.add(new_spin)
    db.session.commit()

    return render_template(
        "result.html",
        success=True,
        number=number,
        quote=quote,
        spins_used=spins_today + 1,
        spins_remaining=2 - spins_today
    )


@main.route("/history")
def history():

    user_id = session.get("user_id")

    if not user_id:
        return redirect(url_for("main.login"))

    spins = Spin.query.filter_by(
        user_id=user_id
    ).order_by(
        Spin.spun_at.desc()
    ).all()

    return render_template(
        "history.html",
        spins=spins
    )


@main.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("main.login"))

