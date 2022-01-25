#***********************
#Created: 24 Jan 2022 by Yamini Konka
#Last access: 24 Jan 2022
#Source: https://flask.palletsprojects.com/en/2.0.x/tutorial/views/#blueprints-and-views
#***********************



#----------- Importing libraries--------------
import functools

from flask import (
	Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

'''
-> A Blueprint object is created with name 'auth'
-> Like the application object, the blueprint needs to know where it's defined,
   so '__name__' is passed as the second argument. 
-> The 'url_prefix' will be prepended to all the URLs associated with the blueprint.
'''

# --------- Step 1 -----------
bp = Blueprint('auth', __name__, url_prefix='/auth')


# --------- Step 2 - Register View -----------
@bp.route('/register', methods=('GET', 'POST'))
def register():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		db = get_db()
		error = None

		if not username:
			error = 'Username is required.'
		elif not password:
			error = 'Password is required.'

		if error is None:
			try:
				db.execute(
					"INSERT INTO user (username, password) VALUES (?, ?)",
					(username, generate_password_hash(password)),
				)
				db.commit()
			except db.IntegrityError:
				error = f"User {username} is already registered."
		else:
			return redirect(url_for("auth.login"))


		flash(error)

	return render_template('auth/register.html')


# --------- Step 3 - Login View -----------
@bp.route('/login', methods=('GET', 'POST'))
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
			error = 'Incorrect username.'
		elif not check_password_hash(user['password'], password):
			error = 'Incorrect password.'

		if error is None:
			session.clear()
			session['user_id'] = user['id']
			return redirect(url_for('index'))

		flash(error)

	return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
	user_id = session.get('user_id')

	if user_id is None:
		g.user = None

	else:
		g.user = get_db().execute(
			'SELECT * FROM user WHERE id = ?', (user_id,)
		).fetchone()



@bp.route('/logout')
def logout():
	session.clear()
	return redirect(url_for('index'))


def login_required(view):
	@functools.wraps(view)
	def wrapped_view(**kwargs):
		if g.user is None:
			return redirect(url_for('auth.login'))

		return view(**kwargs)

	return wrapped_view