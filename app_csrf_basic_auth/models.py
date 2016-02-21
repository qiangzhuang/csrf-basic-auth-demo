from flask_sqlalchemy import SQLAlchemy
from . import app, db
from flask import logging
import binascii, hashlib


class UserAccount(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.Text, unique=True)
	password = db.Column(db.Text)
	salt = db.Column(db.Text)
	amount = db.Column(db.Float)

	def __init__(self, username, password, amount, salt):
		self.username = username
		self.amount = amount
		self.password = password
		self.salt = salt
	def __repr__(self):
		return "%r" % self.amount

	def pass_is_equal(self, password):
		pw = binascii.hexlify(hashlib.pbkdf2_hmac("sha512", password, self.salt, 100000, 128))
		print pw
		print self.password
		#if self.is_equal(pw.decode("hex"), self.password.decode("hex")):
		if pw == self.password:
			return True
		else:
			return False


	def is_equal(self, a, b):
	    if len(a) != len(b):
	        return False

	    result = 0
	    for x, y in zip(a, b):
	        result |= x ^ y
	    return result == 0
