from flask import Flask, request, render_template, session, redirect, url_for, make_response
import MySQLdb, hashlib, os, time
import matplotlib, random, math, pygal
import matplotlib.pyplot as plt
from pylab import plot,show
from numpy import vstack,array
from numpy.random import rand
from scipy.cluster.vq import kmeans,vq,whiten
import pandas as pd
from decimal import *
from pygal.style import DefaultStyle, DarkGreenBlueStyle

custom_style = DarkGreenBlueStyle(colors=('#FF0000', '#0000FF', '#00FF00', '#FFFFFF', '#FFFF00', '#FF69B4', '#663399', '#7EC0EE', '#FF6600', '#40E0D0'))

app = Flask(__name__)
app.secret_key = "1|D0N'T|W4NT|TH15|T0|3E|R4ND0M"

@app.route('/', methods=['POST','GET'])
def register():
	if 'username' in session:
		return render_template('index_barchart.html', username = session['username'])
		
	if request.method == 'POST':
		db = MySQLdb.connect("aishwarya.ccxfz4hgtou6.us-west-2.rds.amazonaws.com","root","aishwarya","assignment3and4")
		cursor = db.cursor()
		
		username = request.form['username']
		password = request.form['password']
		if(username == '' or password == ''):
			return render_template('register.html')
			
		sql = "select username from users where username='"+username+"'"
		cursor.execute(sql)
		if cursor.rowcount == 1:
			return render_template('register.html')
		
		sql = "insert into users (username, password) values ('"+username+"','"+password+"')"
		cursor.execute(sql)
		db.commit()
		cursor.close()
		return render_template('login.html')
	else:
		return render_template('register.html')

		
@app.route('/login', methods=['POST','GET'])
def login():
	if 'username' in session:
		return render_template('index_barchart.html', username = session['username'])
		
	if request.method == 'POST':
		db = MySQLdb.connect("aishwarya.ccxfz4hgtou6.us-west-2.rds.amazonaws.com","root","aishwarya","assignment3and4")
		cursor = db.cursor()
		
		username = request.form['username']
		password = request.form['password']
		
		sql = "select username from users where username = '"+username+"' and password = '"+password+"'"
		cursor.execute(sql)
		if cursor.rowcount == 1:
			results = cursor.fetchall()
			for row in results:
				session['username'] = username
				return render_template('index_barchart.html', username = session['username'])
		else:
			return render_template('login.html')
	else:
		return render_template('login.html')


@app.route('/logout', methods=['POST','GET'])
def logout():
	if 'username' in session:
		session.pop('username', None)
	return redirect(url_for('register'))
	
@app.route('/opvisualization', methods=['POST','GET'])
def barchart():
	if request.method == 'POST':
		total_time = time.clock()
		col1 = request.form['c1']
		col2 = request.form['c2']
				
		if request.files['file'].filename == '':
			csv_data = pd.read_csv("/home/ubuntu/flaskapp/bardata.csv")
		else:
			file = request.files['file']
			csv_data = pd.read_csv(file)
			
		# x = csv_data[col1]
		# y = csv_data[col2]
		
		barChart = pygal.Bar(style=DefaultStyle, x_title='Magnitude', y_title='TotalCount', width=1280, height=720, show_legend=False, human_readable=True, title='MagnitudeCount Bar Chart')
		
		for index, row in csv_data.iterrows():
			barChart.add(row[col1],Decimal(row[col2]))
		
		list = ''	
		#list += '<center>Total Time: '+str(time.clock()-total_time)+'</center><br>'
		#graphData = barChart.render_data_uri()
		bar_chart.render_to_file('/home/ubuntu/flaskapp/chart.svg')
		#list += '<object type="image/svg+xml" data='+graphData+' />'
		#list += '<br><center>Total Time: '+str(time.clock()-total_time)+'</center>'
		
	return '''<html><head><title>Output</title><link rel="stylesheet" href="static/stylesheets/style.css"></head><body>'''+list+'''<br><center>Total Time: '''+str(time.clock()-total_time)+'''</center></body></html>'''
		
if __name__ == '__main__':
	app.run(debug=True)