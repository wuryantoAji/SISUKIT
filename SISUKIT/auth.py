from flask import (
    Flask, Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from SISUKIT.db import get_db
from SISUKIT.sso.csui_helper import get_access_token, verify_user

bp = Blueprint('auth', __name__, url_prefix='/auth')

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        
        return view(**kwargs)
    
    return wrapped_view

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?',(user_id,)
        ).fetchone()


# @bp.route('/register', methods=['GET','POST'])
# def register():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         role = request.form['role']
#         db = get_db()
#         error = None

#         if not username:
#             error = 'Masukkan Username'
#         elif not password:
#             error = 'masukkan password'
#         elif not role:
#             error = 'masukkan peran'
#         elif db.execute(
#             'SELECT id FROM user WHERE username = ?', (username,)
#         ).fetchone() is not None:
#             error = 'User {} sudah ada.'.format(username)

#         if error is None:
#             db.execute(
#                 'INSERT INTO user (username, password, role) VALUES (?,?,?)',
#                 (username,generate_password_hash(password),role)
#             )
#             db.commit()
#             db.close()
#             return redirect(url_for('auth.login'))
        
#         flash(error)
    
#     return render_template('register.html')



@bp.route('/login', methods=['GET','POST'])
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
            db = get_db()
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

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

