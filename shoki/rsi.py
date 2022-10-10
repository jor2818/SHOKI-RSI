from flask import Blueprint, render_template, url_for, redirect, session, flash, request, send_file, make_response
from shoki import db
from .models import User, Rsi
from sqlalchemy import create_engine, or_
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import os
from io import BytesIO
from matplotlib.figure import Figure
import base64

rsi = Blueprint("rsi",__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

def built_bar(data,var,xlabel,ylabel,rotation=0):
    fig = Figure()
    g = fig.subplots()
    plt.rcParams['font.family'] = 'tahoma'
    g = sns.countplot(data=data, x=var, palette=sns.color_palette('pastel'))
    g.set_ylabel(ylabel, fontweight='bold', fontsize='14', horizontalalignment='center')
    g.set_xlabel(xlabel, fontweight='bold', fontsize='14', horizontalalignment='center')
    #g.set_title(title, fontweight='bold', fontsize='14', horizontalalignment='center')
    plt.xticks(rotation=rotation, ha='center')
    buf = BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    data = base64.b64encode(buf.getvalue()).decode('utf8')
    return data

def built_pie(x,y):
    fig = Figure()
    g = fig.subplots()
    plt.rcParams['font.family'] = 'tahoma'
    colors = sns.color_palette('pastel')
    plt.pie(x, labels=y, autopct='%1.1f%%',colors=colors)
    plt.axis('equal')
    buf = BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    data = base64.b64encode(buf.getvalue()).decode('utf8')
    return data

def built_heatmap(x,y):
    fig = Figure()
    g = fig.subplots()
    g = sns.heatmap(pd.crosstab(x, y), cmap="YlGnBu",annot=True)
    buf = BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    data = base64.b64encode(buf.getvalue()).decode('utf8')
    return data

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
        zone_og = int(request.form['zone_og'])
        addr1_dn = request.form['addr1_dn']
        addr2_dn = request.form['addr2_dn']
        addr3_dn = request.form['addr3_dn']
        zone_dn = int(request.form['zone_dn'])
        trip_purpose = request.form['trip_purpose']
        if str(vehicle_type) == "จักรยาน/รถจักรยานยนต์" or str(vehicle_type) == "รถยนต์นั่งส่วนบุคคล 4 ล้อ/รถกระบะ/รถโฟวีล":
            passenger12 = int(request.form['passenger12'])
            passenger34 = None
            passenger58 = None
            cargo_type = None
            cargo_weight = None
        elif str(vehicle_type) == "รถสองแถว 4 ล้อ/รถตู้โดยสาร/รถกะป้อ" or str(vehicle_type) == "รถสองแถว 6 ล้อ/รถโดยสาร":
            passenger34 = request.form['passenger34']
            passenger12 = None
            passenger58 = None
            cargo_type = None
            cargo_weight = None
        else:
            passenger58 = int(request.form['passenger58'])
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
        direction = request.form['direction']
        vehicle_type = request.form['vehicle_type']
        addr1_og = request.form['addr1_og']
        addr2_og = request.form['addr2_og']
        addr3_og = request.form['addr3_og']
        zone_og = int(request.form['zone_og'])
        addr1_dn = request.form['addr1_dn']
        addr2_dn = request.form['addr2_dn']
        addr3_dn = request.form['addr3_dn']
        zone_dn = int(request.form['zone_dn'])
        trip_purpose = request.form['trip_purpose']
        if str(vehicle_type) == "จักรยาน/รถจักรยานยนต์" or str(vehicle_type) == "รถยนต์นั่งส่วนบุคคล 4 ล้อ/รถกระบะ/รถโฟวีล":
            passenger12 = int(request.form['passenger12'])
            passenger34 = None
            passenger58 = None
            cargo_type = None
            cargo_weight = None
        elif str(vehicle_type) == "รถสองแถว 4 ล้อ/รถตู้โดยสาร/รถกะป้อ" or str(vehicle_type) == "รถสองแถว 6 ล้อ/รถโดยสาร":
            passenger34 = request.form['passenger34']
            passenger12 = None
            passenger58 = None
            cargo_type = None
            cargo_weight = None
        else:
            passenger58 = int(request.form['passenger58'])
            cargo_type = request.form['cargo_type']
            cargo_weight = request.form['cargo_weight']
            passenger12 = None
            passenger34 = None
        income = request.form['income']
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
        global df
        
        project_name = str(request.form['project_name'])
        site_name = request.form['site_name']
        if site_name == 'all' or site_name=='All':            
            sql ='''SELECT * FROM rsi WHERE (user_id=:user_id) AND (project_name=:project_name)'''
            df = pd.read_sql(sql, conn, params={'user_id': session['id'],'project_name':project_name})
        else:
            sql ='''SELECT * FROM rsi WHERE (user_id=:user_id) AND (project_name=:project_name) AND (site_name=:site_name)'''
            df = pd.read_sql(sql, conn, params={'user_id': session['id'],'project_name':project_name,'site_name':site_name})
        print(df)
        
        if df.empty:
            flash("รหัสโครงการและจุดสำรวจที่ท่านเลือกไม่มีข้อมูล!!!","danger")
            return redirect(url_for('rsi.showanalysis'))
        else:
            
            vehicleType = df.groupby('vehicle_type')['vehicle_type'].count()
            data1 = built_bar(df,'vehicle_type','ประเภทยานพาหนะ','จำนวน(คัน)',rotation=15)
            data2 = built_pie(vehicleType.values,vehicleType.index)
            tripPurpose = df.groupby('trip_purpose')['trip_purpose'].count()
            data3 = built_bar(df,'trip_purpose','วัตถุประสงค์การเดินทาง','จำนวน(เที่ยว)')
            data4 = built_pie(tripPurpose.values,tripPurpose.index)
            cargoType = df.groupby('cargo_type')['cargo_type'].count()
            data5 = built_bar(df,'cargo_type','ชนิดสินค้า','จำนวน(คัน)')
            data6 = built_pie(cargoType.values,cargoType.index)
            cargoWeight = df.groupby('cargo_weight')['cargo_weight'].count()
            data7 = built_bar(df,'cargo_weight','น้ำหนักสินค้า','จำนวน(คัน)')
            data8 = built_pie(cargoWeight.values,cargoWeight.index)
            pass34 = df.groupby('passenger34')['passenger34'].count()
            data9 = built_bar(df,'passenger34','ปริมาณผู้โดยสาร','จำนวน(คัน)')
            data10 = built_pie(pass34.values,pass34.index)
            pc_pass = df.loc[df['passenger12'].notnull(),['passenger12']]
            data11 = pc_pass.mean()
            tk_pass = df.loc[df['passenger58'].notnull(),['passenger58']]
            income = df.groupby('income')['income'].count()
            data14 = built_bar(df,'income','ระดับรายได้','จำนวน')
            data15 = built_pie(income.values,income.index)
            data12 = tk_pass.mean()
            data13 = built_heatmap(df.zone_og,df.zone_dn)

            return render_template('dash_visualization.html', name='ANALYSIS', df=df, data1=data1, data2=data2, data3=data3, 
                                   data4=data4, data5=data5, data6=data6, data7=data7, data8=data8, data9=data9, data10=data10,
                                   data11=data11, data12=data12, data13=data13, data14=data14, data15=data15)
            
    
    return render_template('dash_analysis.html', name='ANALYSIS')

@rsi.route('/exportChart01', methods=['GET','POST'])
def exportChart01():
    
    if "username" not in session:
        return redirect(url_for('views.home'))
             
    fig = Figure()
    g = fig.subplots()
    plt.rcParams['font.family'] = 'tahoma'
    g = sns.countplot(df, x='vehicle_type', palette=sns.color_palette('pastel'))
    g.set_ylabel('จำนวน(คัน)', fontweight='bold', fontsize='14', horizontalalignment='center')
    g.set_xlabel('ประเภทยานพาหนะ', fontweight='bold', fontsize='14', horizontalalignment='center')

    plt.xticks(rotation=15, ha='center')
    plt.tight_layout()
    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    
    return send_file(buf, mimetype='image/png', as_attachment=True, download_name='Chart01.png')
    
 
@rsi.route('/exportChart02', methods=['GET','POST'])
def exportChart02():
    
    if "username" not in session:
        return redirect(url_for('views.home'))
    
    vehicleType = df.groupby('vehicle_type')['vehicle_type'].count()
    fig = Figure()
    g = fig.subplots()
    plt.rcParams['font.family'] = 'tahoma'
    colors = sns.color_palette('pastel')
    plt.pie(vehicleType.values, labels=vehicleType.index, autopct='%1.1f%%',colors=colors)
    plt.axis('equal')
    plt.tight_layout()
    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    
    return send_file(buf, mimetype='image/png', as_attachment=True, download_name='Chart02.png')

@rsi.route('/exportChart03', methods=['GET','POST'])
def exportChart03():
    
    if "username" not in session:
        return redirect(url_for('views.home'))
             
    fig = Figure()
    g = fig.subplots()
    plt.rcParams['font.family'] = 'tahoma'
    g = sns.countplot(df, x='trip_purpose', palette=sns.color_palette('pastel'))
    g.set_ylabel('จำนวน(เที่ยว)', fontweight='bold', fontsize='14', horizontalalignment='center')
    g.set_xlabel('วัตถุประสงค์การเดินทาง', fontweight='bold', fontsize='14', horizontalalignment='center')

    plt.xticks(rotation=0, ha='center')
    plt.tight_layout()
    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    
    return send_file(buf, mimetype='image/png', as_attachment=True, download_name='Chart03.png')

@rsi.route('/exportChart04', methods=['GET','POST'])
def exportChart04():
    
    if "username" not in session:
        return redirect(url_for('views.home'))
    
    tripPurpose = df.groupby('trip_purpose')['trip_purpose'].count()
    fig = Figure()
    g = fig.subplots()
    plt.rcParams['font.family'] = 'tahoma'
    colors = sns.color_palette('pastel')
    plt.pie(tripPurpose.values, labels=tripPurpose.index, autopct='%1.1f%%',colors=colors)
    plt.axis('equal')
    plt.tight_layout()
    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    
    return send_file(buf, mimetype='image/png', as_attachment=True, download_name='Chart04.png')

@rsi.route('/exportChart05', methods=['GET','POST'])
def exportChart05():
    
    if "username" not in session:
        return redirect(url_for('views.home'))
             
    fig = Figure()
    g = fig.subplots()
    plt.rcParams['font.family'] = 'tahoma'
    g = sns.countplot(df, x='cargo_type', palette=sns.color_palette('pastel'))
    g.set_ylabel('จำนวน(คัน)', fontweight='bold', fontsize='14', horizontalalignment='center')
    g.set_xlabel('ชนิดสินค้า', fontweight='bold', fontsize='14', horizontalalignment='center')

    plt.xticks(rotation=0, ha='center')
    plt.tight_layout()
    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    
    return send_file(buf, mimetype='image/png', as_attachment=True, download_name='Chart05.png')

@rsi.route('/exportChart06', methods=['GET','POST'])
def exportChart06():
    
    if "username" not in session:
        return redirect(url_for('views.home'))
    
    cargoType = df.groupby('cargo_type')['cargo_type'].count()
    fig = Figure()
    g = fig.subplots()
    plt.rcParams['font.family'] = 'tahoma'
    colors = sns.color_palette('pastel')
    plt.pie(cargoType.values, labels=cargoType.index, autopct='%1.1f%%',colors=colors)
    plt.axis('equal')
    plt.tight_layout()
    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    
    return send_file(buf, mimetype='image/png', as_attachment=True, download_name='Chart06.png')

@rsi.route('/exportChart07', methods=['GET','POST'])
def exportChart07():
    
    if "username" not in session:
        return redirect(url_for('views.home'))
             
    fig = Figure()
    g = fig.subplots()
    plt.rcParams['font.family'] = 'tahoma'
    g = sns.countplot(df, x='cargo_weight', palette=sns.color_palette('pastel'))
    g.set_ylabel('จำนวน(คัน)', fontweight='bold', fontsize='14', horizontalalignment='center')
    g.set_xlabel('น้ำหนักสินค้า', fontweight='bold', fontsize='14', horizontalalignment='center')

    plt.xticks(rotation=0, ha='center')
    plt.tight_layout()
    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    
    return send_file(buf, mimetype='image/png', as_attachment=True, download_name='Chart07.png')

@rsi.route('/exportChart08', methods=['GET','POST'])
def exportChart08():
    
    if "username" not in session:
        return redirect(url_for('views.home'))
    
    cargoWeight = df.groupby('cargo_weight')['cargo_weight'].count()
    fig = Figure()
    g = fig.subplots()
    plt.rcParams['font.family'] = 'tahoma'
    colors = sns.color_palette('pastel')
    plt.pie(cargoWeight.values, labels=cargoWeight.index, autopct='%1.1f%%',colors=colors)
    plt.axis('equal')
    plt.tight_layout()
    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    
    return send_file(buf, mimetype='image/png', as_attachment=True, download_name='Chart08.png')

@rsi.route('/exportChart09', methods=['GET','POST'])
def exportChart09():
    
    if "username" not in session:
        return redirect(url_for('views.home'))
             
    fig = Figure()
    g = fig.subplots()
    plt.rcParams['font.family'] = 'tahoma'
    g = sns.countplot(df, x='passenger34', palette=sns.color_palette('pastel'))
    g.set_ylabel('จำนวน(คัน)', fontweight='bold', fontsize='14', horizontalalignment='center')
    g.set_xlabel('ปริมาณผู้โดยสาร', fontweight='bold', fontsize='14', horizontalalignment='center')

    plt.xticks(rotation=0, ha='center')
    plt.tight_layout()
    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    
    return send_file(buf, mimetype='image/png', as_attachment=True, download_name='Chart09.png')

@rsi.route('/exportChart10', methods=['GET','POST'])
def exportChart10():
    
    if "username" not in session:
        return redirect(url_for('views.home'))
    
    pass34 = df.groupby('passenger34')['passenger34'].count()
    fig = Figure()
    g = fig.subplots()
    plt.rcParams['font.family'] = 'tahoma'
    colors = sns.color_palette('pastel')
    plt.pie(pass34.values, labels=pass34.index, autopct='%1.1f%%',colors=colors)
    plt.axis('equal')
    plt.tight_layout()
    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    
    return send_file(buf, mimetype='image/png', as_attachment=True, download_name='Chart10.png')

@rsi.route('/exportChart11', methods=['GET','POST'])
def exportChart11():
    
    if "username" not in session:
        return redirect(url_for('views.home'))
             
    fig = Figure()
    g = fig.subplots()
    plt.rcParams['font.family'] = 'tahoma'
    g = sns.countplot(df, x='income', palette=sns.color_palette('pastel'))
    g.set_ylabel('จำนวน', fontweight='bold', fontsize='14', horizontalalignment='center')
    g.set_xlabel('ระดับรายได้', fontweight='bold', fontsize='14', horizontalalignment='center')

    plt.xticks(rotation=0, ha='center')
    plt.tight_layout()
    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    
    return send_file(buf, mimetype='image/png', as_attachment=True, download_name='Chart11.png')

@rsi.route('/exportChart12', methods=['GET','POST'])
def exportChart12():
    
    if "username" not in session:
        return redirect(url_for('views.home'))
    
    income = df.groupby('income')['income'].count()
    fig = Figure()
    g = fig.subplots()
    plt.rcParams['font.family'] = 'tahoma'
    colors = sns.color_palette('pastel')
    plt.pie(income.values, labels=income.index, autopct='%1.1f%%',colors=colors)
    plt.axis('equal')
    plt.tight_layout()
    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    
    return send_file(buf, mimetype='image/png', as_attachment=True, download_name='Chart12.png')

@rsi.route('/exportOD', methods=['GET','POST'])
def exportOD():
    
    if "username" not in session:
        return redirect(url_for('views.home'))
    
        
    od = pd.crosstab(df.zone_og,df.zone_dn)

    resp = make_response(od.to_csv(index=True,header=True))
    resp.headers["Content-Disposition"] = "attachment; filename=ExportOD.csv"
    resp.headers["Content-Type"] = "text/csv" 
    
    return resp

@rsi.route('/exportData', methods=['GET','POST'])
def exportData():
    
    if "username" not in session:
        return redirect(url_for('views.home'))
    
    resp = make_response(df.to_csv(index=False, header=True))
    resp.headers["Content-Disposition"] = "attachment; filename=ExportOD.csv"
    resp.headers["Content-Type"] = "text/csv" 
    
    return resp