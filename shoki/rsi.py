from flask import Blueprint, render_template, url_for, redirect, session, flash, request
from shoki import db
from .models import User

rsi = Blueprint("rsi",__name__)

@rsi.route('/showform', methods=['GET','POST'])
def showform():
    
    if "username" not in session:
        return redirect(url_for('views.home'))
    
    return render_template('dash_form.html', name='FORM')