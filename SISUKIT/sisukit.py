from flask import Flask
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from SISUKIT.db import get_db
from datetime import date

bp = Blueprint('sisukit', __name__, url_prefix='/sisukit')

def get_session_data():
    if 'user_id' in session:
        return session
    else:
        return "x"
    


@bp.route('/sekre/listSuratSakit', methods=['GET'])
def list_surat_sakit_sekre():
    nama_user = get_session_data()['user_name']
    role_user = get_session_data()['role']
    list_surat = []
    list_param = [nama_user,role_user,list_surat]


    return render_template('list-surat-sekre.html', list_param = list_param)

@bp.route('/sekre/detilSuratSakit/terima', methods=['POST'])
def terima_surat_sakit():
    nama_user = get_session_data()['user_name']
    role_user = get_session_data()['role']
    list_param = [nama_user,role_user]

    return redirect('list-surat-sekre.html', list_param = list_param) 

@bp.route('/sekre/detilSuratSakit/tolak', methods=['POST'])
def tolak_surat_sakit():
    nama_user = get_session_data()['user_name']
    role_user = get_session_data()['role']
    list_param = [nama_user,role_user]

    return redirect('list-surat-sekre.html', list_param = list_param)         
    
@bp.route('/mahasiswa/listSuratSakit', methods=['GET'])       
def list_surat_sakit_mahasiswa():
    nama_user = get_session_data()['user_name']
    role_user = get_session_data()['role']
    list_surat = []
    list_param = [nama_user,role_user,list_surat]

    return render_template('list-surat-mahasiswa.html', list_param = list_param)

@bp.route('/mahasiswa/kirimSuratSakit', methods=['GET','POST'])
def kirim_surat_sakit():
    today = date.today()
    nama_user = get_session_data()['user_name']
    role_user = get_session_data()['role']
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
            'INSERT INTO surat_sakit (nama_mahasiswa, tanggal_upload, surat_sakit_mahasiswa, status_surat_sakit, nama_penyakit) VALUES (?,?,?,?,?)',
            (nama_user,tanggal_submit,'---','submitted',nama_penyakit)
        )
        db.commit()


        

    return render_template('kirim-surat-sakit.html', list_param = list_param)    

@bp.route('/mahasiswa/detilSuratSakit', methods=['GET'])
def detil_surat_sakit_mahasiswa():
    nama_user = get_session_data()['user_name']
    role_user = get_session_data()['role']
    surat = "z"
    list_param = [nama_user,role_user,surat]

    return render_template('detail-surat-mahasiswa.html', list_param = list_param) 

@bp.route('/sekre/detilSuratSakit', methods=['GET'])
def detil_surat_sakit_sekre():
    nama_user = get_session_data()['user_name']
    role_user = get_session_data()['role']
    surat = "z"
    list_param = [nama_user,role_user,surat]

    return render_template('detail-surat-sekre.html', list_param = list_param) 