from flask import Flask
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from SISUKIT.db import get_db

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

@bp.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        db = get_db()
        error = None

        if not username:
            error = 'Masukkan Username'
        elif not password:
            error = 'masukkan password'
        elif not role:
            error = 'masukkan peran'
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} sudah ada.'.format(username)

        if error is None:
            db.execute(
                'INSERT INTO user (username, password, role) VALUES (?,?,?)',
                (username,generate_password_hash(password),role)
            )
            db.commit()
            return redirect(url_for('auth.login'))

        flash(error)
    
    return render_template('register.html')

@bp.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Username salah'
        elif not check_password_hash(user['password'], password):
            error = 'Password salah'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            session['user_name'] = user['username']
            session['role'] = user['role']
            session['state'] = True
            if user['role'] == 'mahasiswa':
                return redirect(url_for('sisukit.list_surat_sakit_mahasiswa'))
            elif user['role'] == 'sekre':
                return redirect(url_for('sisukit.list_surat_sakit_sekre'))
            

        flash(error)

    return render_template('login.html')

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

