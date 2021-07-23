#!/usr/bin/env python3

from flask import Flask, render_template_string, request

app = Flask(__name__)

@app.route('/')
def index():
	return f"<pre><code>{open(__file__).read()}</code></pre>"

@app.route('/check')
def check():
	flag = open("flag.txt", 'r').read().strip()
	query = request.args["flag"]
	try:
		return render_template_string('{{ flag == "%s" }}'%query, flag=flag)
	except Exception as e:
		return str(e)

app.run('localhost', 4000)
