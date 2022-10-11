from flask import Blueprint, render_template, url_for, redirect


views = Blueprint("views",__name__)

@views.route("/")
@views.route("/home")
def home():
    return render_template('home.html', name="HOME")

@views.route("/signup")
def signup():
    return render_template('signup.html', name="SIGNUP")

@views.route("/about")
def about():
    return render_template('about.html', name="ABOUT")

