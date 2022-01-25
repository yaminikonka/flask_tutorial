/*
#***********************
#Created: 24 Jan 2022 by Yamini Konka
#Last access: 24 Jan 2022
#Source: https://flask.palletsprojects.com/en/2.0.x/tutorial/database/#connect-to-the-database
#***********************
*/

-- Code @ https://flask.palletsprojects.com/en/2.0.x/tutorial/database/#create-the-tables


DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;

CREATE TABLE user (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	username TEXT UNIQUE NOT NULL,
	password TEXT NOT NULL

);

CREATE TABLE post (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	author_id INTEGER NOT NULL,
	created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	title TEXT NOT NULL,
	body TEXT NOT NULL,
	FOREIGN KEY (author_id) REFERENCES user (id)
);