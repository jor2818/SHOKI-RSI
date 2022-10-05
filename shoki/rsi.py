from flask import Blueprint, render_template, url_for, redirect, session, flash, request, send_file
from shoki import db
from .models import User, Rsi
from sqlalchemy import create_engine, or_
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import numpy as np
import seaborn as sns
import os
import io
import mpld3

rsi = Blueprint("rsi",__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

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
        direction = int(request.form['direction'])
        vehicle_type = int(request.form['vehicle_type'])
        addr1_og = request.form['addr1_og']
        addr2_og = request.form['addr2_og']
        addr3_og = request.form['addr3_og']
        zone_og = int(request.form['zone_og'])
        addr1_dn = request.form['addr1_dn']
        addr2_dn = request.form['addr2_dn']
        addr3_dn = request.form['addr3_dn']
        zone_dn = int(request.form['zone_dn'])
        trip_purpose = int(request.form['trip_purpose'])
        if str(vehicle_type) == '1' or str(vehicle_type) == '2':
            passenger12 = int(request.form['passenger12'])
            passenger34 = None
            passenger58 = None
            cargo_type = None
            cargo_weight = None
        elif str(vehicle_type) == '3' or str(vehicle_type) == '4':
            passenger34 = int(request.form['passenger34'])
            passenger12 = None
            passenger58 = None
            cargo_type = None
            cargo_weight = None
        else:
            passenger58 = int(request.form['passenger58'])
            cargo_type = int(request.form['cargo_type'])
            cargo_weight = int(request.form['cargo_weight'])
            passenger12 = None
            passenger34 = None
        income = int(request.form['income'])
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
    
@rsi.route('/showtable', methods=['GET','POST'])
def showtable():
    
    if "username" not in session:
        return redirect(url_for('views.home'))
    
    page = request.args.get('page', 1, type=int)
    rsis = Rsi.query.filter_by(user_id=session["id"]).paginate(page=page,per_page=10)
    
    return render_template('dash_table.html', name='TABLE', rsis=rsis)

    
@rsi.route('/deletersi/<id>', methods=['GET','POST'])
def deletersi(id):
    
    if "username" not in session:
        return redirect(url_for('views.home'))
    
    del_rsi = Rsi.query.get(id)
    db.session.delete(del_rsi)
    db.session.commit()
    flash("ข้อมูลการสำรวจได้ถูกลบเรียบร้อยแล้ว","success")
    return redirect(url_for('rsi.showtable'))

@rsi.route('/<id>/edit/', methods=['GET','POST'])
def updatersi(id):
    
    if "username" not in session:
        return redirect(url_for('views.home'))
    
    rsi = Rsi.query.get_or_404(id)
    
    if request.method == 'POST':
        project_name = request.form['project_name']
        site_name = request.form['site_name']
        direction = int(request.form['direction'])
        vehicle_type = int(request.form['vehicle_type'])
        addr1_og = request.form['addr1_og']
        addr2_og = request.form['addr2_og']
        addr3_og = request.form['addr3_og']
        zone_og = int(request.form['zone_og'])
        addr1_dn = request.form['addr1_dn']
        addr2_dn = request.form['addr2_dn']
        addr3_dn = request.form['addr3_dn']
        zone_dn = int(request.form['zone_dn'])
        trip_purpose = int(request.form['trip_purpose'])
        if str(vehicle_type) == '1' or str(vehicle_type) == '2':
            passenger12 = int(request.form['passenger12'])
            passenger34 = None
            passenger58 = None
            cargo_type = None
            cargo_weight = None
        elif str(vehicle_type) == '3' or str(vehicle_type) == '4':
            passenger34 = int(request.form['passenger34'])
            passenger12 = None
            passenger58 = None
            cargo_type = None
            cargo_weight = None
        else:
            passenger58 = int(request.form['passenger58'])
            cargo_type = int(request.form['cargo_type'])
            cargo_weight = int(request.form['cargo_weight'])
            passenger12 = None
            passenger34 = None
        income = int(request.form['income'])
        surveyor_name = session['username']
        user_id = session['id']
        
        rsi.project_name = project_name
        rsi.site_name = site_name
        rsi.direction = direction
        rsi.vehicle_type = vehicle_type
        rsi.addr1_og = addr1_og
        rsi.addr2_og = addr2_og
        rsi.addr3_og = addr3_og
        rsi.zone_og = zone_og
        rsi.addr1_dn = addr1_dn
        rsi.addr2_dn = addr2_dn
        rsi.addr3_dn = addr3_dn
        rsi.zone_dn = zone_dn
        rsi.passenger12 = passenger12
        rsi.passenger34 = passenger34
        rsi.passenger58 = passenger58
        rsi.cargo_type = cargo_type
        rsi.cargo_weight = cargo_weight
        rsi.income = income
        
        db.session.add(rsi)
        db.session.commit()
        flash("ข้อมูลการสำรวจได้ถูกปรับปรุงเรียบร้อยแล้ว","success")
        return redirect(url_for('rsi.showtable'))
    
    return render_template('dash_editform.html', name='TABLE', rsi=rsi)

@rsi.route('/search', methods=['GET', 'POST'])
def search():
    if "username" not in session:
        return redirect(url_for('views.home'))
    
    page = request.args.get('page', 1, type=int)
    
    
    if request.method == 'POST':      
        search = request.form['search']
        rsis = db.session.query(Rsi).filter(Rsi.user_id==session['id']).filter(
            or_(
                    Rsi.site_name.like(search),
                    Rsi.project_name.like(search)
                )
            ).paginate(page=page,per_page=10)

        return render_template('dash_table.html', name='TABLE', rsis=rsis)
    
    rsis = Rsi.query.filter_by(user_id=session["id"]).paginate(page=page,per_page=10)
    
    return render_template('dash_table.html', name='TABLE', rsis=rsis)
    

@rsi.route('/showanalysis', methods=['GET','POST'])
def showanalysis():
    
    if "username" not in session:
        return redirect(url_for('views.home'))
    
    return render_template('dash_analysis.html', name='ANALYSIS')

@rsi.route('/visualization', methods=['GET','POST'])
def visualization():
    
    if "username" not in session:
        return redirect(url_for('views.home'))
    
    conn = create_engine('sqlite:///' + os.path.join(basedir,'data.sqlite'))
    if request.method == 'POST':
        project_name = str(request.form['project_name'])
        site_name = request.form['site_name']
        sql ='''SELECT * FROM rsi WHERE (user_id=:user_id) AND (project_name=:project_name) AND (site_name=:site_name)'''
        df = pd.read_sql(sql, conn, params={'user_id': session['id'],'project_name':project_name,'site_name':site_name})
        print(df)
        if df.empty:
            flash("รหัสโครงการและจุดสำรวจที่ท่านเลือกไม่มีข้อมูล!!!","danger")
            return redirect(url_for('rsi.showanalysis'))
        else:
            

            vehicleType = df.groupby('vehicle_type')['vehicle_type'].count()
            veh_labels = []
            values = []
            i = 0
            for label in vehicleType.index:
                if label == 1:
                    veh_labels.append('จักรยาน/รถจักรยานยนต์')
                    values.append(vehicleType.values[i])
                    i = i + 1
                elif label == 2:
                    veh_labels.append('รถยนต์ส่วนบุคคล 4 ล้อ/รถกระบะ/รถโฟวีล')
                    values.append(vehicleType.values[i])
                    i = i + 1
                elif label == 3:
                    veh_labels.append('รถสองแถว 4 ล้อ/รถตู้โดยสาร/รถกะป้อ')
                    values.append(vehicleType.values[i])
                    i = i + 1
                elif label == 4:
                    veh_labels.append('รถสองแถว 6 ล้อ/รถโดยสาร')
                    values.append(vehicleType.values[i])
                    i = i + 1
                elif label == 5:
                    veh_labels.append('รถบรรทุก 4 ล้อ')
                    values.append(vehicleType.values[i])
                    i = i + 1
                elif label == 6:
                    veh_labels.append('รถบรรทุก 6 ล้อ')
                    values.append(vehicleType.values[i])
                    i = i + 1
                elif label == 7:
                    veh_labels.append('รถบรรทุก 10 ล้อ')
                    values.append(vehicleType.values[i])
                    i = i + 1
                elif label == 8:
                    veh_labels.append('รถพ่วง/รถเทรเลอร์')
                    values.append(vehicleType.values[i])
                    i = i + 1
                else:
                    values.append(0)

            x = np.arange(len(veh_labels))     
            fig, ax = plt.subplots(figsize=(5,5))
            ax = plt.gca()
            print(x)
            print(veh_labels)
            print(values)
            vehiclebar = ax.bar(veh_labels, values)
            ax.set_ylabel('จำนวน (คัน)', fontweight='bold', fontsize='14', horizontalalignment='center')
            ax.set_title('ประเภทยานพาหนะ',fontsize='20')
            ax.set_xticks(x)
            ax.set_xticklabels(labels=veh_labels)

            
            # ax.pie(values, labels=labels, autopct='%1.1f%%')
            # ax.axis('equal')
            
            #fig.suptitle(u'ประเภทยานพาหนะ', fontsize='20')
            fig.tight_layout()


            return render_template('dash_visualization.html', name='ANALYSIS', plot=mpld3.fig_to_html(fig))
            
    
    return render_template('dash_analysis.html', name='ANALYSIS')