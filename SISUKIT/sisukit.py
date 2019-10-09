from flask import Flask
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint('sisukit', __name__, url_prefix='/sisukit')

@bp.route('/sekre/listSuratSakit', methods=['GET'])
def list_surat_sakit_sekre():
    return render_template('list-surat-sekre.html')

@bp.route('/sekre/detilSuratSakit/terima', methods=['POST'])
def terima_surat_sakit():
    return redirect('list-surat-sekre.html') 

@bp.route('/sekre/detilSuratSakit/tolak', methods=['POST'])
def tolak_surat_sakit():
    return redirect('list-surat-sekre.html')         
    
@bp.route('/mahasiswa/listSuratSakit', methods=['GET'])       
def list_surat_sakit_mahasiswa():
    return render_template('list-surat-mahasiswa.html')

@bp.route('/mahasiswa/kirimSuratSakit', methods=['GET','POST'])
def kirim_surat_sakit():
    return render_template('kirim-surat-sakit.html')    

@bp.route('/mahasiswa/detilSuratSakit')
def detil_surat_sakit_mahasiswa():
    return 'Detail dari surat sakit mahasiswa {ID}'

@bp.route('/sekre/detilSuratSakit')
def detil_surat_sakit_sekre():
    return 'Detail dari Surat Sakit Mahasiswa {NPM+ID Surat}' 