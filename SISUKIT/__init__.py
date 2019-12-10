import os
from flask import (
    Flask, Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from . import db
from .sso.csui_helper import get_access_token, verify_user

app = Flask(__name__)
UPLOAD_FOLDER = 'Surat_Sakit/'

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    from . import db
    db.init_app(app)

    from . import auth,sisukit
    app.register_blueprint(auth.bp)
    app.register_blueprint(sisukit.bp)


    return app

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        
        return view(**kwargs)
    
    return wrapped_view


@app.route('/', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        access_token = get_access_token(username,password)
        if access_token is not None:
            ver_user=verify_user(access_token)
            kode_identitas = ver_user['identity_number']
            role = ver_user['role']
            session.clear()
            session['user_name'] = username
            session['access_token'] = access_token
            session['kode_identitas'] = kode_identitas
            session['role'] = role
            if role == 'mahasiswa':
                return redirect(url_for('sisukit.list_surat_sakit_mahasiswa'))
        else:
            db = db.get_db()
            error = None
            user = db.execute(
                'SELECT * FROM user WHERE username = ?', (username,)
            ).fetchone()

            if user is None:
                error = 'Username salah'
            
            if password != user['password']:
                error = 'Password salah'

            if error is None:
                session.clear()
                session['user_name'] = user['username']
                session['kode_identitas'] = user['kode']
                session['role'] = user['role']
                session['access_token'] = '-'
                if user['role'] == 'sekre':
                    print('sekre berhasil login')
                    return redirect(url_for('sisukit.list_surat_sakit_sekre'))
            else:
                flash(error)
                return render_template('login.html')

    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
