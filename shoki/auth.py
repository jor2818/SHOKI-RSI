from flask import Blueprint, render_template, url_for, redirect, session, flash, request
from shoki import db
from .models import User

auth = Blueprint("auth",__name__)

@auth.route('/adduser', methods=['GET','POST'])
def adduser():
    
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password_1']
        con_password = request.form['password_2']
        
        if len(username)<2:
            flash("ชื่อผู้ใช้ควรมีมากกว่า 2 ตัวอักษร กรุณากรอกอีกครั้ง!!!", "danger")

        elif len(email)<7:
            flash("อีเมลล์ไม่ถูกต้อง กรุณากรอกอีกครั้ง!!!", "danger")
        
        elif password != con_password:
            flash("รหัสผ่านไม่ตรงกัน กรุณากรองอีกครั้ง!!!", "danger")
            
        else:
            user = User.query.filter_by(email=email).first()
            if user:
                flash('อีเมลล์นี้มีการใช้งานในแอพลิเคชันแล้ว กรุณาเปลี่ยนอีเมลล์','danger')
                return redirect(url_for('views.signup'))
            user = User(username=username,email=email,password=password)
            db.session.add(user)
            db.session.commit()
            flash('ขอบคุณที่ลงทะเบียนเข้าใช้', 'success')
            return redirect(url_for('views.home'))
            
    return redirect(url_for('views.signup'))

@auth.route('/login', methods=['GET', 'POST'])
def login():
    
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = User.query.filter_by(email=email).first()
        
        if user is not None:
            if user.check_password(password):
                session['username'] = user.username
                session['id'] = user.id
                session.permanent = True
                flash('ยินดีต้อนรับสู่แอพลิเคชั่น','success')
                return redirect(url_for('rsi.showform'))
            else:
                flash('รหัสไม่ถูกต้อง โปรดลองอีกครั้ง','danger')
        else:       
            flash('อีเมลล์ไม่ถูกต้องหรือไม่คุณยังไม่ได้ลงทะเบียนเข้าใช้','danger')
        
    return render_template('home.html')

@auth.route('/logoff')
def logoff():
    session.clear()
    flash('คุณได้ออกจากแอพลิเคชั่นแล้ว ขอบคุณที่ใช้บริการ', 'success')    
    return redirect(url_for('views.home'))