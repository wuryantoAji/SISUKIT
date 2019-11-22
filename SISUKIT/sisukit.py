import sqlite3
import os
from flask import Flask
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, send_from_directory
)
from flask import current_app as app
from SISUKIT.db import get_db
from datetime import date
from werkzeug.utils import secure_filename
from . import auth


bp = Blueprint('sisukit', __name__, url_prefix='/sisukit')
ALLOWED_EXTENSIONS = set(['pdf','png','jpg','jpeg'])

def dict_factory(cursor,row):
    d={}
    for idx,col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def get_session_state():
    if 'access_token' in session:
        return True
    else:
        return False

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    if(get_session_state() == False):
        return redirect(url_for('auth.login'))

    uploads = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    return send_from_directory(directory=uploads, filename=filename)     

@bp.route('/sekre/listSuratSakit', methods=['GET'])
def list_surat_sakit_sekre():
    if(get_session_state() == False):
        return redirect(url_for('auth.login'))

    nama_user = session['user_name']
    role_user = session['role']

    if(role_user != 'sekre'):
        flash('Halaman tidak bisa diakses oleh mahasiswa')
        return redirect(url_for('sisukit.list_surat_sakit_mahasiswa'))

    list_surat = []
    db = get_db()
    surat = db.execute(
        'SELECT * FROM surat_sakit')#now by username then by NPM
    list_surat = surat
    list_param = [nama_user,role_user,list_surat]
    return render_template('list-surat-sekre.html', list_param = list_param)


@bp.route('/sekre/detilSuratSakit/<id>', methods=['GET'])
def detil_surat_sakit_sekre(id):
    if(get_session_state() == False):
        return redirect(url_for('auth.login'))

    nama_user = session['user_name']
    role_user = session['role']

    if(role_user != 'sekre'):
        flash('Halaman tidak bisa diakses oleh mahasiswa')
        return redirect(url_for('sisukit.list_surat_sakit_mahasiswa'))

    db = get_db()
    db.row_factory = dict_factory
    cur = db.cursor()
    surat = cur.execute(
        'SELECT * FROM surat_sakit WHERE id=?',(id,))
    srt = surat.fetchall()
    detail = cur.execute(
        'SELECT * FROM detail_surat_sakit WHERE id_surat_sakit=?',(id,))
    dtl = detail.fetchall()
    detail.close()

    list_param = [nama_user,role_user,srt,dtl]

    return render_template('detail-surat-sekre.html', list_param = list_param)


@bp.route('/sekre/detilSuratSakit/terima/<id>', methods=['GET'])
def terima_surat_sakit(id):
    if(get_session_state() == False):
        return redirect(url_for('auth.login'))

    nama_user = session['user_name']
    role_user = session['role']

    if(role_user != 'sekre'):
        flash('Halaman tidak bisa diakses oleh mahasiswa')
        return redirect(url_for('sisukit.list_surat_sakit_mahasiswa'))    

    today = date.today()
    db = get_db()
    surat = db.execute("""UPDATE surat_sakit
                  SET status_surat_sakit=?, disetujui_oleh=?, ditolak_oleh=?, tanggal_pengubahan_status=?
                  WHERE id=?;""",
               ('Diterima',nama_user+'-'+role_user,'-',today,id))
    db.commit()
    flash("Surat sakit berhasil diterima")
    list_param = [nama_user,role_user]

    return redirect(url_for('sisukit.detil_surat_sakit_sekre',id=id))


@bp.route('/sekre/detilSuratSakit/tolak/<id>', methods=['GET'])
def tolak_surat_sakit(id):
    if(get_session_state() == False):
        return redirect(url_for('auth.login'))

    nama_user = session['user_name']
    role_user = session['role']

    if(role_user != 'sekre'):
        flash('Halaman tidak bisa diakses oleh mahasiswa')
        return redirect(url_for('sisukit.list_surat_sakit_mahasiswa'))

    today = date.today()
    db = get_db()
    surat = db.execute("""UPDATE surat_sakit
                  SET status_surat_sakit=?, disetujui_oleh=?, ditolak_oleh=?, tanggal_pengubahan_status=?
                  WHERE id=?;""",
               ('Ditolak','-',nama_user+'-'+role_user,today,id))
    db.commit()
    flash("Surat sakit berhasil ditolak")
    list_param = [nama_user,role_user]

    return redirect(url_for('sisukit.detil_surat_sakit_sekre',id=id))       
    
@bp.route('/mahasiswa/listSuratSakit', methods=['GET'])       
def list_surat_sakit_mahasiswa():
    if(get_session_state() == False):
        return redirect(url_for('auth.login'))

    nama_user = session['user_name']
    role_user = session['role']
    npm = session['kode_identitas']

    if(role_user != 'mahasiswa'):
        flash('Halaman tidak bisa diakses oleh sekretariat')
        return redirect(url_for('sisukit.list_surat_sakit_sekre'))

    list_surat = []
    db = get_db()
    surat = db.execute(
        'SELECT * FROM surat_sakit WHERE npm=?',(npm,))#now by username then by NPM
    list_surat = surat
    list_param = [nama_user,role_user,list_surat]
    return render_template('list-surat-mahasiswa.html', list_param = list_param)

@bp.route('/mahasiswa/kirimSuratSakit', methods=['GET','POST'])
def kirim_surat_sakit():
    if(get_session_state() == False):
        return redirect(url_for('auth.login'))

    today = date.today()
    nama_user = session['user_name']
    role_user = session['role']
    npm = session['kode_identitas']

    if(role_user != 'mahasiswa'):
        flash('Halaman tidak bisa diakses oleh sekretariat')
        return redirect(url_for('sisukit.list_surat_sakit_sekre'))

    list_param = [nama_user,role_user,today]
    if request.method == 'POST':
        tanggal_submit = request.form['tanggal_submit']
        nama_penyakit = request.form['nama_penyakit']
        tanggal_izin = request.form['tanggal_izin']
        nama_mata_kuliah = request.form.getlist('mata_kuliah_izin')
        nama_dosen = request.form.getlist('dosen_mata_kuliah')
        print(request.form.getlist('mata_kuliah_izin'))
        print(request.form.getlist('dosen_mata_kuliah'))

        db = get_db()
        error = None
     
        if 'dokumen_surat_sakit' not in request.files:
            flash('Tidak ada form dokumen surat sakit')
            return redirect(request.url)

        file = request.files['dokumen_surat_sakit']

        if file.filename == '':
            flash('Masukkan surat sakit')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            extension = file.filename.rsplit('.',1)[1].lower()
            filename = secure_filename(nama_user+npm+nama_penyakit+tanggal_izin)
            surat = db.execute(
                'INSERT INTO surat_sakit (nama_mahasiswa, npm, tanggal_upload, surat_sakit_mahasiswa, status_surat_sakit, nama_penyakit, tanggal_izin) VALUES (?,?,?,?,?,?,?)',
                (nama_user, npm, tanggal_submit,filename+'.'+extension,'submitted',nama_penyakit,tanggal_izin)#change to real NPM after connect to UI API
            )   
            id_surat = surat.lastrowid

            for i in range (len(nama_mata_kuliah)):
                print(nama_mata_kuliah[i])
                print(nama_dosen[i])
                detail = db.execute(
                    'INSERT INTO detail_surat_sakit (id_surat_sakit,mata_kuliah_izin,nama_dosen_izin) VALUES (?,?,?)',
                    (id_surat, nama_mata_kuliah[i],nama_dosen[i])
                )

            file.save(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], (filename+'.'+extension)))# Windows OS
            db.commit()
            return redirect(url_for('sisukit.list_surat_sakit_mahasiswa'))


    return render_template('kirim-surat-sakit.html', list_param = list_param)    

@bp.route('/mahasiswa/detilSuratSakit/<id>', methods=['GET'])
def detil_surat_sakit_mahasiswa(id):
    if(get_session_state() == False):
        return redirect(url_for('auth.login'))

    nama_user = session['user_name']
    role_user = session['role']

    if(role_user != 'mahasiswa'):
        flash('Halaman tidak bisa diakses oleh sekretariat')
        return redirect(url_for('sisukit.list_surat_sakit_sekre'))

    db = get_db()
    db.row_factory = dict_factory
    cur = db.cursor()
    surat = cur.execute(
        'SELECT * FROM surat_sakit WHERE id=?',(id,))
    srt = surat.fetchall()
    detail = cur.execute(
        'SELECT * FROM detail_surat_sakit WHERE id_surat_sakit=?',(id,))
    dtl = detail.fetchall()
    detail.close()
    list_param = [nama_user,role_user,srt,dtl]

    return render_template('detail-surat-mahasiswa.html', list_param = list_param) 

