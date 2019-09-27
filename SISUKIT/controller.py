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
    
       
