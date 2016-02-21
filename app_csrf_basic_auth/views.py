from flask import Flask, g, request, Response, render_template, flash, redirect
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from . import app, db, models
from functools import wraps

def need_to_authenticate():
	return Response(response="Invalid/No Basic Auth header set", status=401, headers={'WWW-Authenticate': 'Basic realm="Login Required"'}, mimetype=None, content_type=None, direct_passthrough=False)

def check_auth(username, password):
	user = models.UserAccount.query.filter_by(username=username).first()
	if user and user.pass_is_equal(password):
		return True

def requires_auth(f):
	@wraps(f)
	def decorates(*args, **kwargs):
		auth = request.authorization
		if not auth or not check_auth(auth.username,auth.password):
			return need_to_authenticate()
		return f(*args, **kwargs)
	return decorates


@app.route("/")
def index():
	return redirect("/accountsummary", code=302, Response=None)

@app.route("/accountsummary")
@requires_auth
def summary():
	try:
		u = models.UserAccount.query.filter_by(username=request.authorization.username).first()
		return render_template("accountsummary.html", amount = u.amount, name =u.username)
	except:
		pass
	return Response(response="Some error happened", status=None, headers=None, mimetype=None, content_type=None, direct_passthrough=False)

@app.route("/login", methods=["POST", "GET"])
def login():
	return redirect("/accountsummary")

@app.route("/logout")
def logout():
	#destroy session
	return redirect("http://null:null@" + request.host + "/", code=302, Response=None)

@app.route("/transfer", methods=["POST"])
@requires_auth
def transfer():
	transferto = request.form["username"]
	amount = float()
	try:
		amount = float(request.form["amount"])
		print amount
		user = models.UserAccount.query.filter_by(username=request.form["username"]).first()
		print user
		if user:
			currentuser = models.UserAccount.query.filter_by(username=request.authorization.username).first()
			currentuser.amount = currentuser.amount - amount
			user.amount = user.amount + amount
			db.session.commit()
		else:
			flash("User does not exist, transfer failed", category='message')
			return redirect("/accountsummary", code=302, Response=None)
	except:
		flash("transfer unsuccessful", category='message')
		return redirect("/accountsummary", code=302, Response=None)
	print transferto, amount
	flash("transfer successful to {0}: {1}".format(transferto, amount))
	return redirect("/accountsummary", code=302, Response=None)

