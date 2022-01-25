#***********************
#Created: 24 Jan 2022 by Yamini Konka
#Last access: 24 Jan 2022
#Source: https://flask.palletsprojects.com/en/2.0.x/tutorial/database/#connect-to-the-database
#***********************



#----------- Importing libraries--------------
# More info @ https://flask.palletsprojects.com/en/2.0.x/tutorial/database/#define-and-access-the-database
import sqlite3  # Interact with database , it has built-in support with Python

'''
-> Click is a Python package for creating beautiful command line interfaces
   in a composable way with as little code as necessary.
-> It's highly configurable but comes with sensible defaults out of the box

-> More info @ https://palletsprojects.com/p/click/
'''
import click   # Command Line Interface Creation Kit
# More info 'g' @ https://flask.palletsprojects.com/en/2.0.x/api/#flask.g
# More info 'current_app' @ https://flask.palletsprojects.com/en/2.0.x/api/#flask.current_app
from flask import current_app, g 

from flask.cli import with_appcontext


# Reference @ https://flask.palletsprojects.com/en/2.0.x/tutorial/database/#connect-to-the-database
def get_db():
	if 'db' not in g:
		g.db = sqlite3.connect(
			current_app.config['DATABASE'],
			detect_types=sqlite3.PARSE_DECLTYPES
		)
		g.db.row_factory = sqlite3.Row

	return g.db


def close_db(e=None):
	db = g.pop('db', None)

	if db is not None:   # If there is an database in request object(g) : Closed
		db.close()


def init_db():
	db = get_db()

	with current_app.open_resource('schema.sql') as f:
		db.executescript(f.read().decode('utf8'))



@click.command('init-db')
@with_appcontext
def init_db_command():
	"""Clear the existing data and create new tables."""
	init_db()
	click.echo('Initialized the database.')


def init_app(app):
	app.teardown_appcontext(close_db)
	app.cli.add_command(init_db_command)