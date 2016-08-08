from flask import request
from flask import Flask


@app.route('/')
def index():
	user_agent = request.headers.get('User-Agent')
	return '<p>Your brower is %s</p>' %user_agent
