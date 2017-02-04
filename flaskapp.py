from flask import Flask, request, render_template, session, redirect, url_for, make_response
import MySQLdb, hashlib, os, time
import matplotlib, random, math, pygal
import matplotlib.pyplot as plt
from pylab import plot,show
from numpy import vstack,array
from numpy.random import rand
from scipy.cluster.vq import kmeans,vq,whiten
import pandas as pd
from pygal.style import DefaultStyle, DarkGreenBlueStyle

custom_style = DarkGreenBlueStyle(colors=('#FF0000', '#0000FF', '#00FF00', '#FFFFFF', '#FFFF00', '#FF69B4', '#663399', '#7EC0EE', '#FF6600', '#40E0D0'))

app = Flask(__name__)
app.secret_key = "1|D0N'T|W4NT|TH15|T0|3E|R4ND0M"

@app.route('/', methods=['POST','GET'])
def register():
	if 'username' in session:
		return render_template('index.html', username = session['username'])
		
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
		return render_template('index.html', username = session['username'])
		
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
				return render_template('index.html', username = session['username'])
		else:
			return render_template('login.html')
	else:
		return render_template('login.html')


@app.route('/logout', methods=['POST','GET'])
def logout():
	if 'username' in session:
		session.pop('username', None)
	return redirect(url_for('register'))
	
@app.route('/k_means', methods=['POST','GET'])
def k_means():
	if request.method == 'POST':
		total_time = time.clock()
		col1 = request.form['c1']
		col2 = request.form['c2']
		clusters = int(request.form['clusters'])
		
		if request.files['file'].filename == '':
			csv_data = pd.read_csv("/home/ubuntu/flaskapp/data.csv")
		else:
			file = request.files['file']
			csv_data = pd.read_csv(file)
			
		#cols = ("time","latitude","longitude","depth","mag","magType","nst","gap","dmin","rms","net","id","updated","place","type","horizontalError","depthError","magError","magNst","status","locationSource","magSource")
		#print cols.index(col1)
		#print cols.index(col2)
		
		x = csv_data[col1]
		y = csv_data[col2]
		
		range_value = len(x)
		#clusters = int(math.sqrt(range_value/2))
		
		data = []
		count = 0
		for i in range(0,range_value):
			if math.isnan(x[i]) is False and math.isnan(y[i]) is False:
				count += 1
				element = []
				element.append(x[i])
				element.append(y[i])
				data.append(element)
		
		print count
		data = vstack(data)
		#data = whiten(data)
		centroids, distortion = kmeans(data,clusters)
		idx,_ = vq(data,centroids)
		
		list = ''
		totalPoints =[]
		clusterNames = []
		for i in range(clusters):
			resultNames = data[idx==i, 0]
			print "================================="
			
			name = "Cluster " + str(i+1)
			list += '<center>'+name
			print name
			clusterNames.append(name)
			count = 0
			
			for name in resultNames:
				count +=1
			print "Total cluster points: " + str(count)
			list += " : " + str(count) + "</center><br>"
			totalPoints.append(count)
			
		print totalPoints
		
		print " ==================================="
		print "Centroids : "
		print(centroids[0:])

		centroidPoints = []
		for row in centroids:
			cen = []
			cen.append(row[0])
			cen.append(row[1])
			centroidPoints.append(cen)
		
		scatterChart = pygal.XY(stroke=False,style=custom_style,dots_size=2,width=1280,height=720,legend_at_bottom=False,title='K-Means Clustering')

		for i in range(0,clusters):
			for j in range(0,1):
				scatterData = []
				for k in range(0,len(data[idx==i,j])-1):
					individualTuple = (data[idx==i,j][k], data[idx==i,j+1][k])
					scatterData.append(individualTuple)
					
				scatterChart.add(clusterNames[i],scatterData)
				
		scatterData = []
		for i in range(len(centroids[:,0])):
			individualTuple = (centroids[:,0][i-1], centroids[:,1][i-1])
			scatterData.append(individualTuple)	

		scatterChart.add("Centroids",scatterData)
				
		list += '<center>Total Time: '+str(time.clock()-total_time)+'</center><br>'
		graphData = scatterChart.render_data_uri()
		list += '<object type="image/svg+xml" data='+graphData+' />'
		list += '<br><center>Total Time: '+str(time.clock()-total_time)+'</center>'
		
	return '''<html><head><title>Output</title><link rel="stylesheet" href="static/stylesheets/style.css"></head><body>'''+list+'''<br><center>Total Time: '''+str(time.clock()-total_time)+'''</center></body></html>'''
		
if __name__ == '__main__':
	app.run(debug=True)