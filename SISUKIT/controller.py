from flask import Flask

app = Flask(__name__)

@app.route('/')
def login():
    return 'Login'

@app.route('/sekre/listSuratSakit')
def list_surat_sakit_sekre():
    return 'List Surat Sakit Sekre'

@app.route('/sekre/detilSuratSakit')
def detil_surat_sakit_sekre():
    return 'Detail dari Surat Sakit Mahasiswa {NPM+ID Surat}' 
    
@app.route('/mahasiswa/listSuratSakit')       
def list_surat_sakit_mahasiswa():
    return 'List Surat Sakit Mahasiswa'

@app.route('/mahasiswa/detilSuratSakit')
def detil_surat_sakit_mahasiswa():
    return 'Detail dari surat sakit mahasiswa {ID}'

@app.route('/mahasiswa/kirimSuratSakit')
def kirim_surat_sakit():
    return 'Kirim Surat Sakit Mahasiswa'    