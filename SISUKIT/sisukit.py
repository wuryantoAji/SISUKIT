from flask import Flask
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from SISUKIT.db import get_db
from datetime import date
from . import auth

bp = Blueprint('sisukit', __name__, url_prefix='/sisukit')

def get_session_state():
    if 'user_id' in session:
        return True
    else:
        return False


@bp.route('/sekre/listSuratSakit', methods=['GET'])
def list_surat_sakit_sekre():
    if(get_session_state() == False):
        return redirect(url_for('auth.login'))

    nama_user = session['user_name']
    role_user = session['role']
    list_surat = []
    list_param = [nama_user,role_user,list_surat]


    return render_template('list-surat-sekre.html', list_param = list_param)

@bp.route('/sekre/detilSuratSakit/terima/<id>', methods=['POST'])
def terima_surat_sakit(id):
    nama_user = session['user_name']
    role_user = session['role']
    list_param = [nama_user,role_user]

    return redirect('list-surat-sekre.html', list_param = list_param) 

@bp.route('/sekre/detilSuratSakit/tolak/<id>', methods=['POST'])
def tolak_surat_sakit(id):
    nama_user = session['user_name']
    role_user = session['role']
    list_param = [nama_user,role_user]

    return redirect('list-surat-sekre.html', list_param = list_param)         
    
@bp.route('/mahasiswa/listSuratSakit', methods=['GET'])       
def list_surat_sakit_mahasiswa():
    if(get_session_state() == False):
        return redirect('login.html')

    nama_user = session['user_name']
    role_user = session['role']
    list_surat = []
    db = get_db()
    surat = db.execute(
        'SELECT * FROM surat_sakit WHERE nama_mahasiswa=?',(nama_user,))#now by username then by NPM
    list_surat = surat
    list_param = [nama_user,role_user,list_surat]
    return render_template('list-surat-mahasiswa.html', list_param = list_param)

@bp.route('/mahasiswa/kirimSuratSakit', methods=['GET','POST'])
def kirim_surat_sakit():
    if(get_session_state() == False):
        return redirect('login.html')

    today = date.today()
    nama_user = session['user_name']
    role_user = session['role']
    list_param = [nama_user,role_user,today]
    if request.method == 'POST':
        tanggal_submit = request.form['tanggal_submit']
        nama_penyakit = request.form['nama_penyakit']
        tanggal_izin = request.form['tanggal_izin']
        nama_mata_kuliah = request.form['mata_kuliah_izin']
        nama_dosen = request.form['dosen_mata_kuliah']
        db = get_db()
        error = None
        surat = db.execute(
            'INSERT INTO surat_sakit (nama_mahasiswa, npm, tanggal_upload, surat_sakit_mahasiswa, status_surat_sakit, nama_penyakit, tanggal_izin) VALUES (?,?,?,?,?,?,?)',
            (nama_user, 10, tanggal_submit,'---','submitted',nama_penyakit,tanggal_izin)#change to real NPM after connect to UI API
        )
        id_surat = surat.lastrowid
        db.commit()
        detail = db.execute(
            'INSERT INTO detail_surat_sakit (id_surat_sakit,mata_kuliah_izin,nama_dosen_izin) VALUES (?,?,?)',
            (id_surat, nama_mata_kuliah,nama_dosen)
        )
        db.commit()
        return redirect(url_for('sisukit.list_surat_sakit_mahasiswa'))

    return render_template('kirim-surat-sakit.html', list_param = list_param)    

@bp.route('/mahasiswa/detilSuratSakit/<id>', methods=['GET'])
def detil_surat_sakit_mahasiswa(id):
    if(get_session_state() == False):
        return redirect('login.html')

    nama_user = session['user_name']
    role_user = session['role']
    db = get_db()
    surat = db.execute(
        'SELECT * FROM surat_sakit WHERE id=?',(id,))#now by username then by NPM
    srt = surat.fetchall()
    surat.close()
    detail = db.execute(
        'SELECT * FROM detail_surat_sakit WHERE id_surat_sakit=?',(id,))#now by username then by NPM
    dtl = detail.fetchall()
    detail.close()
    list_param = [nama_user,role_user,srt,dtl]

    return render_template('detail-surat-mahasiswa.html', list_param = list_param) 

@bp.route('/sekre/detilSuratSakit/<id>', methods=['GET'])
def detil_surat_sakit_sekre(id):
    if(get_session_state() == False):
        return redirect('login.html')
        
    nama_user = session['user_name']
    role_user = session['role']
    surat = "z"
    list_param = [nama_user,role_user,surat]

    return render_template('detail-surat-sekre.html', list_param = list_param) 