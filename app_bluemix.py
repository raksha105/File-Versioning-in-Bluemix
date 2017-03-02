"""Cloud Foundry test"""
from flask import Flask , render_template, request, redirect, url_for
import swiftclient
from flask.json import jsonify
import json
from pprint import pprint
import MySQLdb

import os
global conn
import aes



app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1000000
# On Bluemix, get the port number from the environment variable VCAP_APP_PORT
# When running this app on the local machine, default the port to 8080
port = int(os.getenv('VCAP_APP_PORT', 8080))







@app.route('/', methods=['GET', 'POST'])
def hello_world():
		
	
	
	
		return """  <form method="post" action="user_submit">
        <p><input type="text" name="username" value="" placeholder="Username "></p>"""
	
		# return """ <html><body>
	# <form method="post" action="login">
        # <p><input type="text" name="login" value="" placeholder="Username or Email"></p>
        # <p><input type="password" name="password" value="" placeholder="Password"></p>
		# <input type="submit" name="commit" value="Login"></p>
		# </form>
		# """

		
@app.route('/user_submit', methods=['GET', 'POST'])
def user_submit():	
		global user_name
		user_name =  request.form['username']
		print user_name
		
		if(user_name == "Tom"):
				app.config['MAX_CONTENT_LENGTH'] = 2000
				
		if(user_name == "Susan"):
				app.config['MAX_CONTENT_LENGTH'] = 5000
				
		if(user_name == "Pepe"):
				app.config['MAX_CONTENT_LENGTH'] = 1000
			
		
		
		auth_url = "https://identity.open.softlayer.com/v3"
		password = "j=UL})!(?jn3HKa0"
		project_id = "5e47613b0b484065bac4de170c4c2335"
		user_id = "0961b2e11ef4447dbcb5582a1454ac3a"
		region_name = "dallas"
		conn = swiftclient.Connection(key=password,
		authurl=auth_url,
		auth_version='3',
		os_options={"project_id": project_id,
					"user_id": user_id,
					"region_name": region_name})	
		container_name = 'original_folder'
		
		
		check =[]
		bytes_file =[]
		
		for container in conn.get_account()[1]:
			print container
			for data in conn.get_container(container['name'])[1]:
			
				check.append(data['name'])
			print check
			names = jsonify(check)
			

	
	
	
		
		
		if((user_name == "Tom") or user_name=="Pepe" or user_name =="Susan" ):
				return render_template('users.html', user_name=user_name, names=check, names_b =bytes_file)
		else:
			return "incorrect"
			


@app.route('/user_dsiplay', methods=['GET', 'POST'])
def user_dsiplay():

		auth_url = "https://identity.open.softlayer.com/v3"
		password = "j=UL})!(?jn3HKa0"
		project_id = "5e47613b0b484065bac4de170c4c2335"
		user_id = "0961b2e11ef4447dbcb5582a1454ac3a"
		region_name = "dallas"
		conn = swiftclient.Connection(key=password,
		authurl=auth_url,
		auth_version='3',
		os_options={"project_id": project_id,
					"user_id": user_id,
					"region_name": region_name})	
					
					
		container_name = 'original_folder'
		filename =  request.form['display']
		print filename
		
		downloaded = conn.get_object(container_name,filename)
		print downloaded
		print downloaded[0]['content-length']
		print 'before this'
		
		f = open(filename, "w")
		f.write(downloaded[1]);
		f = open(filename)
		temp_content = f.read()
		temp_name = f.name
		print temp_content
		print temp_name
		
		#decrypt_name = f.name
		
		aes.decrypt(temp_name, "test", outputfile=None)
		f.close()
		f_f = open(filename[:-4])
		f_content = f_f.read()
		f_f.close()
		os.remove(filename)
		return f_content
		
	

			

@app.route('/user_upload', methods=['GET', 'POST'])
def user_upload():
		
		global user_name
		auth_url = "https://identity.open.softlayer.com/v3"
		password = "j=UL})!(?jn3HKa0"
		project_id = "5e47613b0b484065bac4de170c4c2335"
		user_id = "0961b2e11ef4447dbcb5582a1454ac3a"
		region_name = "dallas"
		conn = swiftclient.Connection(key=password,
		authurl=auth_url,
		auth_version='3',
		os_options={"project_id": project_id,
					"user_id": user_id,
					"region_name": region_name})	
		container_name = 'original_folder'
		
		file = request.files['get_myfile']
		print file
		
		print container_name
		
		filename=file.filename
		filecontent=file.read()
		
		fo = open("output.txt", "w")
		fo.write(filecontent);
		print fo
		
		fo = open("output.txt")
		output_content = fo.read()
		print output_content
		
		temp_name = fo.name
		print 'temporar name' + temp_name

		
		aes.encrypt(temp_name, "test", outputfile=None)
		target = open(temp_name+'.aes')
		target_content = target.read()
		
		print target_content
		print target
		
		conn.put_object(container_name,filename+user_name+'.aes',contents=target_content,content_type='text/plain')
		
		
		target.close()
		fo.close()
		os.remove(temp_name+'.aes')
		os.remove(temp_name)


		
		return container_name
		
		

@app.route('/login', methods=['GET', 'POST'])
def login():
		
		global u_id

		user_name =  request.form['login']
		print user_name
		
		pass_word =  request.form['password']
		print pass_word

		
		db = MySQLdb.connect(host="us-cdbr-iron-east-04.cleardb.net",   
						user="b03e31d33b8384",        
						passwd="38370136",
						db="ad_f80343430d3be24")
					 
		cur = db.cursor()
		cur.execute("select id, username, user_password from user_credential where username=%s and user_password=%s",(user_name, pass_word))
		
		

		for row in cur.fetchall():
			
			
			u_id = row[0]
			print u_id
			if row is not None:
				
				
				return"""<form id ="db_store" enctype="multipart/form-data" method="post" action="db_store">
		
		<input type ="submit" value="save to cloud db" name ="db"></form>
		
		<form id ="file_store" enctype="multipart/form-data" method="post" action="file_store">
		<input type ="submit" value="save as file " name="file">
		</form>
		
		
		
		
		"""
		db.close()
		return "wrong user name or password"

				
			
@app.route('/dbfile_display', methods=['GET', 'POST'])
def dbfile_display():
		
		all_files = []
		db = MySQLdb.connect(host="us-cdbr-iron-east-04.cleardb.net",   
						user="b03e31d33b8384",        
						passwd="38370136",
						db="ad_f80343430d3be24")
					 
		cur = db.cursor()
		cur.execute("select file_description, user_file, file_name from user_storage")
		
		

		for row in cur.fetchall():
				print row[2]
				all_files.append(row[2])
				
			
		print all_files		
		return render_template('files.html', all_files=all_files)
		
	


@app.route('/file_store', methods=['GET', 'POST'])
def file_store():
		return"""


		<form id="upload" enctype="multipart/form-data" method="post" action="upload">
    <p><input id="fileupload" name="myfile" type="file" />
    <input type="submit" value="submit" id="submit" /></form>
	
	
	
	<form id="deleting" enctype="multipart/form-data" method="post" action="display">
	
	 <input type="submit" name ="display" value="display" id="display" />
	
	
	
	
	
    </form>
"""


@app.route('/db_store', methods=['GET', 'POST'])
def db_store():
		
		
		
		return"""<form id="upload_db" enctype="multipart/form-data" method="post" action="upload_db">
		<p><input id="dbupload" name="dbfile" type="file" /></br>
		About the file<input type="text area" name="about_file" id="about_file">
		<input type="submit" value="submit" id="submit" /></form>
		
		
		<form id ="dbfile_display" enctype="multipart/form-data" method="post" action="dbfile_display">
		<input type ="submit" value="downlaod file " name="downlaod_file">
		</form>
		
		"""
	
		
@app.route('/upload_db', methods=['GET', 'POST'])
def upload_db():

		global u_id
		db_file = request.files['dbfile']
		print file
		file_name = db_file.filename
		print file_name
		
		db_content = db_file.read()
		print db_content
		
		about_file = request.form['about_file']
		print about_file
		print type(u_id)
		
		db = MySQLdb.connect(host="us-cdbr-iron-east-04.cleardb.net",   
						user="b03e31d33b8384",        
						passwd="38370136",
						db="ad_f80343430d3be24")
					 
		cur = db.cursor()
		cur.execute("insert into user_storage(user_id, file_description, user_file, file_name) values(%s,%s,%s,%s)", (str(u_id),about_file,db_content,file_name))
		db.commit()
		
		# cur.execute("select id, username, user_password from user_credential where username=%s and user_password=%s",(user_name, pass_word))
		
	
		db.close()
		return "updated database"
	


@app.route('/db_download', methods=['POST'])
def db_download():
		return "dispay content n download file"
	
	
@app.route('/upload', methods=['POST'])
def upload():
		print "hey"
		auth_url = "https://identity.open.softlayer.com/v3"
		password = "j=UL})!(?jn3HKa0"
		project_id = "5e47613b0b484065bac4de170c4c2335"
		user_id = "0961b2e11ef4447dbcb5582a1454ac3a"
		region_name = "dallas"
		conn = swiftclient.Connection(key=password,
		authurl=auth_url,
		auth_version='3',
		os_options={"project_id": project_id,
					"user_id": user_id,
					"region_name": region_name})	
		container_name = 'cloud_container'
		print container_name
		conn.put_container(container_name)
     # Get the name of the uploaded file
		file = request.files['myfile']
		filename=file.filename
		filecontent=file.read()
		
		fo = open("output.txt", "w")
		fo.write(filecontent);
		print fo
		
		fo = open("output.txt")
		output_content = fo.read()
		print output_content
		
		temp_name = fo.name
		print 'temporar name' + temp_name

		
		aes.encrypt(temp_name, "test", outputfile=None)
		target = open(temp_name+'.aes')
		target_content = target.read()
		
		print target_content
		print target

		
    #to read file content
		
		
		conn.put_object(container_name,filename+'.aes',contents=target_content,content_type='text/plain')
		# for container in conn.get_account()[1]:
			# print 'container'+container
			# for data in conn.get_container(container['name'])[1]:
				# print 'data in container'+data
				
		target.close()
		fo.close()
		os.remove(temp_name+'.aes')
		os.remove(temp_name)

		
		return """ 	
	<form id="file_store" enctype="multipart/form-data" method="post" action="file_store">
	
	 <input type="submit" name ="fileupload" value="upload more" id="fileupload" /> </form>
	 
	
	 
	 
	 
	 
	 """
	 
	 
				


				
				
				
			

				

	
@app.route('/delete', methods=['POST'])
def delete():


		
		auth_url = "https://identity.open.softlayer.com/v3"
		password = "j=UL})!(?jn3HKa0"
		project_id = "5e47613b0b484065bac4de170c4c2335"
		user_id = "0961b2e11ef4447dbcb5582a1454ac3a"
		region_name = "dallas"
		conn = swiftclient.Connection(key=password,
		authurl=auth_url,
		auth_version='3',
		os_options={"project_id": project_id,
					"user_id": user_id,
					"region_name": region_name})	
					
					
		container_name = 'cloud_container'
		filename =  request.form['delete']
		print filename
		
		# for container in conn.get_account()[1]:
			# for data in conn.get_container(container['name'])[1]:
				# return 'object: {0}\t size: {1}\t date: {2}'.format(data['name'], data['bytes'], data['last_modified'])

		conn.delete_object(container_name, filename)
		return 'deleted'
		
	




@app.route('/download', methods=['POST'])
def download():


		
		auth_url = "https://identity.open.softlayer.com/v3"
		password = "j=UL})!(?jn3HKa0"
		project_id = "5e47613b0b484065bac4de170c4c2335"
		user_id = "0961b2e11ef4447dbcb5582a1454ac3a"
		region_name = "dallas"
		conn = swiftclient.Connection(key=password,
		authurl=auth_url,
		auth_version='3',
		os_options={"project_id": project_id,
					"user_id": user_id,
					"region_name": region_name})	
					
					
		container_name = 'cloud_container'
		filename =  request.form['download']
		print filename
		
		
		
		
		
		# for container in conn.get_account()[1]:
			# for data in conn.get_container(container['name'])[1]:
				# return 'object: {0}\t size: {1}\t date: {2}'.format(data['name'], data['bytes'], data['last_modified'])

		
		downloaded = conn.get_object(container_name,filename)
		print downloaded
		print downloaded[0]['content-length']
		print 'before this'
		
		f = open(filename, "w")
		f.write(downloaded[1]);
		f = open(filename)
		temp_content = f.read()
		temp_name = f.name
		print temp_content
		print temp_name
		
		#decrypt_name = f.name
		
		aes.decrypt(temp_name, "test", outputfile=None)
		f.close()
		f_f = open(filename[:-4])
		f_content = f_f.read()
		f_f.close()
		os.remove(filename)
		return f_content	
	
@app.route('/display', methods=['POST'])
def display():
		print "hey"
		auth_url = "https://identity.open.softlayer.com/v3"
		password = "j=UL})!(?jn3HKa0"
		project_id = "5e47613b0b484065bac4de170c4c2335"
		user_id = "0961b2e11ef4447dbcb5582a1454ac3a"
		region_name = "dallas"
		conn = swiftclient.Connection(key=password,
		authurl=auth_url,
		auth_version='3',
		os_options={"project_id": project_id,
					"user_id": user_id,
					"region_name": region_name})	
		container_name = 'cloud_container'
		check =[]
		
		for container in conn.get_account()[1]:
			print container
			for data in conn.get_container(container['name'])[1]:
			
				check.append(data['name'])
			print check
			names = jsonify(check)
			

	
	
		
		return render_template('view_files.html', names=check)
						
		#return 'object: {0}\t size: {1}\t date: {2}'.format(data['name'], data['bytes'], data['last_modified'])
		
		
	
	
				

if __name__ == '__main__':
    
    #app.run(debug = True)
	
	app.run(host='ec2-52-39-213-50.us-west-2.compute.amazonaws.com', port=port)
