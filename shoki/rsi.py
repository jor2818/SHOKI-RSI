from flask import Blueprint, render_template, url_for, redirect, session, flash, request
from shoki import db
from .models import User, Rsi

rsi = Blueprint("rsi",__name__)

@rsi.route('/showform', methods=['GET','POST'])
def showform():
    
    if "username" not in session:
        return redirect(url_for('views.home'))
    
    return render_template('dash_form.html', name='FORM')

@rsi.route('/addrsi', methods=['GET','POST'])
def addrsi():
    
    if "username" not in session:
        return redirect(url_for('views.home'))
    
    if request.method == 'POST':
        project_name = request.form['project_name']
        site_name = request.form['site_name']
        direction = request.form['direction']
        vehicle_type = request.form['vehicle_type']
        addr1_og = request.form['addr1_og']
        addr2_og = request.form['addr2_og']
        addr3_og = request.form['addr3_og']
        zone_og = request.form['zone_og']
        addr1_dn = request.form['addr1_dn']
        addr2_dn = request.form['addr2_dn']
        addr3_dn = request.form['addr3_dn']
        zone_dn = request.form['zone_dn']
        trip_purpose = request.form['trip_purpose']
        if vehicle_type == '1' or vehicle_type == '2':
            passenger12 = request.form['passenger12']
            passenger34 = None
            passenger58 = None
            cargo_type = None
            cargo_weight = None
        elif vehicle_type == '3' or vehicle_type == '4':
            passenger34 = request.form['passenger34']
            passenger12 = None
            passenger58 = None
            cargo_type = None
            cargo_weight = None
        else:
            passenger58 = request.form['passenger58']
            cargo_type = request.form['cargo_type']
            cargo_weight = request.form['cargo_weight']
            passenger12 = None
            passenger34 = None
        income = request.form['income']
        surveyor_name = session['username']
        user_id = session['id']
        
        rsi = Rsi(project_name=project_name,site_name=site_name,direction=direction,vehicle_type=vehicle_type,addr1_og=addr1_og,addr2_og=addr2_og,addr3_og=addr3_og,
                  zone_og=zone_og,addr1_dn=addr1_dn,addr2_dn=addr2_dn,addr3_dn=addr3_dn,zone_dn=zone_dn,trip_purpose=trip_purpose,
                  passenger12=passenger12,passenger34=passenger34,passenger58=passenger58,cargo_type=cargo_type,
                  cargo_weight=cargo_weight,income=income,surveyor_name=surveyor_name,user_id=user_id)
        db.session.add(rsi)
        db.session.commit()
        flash("ข้อมูลการสำรวจได้ถูกจัดเก็บเรียบร้อยแล้ว","success")
        return redirect(url_for('rsi.showform'))